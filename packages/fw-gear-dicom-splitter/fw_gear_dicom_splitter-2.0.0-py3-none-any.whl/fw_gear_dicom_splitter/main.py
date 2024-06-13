"""Module to run gear."""

import logging
import typing as t
import zipfile
from pathlib import Path

import pandas as pd
from fw_file.dicom import DICOMCollection
from fw_file.dicom.utils import sniff_dcm

from .metadata import SeriesName, add_contributing_equipment, update_localizer_frames
from .dicom_splitter.base import SingleSplitter, SplitterError
from .splitters import (
    EuclideanSplitter,
    JensenShannonDICOMSplitter,
    UniqueTagMultiSplitter,
    UniqueTagSingleSplitter,
    split_by_geometry,
)
from .utils import collection_from_df, collection_to_df

# Override dicom validation logging level
validation_log = logging.getLogger("fw_file.dicom.validation")
validation_log.setLevel(logging.INFO)
log = logging.getLogger(__name__)

SCORE_THRESH = 0.5


def run_individual_split(
    splitter: SingleSplitter, dataframe: pd.DataFrame, **kwargs: t.Any
) -> None:
    """Helper function to run one splitter algorithm."""
    try:
        split = splitter.split(dataframe, **kwargs)
    except SplitterError as e:
        log.error(e.args[0])
        if log.parent.level > logging.DEBUG:  # type: ignore
            log.error("Enable debug to see full stack")
        log.info(
            "Note: JensenShannon splitter is not necessary, but this "
            "failure indicates there is probably something wrong with your "
            "dicom's PixelData or PixelData attributes."
        )
        log.debug(repr(e), exc_info=True)
        return
    frames_found = split[split["decision"] > 0]
    log.debug(
        "%s found %d localizer frames",
        splitter.__class__.__name__,
        frames_found.shape[0],
    )
    dataframe.loc[dataframe["path"] == split["path"], "score"] += split["decision"]  # type: ignore


def gen_split_score(dcm: DICOMCollection) -> pd.DataFrame:
    """Generate 'voting' score for each frame in DICOM.

    Voting score comes from multiple splitting algorithms and tries to
    find a concensus among these different methods.

    Methods so far:
        1. Split on change in neighboring frames 'ImageOrientationPatient'.
        2. Split on change in neighboring frames 'ImagePositionPatient'.
        3. Split on change in neighboring frames pixel intensity distribution.
        4. Split on unique combo of 'Rows', 'Columns' tags across archive.
        5. Split on unique value of 'ImageType' across archive.
    """
    total: int = 0
    # Need ordering for pairwise splitters
    if all(dcm.bulk_get("InstanceNumber")):
        dcm.sort(key=lambda x: x.InstanceNumber)
        dataframe = collection_to_df(dcm)
        dataframe["score"] = 0

        if all(dcm.bulk_get("ImageOrientationPatient")):
            log.debug(
                "ImageOrientationPatient tag present, attempting localizer split.."
            )
            iop_splitter = EuclideanSplitter(
                dcm, decision_val=30, tag="ImageOrientationPatient"
            )
            run_individual_split(iop_splitter, dataframe)
            total += iop_splitter.decision_val
        else:
            log.debug("ImageOrientationPatient tags not all present.")

        if all(dcm.bulk_get("ImagePositionPatient")):
            log.debug("ImagePositionPatient tag present, attempting localizer split..")
            ipp_splitter = EuclideanSplitter(
                dcm, decision_val=30, tag="ImagePositionPatient"
            )
            run_individual_split(ipp_splitter, dataframe)
            total += ipp_splitter.decision_val
        else:
            log.debug("ImagePositionPatient tags not all present.")

        log.debug("Attempting Jensen-Shannon localizer splitter")
        js_splitter = JensenShannonDICOMSplitter(dcm, decision_val=20)
        try:
            run_individual_split(js_splitter, dataframe)
            total += js_splitter.decision_val
        except RuntimeError:
            log.warning("JensenShannon fit didn't converge. Moving on...")
        except AttributeError:
            log.warning("PixelData not present on one or more slices.  Moving on...")
    else:
        dataframe = collection_to_df(dcm)
        dataframe["score"] = 0
    # Try splitting by rows and columns
    if all(dcm.bulk_get("Rows")) and all(dcm.bulk_get("Columns")):
        log.debug("Row and Column tags present, attempting localizer split...")
        row_col_splitter = UniqueTagSingleSplitter(
            dcm, decision_val=30, tags=["Rows", "Columns"]
        )
        run_individual_split(row_col_splitter, dataframe)
        total += row_col_splitter.decision_val
    else:
        log.debug("Row and Column tags not all present.")

    # Try splitting by image type
    # TODO: Leave out for now, refine heuristic looking specificall for
    # 'LOCALIZER' or other manufacturer specific codewords for Localizer
    # frames.
    #    if all(dcm.bulk_get("ImageType")):
    #        log.debug("ImageType tag present, attempting localizer split..")
    #        image_type_splitter = UniqueTagSingleSplitter(
    #            dcm, tags=["ImageType"]
    #        )
    #        run_individual_split(image_type_splitter, dataframe)
    #        total += image_type_splitter.decision_val
    #    else:
    #        log.debug("Row and Column tags not all present.")

    dataframe["score"] /= total
    return dataframe


