import numpy as np
from astropy.io import fits
from dkist_processing_common.codecs.fits import fits_array_decoder
from dkist_processing_common.codecs.fits import fits_hdulist_encoder
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_math.statistics import average_numpy_arrays
from dkist_service_configuration.logging import logger

from dkist_processing_dlnirsp.models.constants import DlnirspBudName
from dkist_processing_dlnirsp.models.tags import DlnirspTag
from dkist_processing_dlnirsp.tasks.dlnirsp_base import DlnirspTaskBase
from dkist_processing_dlnirsp.tasks.mixin.intermediate_frame_helpers import (
    IntermediateFrameHelpersMixin,
)


class SetObserveWavelength(WorkflowTaskBase):
    def run(self):
        self.constants._update({DlnirspBudName.wavelength.value: 1083.0})


class SetSolarGainExpTime(WorkflowTaskBase):
    def run(self):
        self.constants._update({DlnirspBudName.solar_gain_exposure_times.value: []})


class SetPolcalExpTime(WorkflowTaskBase):
    def run(self):
        self.constants._update({DlnirspBudName.polcal_exposure_times.value: []})


class SetObserveExpTime(DlnirspTaskBase):
    def run(self):
        if self.constants.correct_for_polarization:
            dummy_value = self.constants.polcal_exposure_times
        else:
            dummy_value = self.constants.solar_gain_exposure_times

        self.constants._update({DlnirspBudName.observe_exposure_times.value: dummy_value})


class ForceIntensityOnly(WorkflowTaskBase):
    def run(self) -> None:
        try:
            del self.constants._db_dict[DlnirspBudName.polarimeter_mode.value]
        except KeyError:
            pass

        self.constants._update({DlnirspBudName.polarimeter_mode.value: "Stokes I"})


class InsertDemodMatrices(WorkflowTaskBase, IntermediateFrameHelpersMixin):
    def run(self):
        # "Dmat" for cam2 from "test_reduce_pore.ipynb
        raw_data_from_SJ = np.array(
            [
                [0.15947, 0.11047, 0.09053, 0.13953, 0.15947, 0.11047, 0.09053, 0.13953],
                [0.20454, 0.28906, -0.20454, -0.28906, 0.20454, 0.28906, -0.20454, -0.28906],
                [-0.28906, 0.20454, 0.28906, -0.20454, -0.28906, 0.20454, 0.28906, -0.20454],
                [-0.30109, -0.16633, 0.06587, 0.25948, 0.30109, 0.16633, -0.06587, -0.25948],
            ]
        )

        self.intermediate_frame_helpers_write_arrays(arrays=raw_data_from_SJ, task="DEMOD_MATRICES")


class TagPolcasAsScience(DlnirspTaskBase):
    """Do."""

    def run(self) -> None:
        """Do."""
        for cs_step in range(self.constants.num_cs_steps):
            for modstate in range(1, self.constants.num_modstates + 1):
                tags = [
                    DlnirspTag.task("POLCAL"),
                    DlnirspTag.cs_step(cs_step),
                    DlnirspTag.modstate(modstate),
                ]
                file_list = list(self.read(tags=tags))
                first_hdul = fits.open(file_list[0])
                idx = 1 if first_hdul[0].data is None else 0
                first_header = first_hdul[idx].header
                logger.info(
                    f"{cs_step = } and {modstate = } has {len(file_list)} files that will be averaged"
                )
                arrays = self.read(tags=tags, decoder=fits_array_decoder)
                avg_array = average_numpy_arrays(arrays=arrays)

                hdul = fits.HDUList([fits.PrimaryHDU(data=avg_array, header=first_header)])
                hdul[0].header["DLCSTPX"] = 0
                hdul[0].header["DLCSTPY"] = 0
                hdul[0].header["DLMOSNRP"] = self.constants.num_cs_steps
                hdul[0].header["DLCURMOS"] = cs_step

                new_tags = [
                    DlnirspTag.task("OBSERVE"),
                    DlnirspTag.mosaic_num(cs_step),
                    DlnirspTag.tile_X_num(0),
                    DlnirspTag.tile_Y_num(0),
                    DlnirspTag.frame(),
                    DlnirspTag.modstate(modstate),
                    DlnirspTag.linearized(),
                    DlnirspTag.exposure_time(self.constants.polcal_exposure_times[0]),
                ]
                file_name = self.write(data=hdul, tags=new_tags, encoder=fits_hdulist_encoder)
                final_tags = self.tags(self.scratch.workflow_base_path / file_name)
                logger.info(f"after re-tagging tags for {str(file_name) = } are {final_tags}")

        # Now update the num[mosaic, X_tile] constants. We'll call each CS step a "map"
        self.constants._update(
            {
                DlnirspBudName.num_spatial_steps_X.value: 1,
                DlnirspBudName.num_spatial_steps_Y.value: 1,
                DlnirspBudName.num_mosaic_repeats.value: self.constants.num_cs_steps,
            }
        )


class TagSingleSolarGainAsScience(DlnirspTaskBase):
    """Do."""

    def run(self) -> None:
        """Do."""
        tags = [
            DlnirspTag.task("SOLAR_GAIN"),
        ]
        file_list = list(self.read(tags=tags))
        first_hdul = fits.open(file_list[0])
        idx = 1 if first_hdul[0].data is None else 0
        first_header = first_hdul[idx].header
        logger.info(f"Averaging {len(file_list)} files")
        arrays = self.read(tags=tags, decoder=fits_array_decoder)
        avg_array = average_numpy_arrays(arrays=arrays)

        hdul = fits.HDUList([fits.PrimaryHDU(data=avg_array, header=first_header)])
        hdul[0].header["DLCSTPX"] = 0
        hdul[0].header["DLCSTPY"] = 0
        hdul[0].header["DLMOSNRP"] = 1
        hdul[0].header["DLCURMOS"] = 0

        new_tags = [
            DlnirspTag.task("OBSERVE"),
            DlnirspTag.mosaic_num(0),
            DlnirspTag.tile_X_num(0),
            DlnirspTag.tile_Y_num(0),
            DlnirspTag.frame(),
            DlnirspTag.modstate(1),
            DlnirspTag.linearized(),
            DlnirspTag.exposure_time(self.constants.solar_gain_exposure_times[0]),
        ]
        file_name = self.write(data=hdul, tags=new_tags, encoder=fits_hdulist_encoder)
        final_tags = self.tags(self.scratch.workflow_base_path / file_name)
        logger.info(f"after re-tagging tags for {str(file_name) = } are {final_tags}")

        del self.constants._db_dict[DlnirspBudName.polarimeter_mode.value]
        self.constants._update(
            {
                DlnirspBudName.num_spatial_steps_X.value: 1,
                DlnirspBudName.num_spatial_steps_Y.value: 1,
                DlnirspBudName.num_mosaic_repeats.value: 1,
                DlnirspBudName.polarimeter_mode.value: "None",
            }
        )