def run_split_localizer(
    dcm: DICOMCollection,
) -> t.Tuple[DICOMCollection, ...]:
    """Split localizer from dicom archive.

    Args:
        dcm (DICOMCollection): Dicom Archive

    Returns:
        t.Tuple[DICOMCollection, ...]: Tuple of dicom collections,
            first is the main archive, second is the localizer if any.
    """
    if len(dcm) < 2:
        log.warning(
            "Refusing to extract localizer from archive with less than 2 frames."
        )
        return (dcm, DICOMCollection())
    log.debug("Generating splitting score")
    score_dataframe = gen_split_score(dcm)

    dicom_dataframe = score_dataframe[score_dataframe["score"] < SCORE_THRESH]
    localizer_dataframe = score_dataframe[score_dataframe["score"] >= SCORE_THRESH]
    log.debug("Found %d localizer frames", localizer_dataframe.shape[0])

    if localizer_dataframe.shape[0] >= dicom_dataframe.shape[0] * 0.5:
        log.error("Splitting localizer may have failed...")

    dicom_coll = collection_from_df(dcm, dicom_dataframe)
    localizer_coll = collection_from_df(dcm, localizer_dataframe)
    return (dicom_coll, localizer_coll)


def check_secondary_capture_sopclassuid(dcm: DICOMCollection) -> bool:
    """
    Returns False if the SOPClassUID is a secondary capture image storage (SCIS).

    We shouldn't split the input file and should exit early in that case. This should
    cover some of the reviewed and approved variants of SCIS. When we have multiple
    slices in the dicom collection, then only split if all the unique SOPClassUID's
    match ones approved for not splitting.

    Args:
        dcm: DICOMCollection
            A collection of dicom slices.

    Returns:
        no_split: bool
            True if the collection should not be split. False if otherwise.
    """
    log.debug(
        "Attempting to see if SOPClassUID's all match options for not splitting..."
    )
    # Define reviewed and approved SOPClassUID cases matching Secondary Capture Image
    secondary_capture_sopclassuids = {
        "1.2.840.10008.5.1.4.1.1.7": "Secondary Capture Image",
        "1.2.840.10008.5.1.4.1.1.7.1": "Multi-frame Single Bit Secondary Capture Image",
        "1.2.840.10008.5.1.4.1.1.7.2": "Multi-frame Grayscale Byte Secondary Capture Image",
        "1.2.840.10008.5.1.4.1.1.7.3": "Multi-frame Grayscale Word Secondary Capture Image",
        "1.2.840.10008.5.1.4.1.1.7.4": "Multi-frame True Color Secondary Capture Image",
    }
    sopc_uids = list(set(dcm.bulk_get("SOPClassUID")))

    # Return false (i.e., proceed to split) if at least one SOPClassUID is not in the
    # secondary_capture_sopclassuids dict
    matched_no_split = {}
    for sopc_uid in sopc_uids:
        if sopc_uid not in secondary_capture_sopclassuids:
            log.debug(
                "SOPClassUID %s do not match secondary capture SOPClassUID list: \n%s"
                % (sopc_uid, secondary_capture_sopclassuids.keys())
            )
            return False
        matched_no_split[sopc_uid] = secondary_capture_sopclassuids[sopc_uid]

    log.warning(
        "All the DICOM frame SOPClassUID match an Image Storage approved for not "
        "splitting. \n No split will be attempted.\n"
        "Dict with keys SOPClassUID and values IOD specification: \n\t'%s')"
        % matched_no_split
    )
    return True


def add_phases_to_output(
    outputs: dict,
    collection: DICOMCollection,
    phase_count: int,
    phase_indexes: list[int],
):
    """
    Add child collections to output_list derived from phases of the parent collection

    Args:
        outputs (t.Optional[t.List[str]]): Dicom archive
        collection (DICOMCollection): Parent collection
        phase_count (bool): Number of phases
        phase_indexes (int): Array that maps index to phase
    """
    secondary = []
    for k in range(phase_count):
        secondary.append(DICOMCollection())
    for image_index in range(len(collection)):
        phase_index = phase_indexes[image_index]
        secondary[phase_index].append(collection[image_index])
    for k in range(phase_count):
        sn = k + 1
        coll = secondary[k]
        name = SeriesName.gen_name(coll, series_number=str(sn))
        outputs[name] = coll
    return outputs


def split_dicom(  # pylint: disable=too-many-locals,too-many-statements
    dcm: DICOMCollection,
    group_by: t.Optional[t.List[str]],
    split_localizer: bool,
    max_geom_splits=-1,
) -> t.Optional[t.Dict[SeriesName, DICOMCollection]]:
    """Split the dicom archive by tags or localizer.

    Args:
        dcm (DICOMCollection): Dicom archive
        group_by (t.Optional[t.List[str]]): List of tags to split by.
        split_localizer (bool): Whether to split localizer.
        max_geom_splits (int): Maximum number of splits by geometry

    Returns:
        t.Dict[SeriesName, DICOMCollection]: Dictionary with output filenames as
            keys, and Dicom collections.
    """
    outputs = {}

    # Do not attempt to split secondary capture image storage SOPClassUID
    if check_secondary_capture_sopclassuid(dcm):
        return {}  # return empty dict so it doesn't trigger a failed split

    geometric_split = False
    if max_geom_splits > 0:
        phase_count, indexes = split_by_geometry(dcm, max_split_count=max_geom_splits)
        if phase_count is not None and phase_count > 1:
            add_phases_to_output(outputs, dcm, phase_count, indexes)
            geometric_split = True

    if group_by and not geometric_split:
        dataframe = collection_to_df(dcm)
        dataframe["score"] = 0
        tag_splitter = UniqueTagMultiSplitter(dcm, 10, tags=group_by)
        out_dfs = list(tag_splitter.split(dataframe))
        # Sort by number of frames
        out_dfs.sort(key=lambda out_df: out_df.shape[0], reverse=True)
        # GEAR-896, name outputs of group-by consistently with:
        #   {SeriesNumber}-{Modality}-{SeriesDescription}.dicom.zip
        #   and appending a `_{count}`￼ if duplicate name is found
        primary = collection_from_df(dcm, out_dfs[0])
        try:
            series = primary.get("SeriesNumber")
        except ValueError:
            log.error(
                "Multiple SeriesNumbers found on primary split. "
                "Please split on SeriesNumber."
            )
            # Don't split if we find multiple SeriesNumbers here.
            return None
        name = SeriesName.gen_name(primary, series_number=series, group_by=group_by)
        log.info("Naming primary collection: %s", str(name))
        outputs[name] = primary
        if len(out_dfs) > 1:
            for i, out_df in enumerate(out_dfs[1:]):
                secondary = collection_from_df(dcm, out_df)
                try:
                    series = secondary.get("SeriesNumber")
                except ValueError:
                    log.error(
                        "Multiple SeriesNumbers found on secondary split."
                        " Please split on SeriesNumber."
                    )
                    # Don't split if we find multiple SeriesNumbers here.
                    return None
                name = SeriesName.gen_name(
                    secondary,
                    series_number=(series if series else str(i + 1000)),
                    group_by=group_by,
                )
                counter = 1
                while name in outputs:
                    name.number = counter
                    counter += 1
                log.info("Added secondary collection named: %s", str(name))
                outputs[name] = secondary
    elif len(outputs) == 0:
        log.info("Skipping group_by step.")
        # Add input to outputs dict to have localizer split
        try:
            series = dcm.get("SeriesNumber")
        except ValueError:
            log.error("Multiple SeriesNumbers found. Please split on SeriesNumber.")
            # Don't split if we find multiple SeriesNumbers here.
            return None
        name = SeriesName.gen_name(dcm, series_number=series, group_by=group_by)
        outputs[name] = dcm

    if len(outputs) > 1:
        # Generating unique attributes for the new grouped series
        # Don't generate new SeriesInstanceUID if groupby contains SeriesInstanceUID
        for name, collection in outputs.items():
            orig_series_uid = collection.get("SeriesInstanceUID")
            orig_series_num = name.series_number
            keep_suid = "SeriesInstanceUID" in group_by
            update_localizer_frames(
                collection, orig_series_uid, orig_series_num, keep_suid
            )

    if split_localizer and not geometric_split:
        # <dcm>.get() will raise ValueError if there are multiple unique values.
        #   let it raise here.
        localizer_outputs = {}
        for name, archive in outputs.items():
            # split_localizer only available for MR or CT modalities
            if archive.get("Modality") not in ["MR", "CT"]:
                log.info(
                    "Split localizer option is only applicable for MR or CT DICOMs. "
                    "%s DICOM modality is %s.",
                    name,
                    archive.get("Modality"),
                )
            else:
                log.info("Splitting collection %s", name)
                dicom, localizer = run_split_localizer(archive)
                localizer_outputs[name] = dicom
                if localizer and len(localizer) > 0:
                    log.info("Found %s localizer frame(s)", str(len(localizer)))
                    orig_series_uid = dicom.get("SeriesInstanceUID")
                    orig_series_num = name.series_number
                    new_series_num = update_localizer_frames(
                        localizer, orig_series_uid, orig_series_num, False
                    )
                    new_name = SeriesName.from_name(name)
                    new_name.series_number = new_series_num
                    new_name.localizer = True
                    localizer_outputs[new_name] = localizer
        outputs.update(localizer_outputs)

    return outputs


# Most of this function is already tested in fw_file
def run(
    dcm_path: Path,
    output_dir: Path,
    group_by: t.List[str],
    split_localizer: bool,
    zip_single: bool,
    max_geom_splits=-1,
) -> t.Tuple[t.Tuple[Path, ...], bool]:  # pragma: no cover
    """Main function of module.

    Args:
        dcm_path (Path): Dicom file path
        output_dir (Path): Gear output directory.
        group_by (t.List[str]): List of tags to split by.
        split_localizer (bool): Whether or not to split localizer out.
        zip_single (bool): Zip single dicom or not
        max_geom_splits(int): Maximum number of geometric splittings

    Returns:
        t.Tuple[Path]: Tuple of saved output paths.
        bool: Whether or not splitter completed successfully
    """
    if sniff_dcm(dcm_path):
        log.info("Input is a single DICOM, nothing to split. Exiting")
        return tuple(), True
    if not zipfile.is_zipfile(dcm_path):
        log.info("Not a zip file, nothing to split. Exiting")
        return tuple(), True
    with DICOMCollection.from_zip(dcm_path, force=True, stop_when=None) as dcm:
        suffix = ".dicom.zip"
        # Don't try to split if there is only one slice.
        if len(dcm) == 1:
            log.info("Only one slice present in archive.")
            return tuple(), True

        collections = split_dicom(dcm, group_by, split_localizer, max_geom_splits)
        # If collections = None, splitter encountered an error (see log)
        if not collections:
            log.info("Archive was not split due to an error.")
            return tuple(), False
        # If nothing was split out
        elif len(collections.items()) in (0, 1):
            log.info("Archive was not split; nothing to split was found.")
            # Return an empty tuple
            return tuple(), True
        # Otherwise populate output dir and return saved paths.
        save_paths = []
        for name, collection in collections.items():
            log.info(
                "Adding contributing equipment to collection: %s",
                str(name),
            )
            add_contributing_equipment(collection)

            if len(collection) > 1 or zip_single:
                # save and name
                save_path = output_dir / (str(name) + suffix)
                log.info(f"Saving {name} to {save_path}")
                save_paths.append(save_path)
                collection.to_zip(save_path)
            else:
                # remove .zip when only one slice in DICOMCollection
                suffix = suffix.replace(".zip", "")
                save_path = output_dir / (str(name) + suffix)
                log.info(f"Saving {name} to {save_path}")
                save_paths.append(save_path)
                collection[0].save(save_path)

        return tuple(save_paths), True
