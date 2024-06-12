# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                                final_checks.py
#                Checks files produced by the calibration pipeline
# ******************************************************************************

"""
This scripts checks for the final files of each step to determine which steps
have already been run for a given field

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 final_checks.py *field_name* *config_file*

"""

################################################################################
# Import external packages

import os
import sys
import warnings
import pandas as pd
import numpy as np

steps_path = os.path.split(__file__)[0]
pipeline_path = os.path.split(steps_path)[0]
spluscalib_path = os.path.split(pipeline_path)[0]

sys.path.append(spluscalib_path)

################################################################################
# Import spluscalib packages

from spluscalib import utils as ut

if __name__ == "__main__":
    ############################################################################
    # Read parameters

    field = sys.argv[1]
    config_file = sys.argv[2]

    conf = ut.pipeline_conf(config_file)

    calib_phot = conf["calibration_photometry"]

    ############################################################################
    # Get directories

    field_path              = os.path.join(conf['run_path'], field)

    # images
    images_path             = os.path.join(field_path, 'Images')
    headers_path            = os.path.join(images_path, 'headers')

    # dual-mode phot
    photometry_path         = os.path.join(field_path, 'Photometry')

    dual_path               = os.path.join(photometry_path, 'dual')
    dual_sexcatalogs_path   = os.path.join(dual_path, 'catalogs')

    res_path               = os.path.join(photometry_path, 'res')
    res_sexcatalogs_path   = os.path.join(res_path, 'catalogs')

    # single-mode phot
    single_path             = os.path.join(photometry_path, 'single')
    single_sexcatalogs_path = os.path.join(single_path, 'catalogs')

    # psf phot
    psf_path                = os.path.join(photometry_path, 'psf')
    psf_dophotcatalogs_path = os.path.join(psf_path, 'catalogs')

    # Crossmatch
    crossmatch_path         = os.path.join(field_path, 'Crossmatch')

    # Calibration
    suffix                  = ut.calibration_suffix(conf)
    calibration_path        = os.path.join(field_path, f'Calibration_{suffix}')

    # XPSP
    gaiaxpsp_cal_path       = os.path.join(calibration_path, 'gaiaXPSP')

    # SED-fittig
    sedfit_cal_path         = os.path.join(calibration_path, 'external')

    # gaiascale
    gaiascale_cal_path      = os.path.join(calibration_path, 'gaiascale')

    # Final Catalogs
    dual_catalogs_path      = os.path.join(calibration_path, field, "dual")
    single_catalogs_path    = os.path.join(calibration_path, field, "single")
    psf_catalogs_path       = os.path.join(calibration_path, field, "psf")

    ############################################################################
    # Create checks dict

    checks_dict = {}

    checks_dict["Field"] = field
    checks_dict["Calib"] = suffix
    checks_dict["Reduction"] = conf["reduction"]
    checks_dict["Calib_phot"] = calib_phot

    checks_dict["Check_timestap"] = ut.get_current_time()

    ############################################################################
    # Get field RA, DEC

    try:
        filt_image_hdr_file = os.path.join(headers_path, 
                                        f"{field}_R_swp.header")
        
        filt_image_hdr = ut.read_hdr_file(filt_image_hdr_file)

        checks_dict["RAdeg_R"] = filt_image_hdr["CRVAL1"]
        checks_dict["DECdeg_R"] = filt_image_hdr["CRVAL2"]
    except FileNotFoundError:
        checks_dict["RAdeg_R"] = np.nan
        checks_dict["DECdeg_R"] = np.nan

    ############################################################################
    # Image checks

    for filt in conf["filters"]:
        filt_image_hdr_file = os.path.join(headers_path, 
                                        f"{field}_{filt}_swp.header")
        
        filt_image_hdr = ut.read_hdr_file(filt_image_hdr_file)

        try:
            checks_dict[f"{filt}_CHECKSUM"] = filt_image_hdr["CHECKSUM"].replace("'", "")
            checks_dict[f"{filt}_DATASUM"]  = int(filt_image_hdr["DATASUM"].replace("'", ""))
        except FileNotFoundError:
            checks_dict[f"{filt}_CHECKSUM"] = np.nan
            checks_dict[f"{filt}_DATASUM"]  = np.nan

        # Weights
        filt_wimage_hdr_file = os.path.join(headers_path, 
                                        f"{field}_{filt}_swpweight.header")
        
        filt_wimage_hdr = ut.read_hdr_file(filt_wimage_hdr_file)

        try:
            checks_dict[f"{filt}weight_CHECKSUM"] = filt_wimage_hdr["CHECKSUM"].replace("'", "")
            checks_dict[f"{filt}weight_DATASUM"]  = int(filt_wimage_hdr["DATASUM"].replace("'", ""))
        except FileNotFoundError:
            checks_dict[f"{filt}weight_CHECKSUM"] = np.nan
            checks_dict[f"{filt}weight_DATASUM"]  = np.nan

    ############################################################################
    # dual-mode Photometry checks

    sexphotdual_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_sexphotdual = os.path.join(dual_sexcatalogs_path, 
                                        f"sex_{field}_{filt}_dual.fits")

        try:
            checks_dict[f"{filt}_SExPhotDual__ctime"] = ut.get_creation_time(filt_sexphotdual)
            checks_dict[f"{filt}_SExPhotDual__size"]  = ut.get_file_size(filt_sexphotdual)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_SExPhotDual__ctime"] = np.nan
            checks_dict[f"{filt}_SExPhotDual__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            sexphotdual_status = "Not-complete"
        else:
            sexphotdual_status = "Not-started"

    checks_dict[f"SExPhotDual__status"] = sexphotdual_status


    ############################################################################
    # restricted-mode Photometry checks

    sexphotres_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_sexphotres = os.path.join(res_sexcatalogs_path, 
                                       f"sex_{field}_{filt}_res.fits")

        try:
            checks_dict[f"{filt}_SExPhotRes__ctime"] = ut.get_creation_time(filt_sexphotres)
            checks_dict[f"{filt}_SExPhotRes__size"]  = ut.get_file_size(filt_sexphotres)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_SExPhotDual__ctime"] = np.nan
            checks_dict[f"{filt}_SExPhotDual__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            sexphotres_status = "Not-complete"
        else:
            sexphotres_status = "Not-started"

    checks_dict[f"SExPhotRes__status"] = sexphotdual_status


    ############################################################################
    # single-mode Photometry checks 

    sexphotsingle_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_sexphotsingle = os.path.join(single_sexcatalogs_path, 
                                        f"sex_{field}_{filt}_single.fits")

        try:
            checks_dict[f"{filt}_SExPhotSingle__ctime"] = ut.get_creation_time(filt_sexphotsingle)
            checks_dict[f"{filt}_SExPhotSingle__size"]  = ut.get_file_size(filt_sexphotsingle)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_SExPhotSingle__ctime"] = np.nan
            checks_dict[f"{filt}_SExPhotSingle__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            sexphotsingle_status = "Not-complete"
        else:
            sexphotsingle_status = "Not-started"

    checks_dict[f"SExPhotSingle__status"] = sexphotsingle_status


    ############################################################################
    # psf Photometry checks

    psfphot_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_psfphot = os.path.join(psf_dophotcatalogs_path, 
                                    f"{field}_{filt}_psf.cat")

        try:
            checks_dict[f"{filt}_PSFphot__ctime"] = ut.get_creation_time(filt_psfphot)
            checks_dict[f"{filt}_PSFphot__size"]  = ut.get_file_size(filt_psfphot)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_PSFphot__ctime"] = np.nan
            checks_dict[f"{filt}_PSFphot__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            psfphot_status = "Not-complete"
        else:
            psfphot_status = "Not-started"

    checks_dict[f"PSFphot__status"] = psfphot_status

    ############################################################################
    # Check if it is possible to ensure the same fits images have been used

    has_any_phot = psfphot_status == "Complete"
    has_any_phot = has_any_phot or (psfphot_status == "Not-Complete")
    has_any_phot = has_any_phot or (sexphotsingle_status == "Complete")
    has_any_phot = has_any_phot or (sexphotsingle_status == "Not-Complete")
    has_any_phot = has_any_phot or (sexphotdual_status == "Complete")
    has_any_phot = has_any_phot or (sexphotdual_status == "Not-Complete")

    if has_any_phot:
        checkable_warning_file = os.path.join(images_path,
                                        "warning.warn")
        if os.path.exists(checkable_warning_file):
            image_checkable = False
        else:
            image_checkable = True
    else:
        image_checkable = True

    checks_dict[f"fits_are_checkable"] = image_checkable

    ############################################################################
    # Crossmatch checks

    count = 0

    # Check for GAIADR3
    xmatch_gaiaDR3 = os.path.join(crossmatch_path, 
                                f"{field}_SPLUS_{calib_phot}_GAIADR3.fits")
    try:
        checks_dict[f"GAIADR3xmatch__ctime"] = ut.get_creation_time(xmatch_gaiaDR3)
        checks_dict[f"GAIADR3xmatch__size"]  = ut.get_file_size(xmatch_gaiaDR3)
        count += 1
    except FileNotFoundError:
        checks_dict[f"GAIADR3xmatch__ctime"] = np.nan
        checks_dict[f"GAIADR3xmatch__size"]  = np.nan

    # Check for XPSP
    xmatch_XPSP = os.path.join(crossmatch_path, 
                                f"{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.fits")
    try:
        checks_dict[f"XPSPxmatch__ctime"] = ut.get_creation_time(xmatch_XPSP)
        checks_dict[f"XPSPxmatch__size"]  = ut.get_file_size(xmatch_XPSP)
        count += 1
    except FileNotFoundError:
        checks_dict[f"XPSPxmatch__ctime"] = np.nan
        checks_dict[f"XPSPxmatch__size"]  = np.nan

    if count == 2:
        xmatch_status = "Complete"
    elif count == 1:
        xmatch_status = "Not-complete"
    elif count == 0:
        xmatch_status = "Not-started"

    checks_dict[f"Xmatch__status"] = xmatch_status

    ############################################################################
    # Calibration XPSP

    xpsp_zp = os.path.join(gaiaxpsp_cal_path, 
                        f"{field}_gaiaxpsp.zp")

    try:
        checks_dict[f"ZP_XPSP__ctime"] = ut.get_creation_time(xpsp_zp)
        checks_dict[f"ZP_XPSP__size"]  = ut.get_file_size(xpsp_zp)
        xpsp_zp_status = "Found"
    except FileNotFoundError:
        checks_dict[f"ZP_XPSP__ctime"] = np.nan
        checks_dict[f"ZP_XPSP__size"]  = np.nan
        xpsp_zp_status = "Not Found"

    checks_dict[f"ZP_XPSP__status"] = xpsp_zp_status

    ############################################################################
    # Calibration sed-fitting

    sedfit_zp = os.path.join(sedfit_cal_path, 
                        f"{field}_external.zp")

    try:
        checks_dict[f"ZP_SEDfit__ctime"] = ut.get_creation_time(sedfit_zp)
        checks_dict[f"ZP_SEDfit__size"]  = ut.get_file_size(sedfit_zp)
        sedfit_zp_status = "Found"
    except FileNotFoundError:
        checks_dict[f"ZP_SEDfit__ctime"] = np.nan
        checks_dict[f"ZP_SEDfit__size"]  = np.nan
        sedfit_zp_status = "Not Found"

    checks_dict[f"ZP_SEDfit__status"] = sedfit_zp_status


    ############################################################################
    # Calibration final ZP

    final_zp = os.path.join(calibration_path, 
                        f"{field}_final.zp")

    try:
        checks_dict[f"ZP_final__ctime"] = ut.get_creation_time(final_zp)
        checks_dict[f"ZP_finalt__size"]  = ut.get_file_size(final_zp)
        final_zp_status = "Found"
    except FileNotFoundError:
        checks_dict[f"ZP_final__ctime"] = np.nan
        checks_dict[f"ZP_finalt__size"]  = np.nan
        final_zp_status = "Not Found"

    checks_dict[f"ZP_final__status"] = final_zp_status


    ############################################################################
    # gaia-scale check

    gaiascale_zp = os.path.join(gaiascale_cal_path, 
                        f"{field}_gaiascale_gaia.zp")

    try:
        checks_dict[f"ZP_gaiascale__ctime"] = ut.get_creation_time(gaiascale_zp)
        checks_dict[f"ZP_gaiascale__size"]  = ut.get_file_size(gaiascale_zp)
        gaiascale_zp_status = "Found"
    except FileNotFoundError:
        checks_dict[f"ZP_gaiascale__ctime"] = np.nan
        checks_dict[f"ZP_gaiascale__size"]  = np.nan
        gaiascale_zp_status = "Not Found"

    checks_dict[f"ZP_gaiascale__status"] = gaiascale_zp_status

    ############################################################################
    # mosaic plot

    mosaic_plot = os.path.join(calibration_path, 
                        f"{field}_{suffix}_mosaic_v3.png")

    try:
        checks_dict[f"MosaicPlot__ctime"] = ut.get_creation_time(mosaic_plot)
        checks_dict[f"MosaicPlot__size"]  = ut.get_file_size(mosaic_plot)
        mosaic_status = "Found"
    except FileNotFoundError:
        checks_dict[f"MosaicPlot__ctime"] = np.nan
        checks_dict[f"MosaicPlot__size"]  = np.nan
        mosaic_status = "Not Found"

    checks_dict[f"MosaicPlot__status"] = mosaic_status

    ############################################################################
    # Final Dual Catalogs

    catdual_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_catdual = os.path.join(dual_catalogs_path, 
                                    f"{field}_{filt}_dual.fits")

        try:
            checks_dict[f"{filt}_CatDual__ctime"] = ut.get_creation_time(filt_catdual)
            checks_dict[f"{filt}_CatDual__size"]  = ut.get_file_size(filt_catdual)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_CatDual__ctime"] = np.nan
            checks_dict[f"{filt}_CatDual__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            catdual_status = "Not-complete"
        else:
            catdual_status = "Not-started"

    checks_dict[f"CatDual__status"] = catdual_status


    ############################################################################
    # Final Single Catalogs

    catsingle_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_catsingle = os.path.join(single_catalogs_path, 
                                    f"{field}_{filt}_single.fits")

        try:
            checks_dict[f"{filt}_CatSingle__ctime"] = ut.get_creation_time(filt_catsingle)
            checks_dict[f"{filt}_CatSingle__size"]  = ut.get_file_size(filt_catsingle)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_CatSingle__ctime"] = np.nan
            checks_dict[f"{filt}_CatSingle__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            catsingle_status = "Not-complete"
        else:
            catsingle_status = "Not-started"

    checks_dict[f"CatSingle__status"] = catsingle_status


    ############################################################################
    # Final PSF Catalogs

    catpsf_status = "Complete"

    count = 0

    for filt in conf["filters"]:
        filt_catpsf = os.path.join(psf_catalogs_path, 
                                    f"{field}_{filt}_psf.fits")

        try:
            checks_dict[f"{filt}_CatPSF__ctime"] = ut.get_creation_time(filt_catpsf)
            checks_dict[f"{filt}_CatPSF__size"]  = ut.get_file_size(filt_catpsf)
            count += 1
        except FileNotFoundError:
            checks_dict[f"{filt}_CatPSF__ctime"] = np.nan
            checks_dict[f"{filt}_CatPSF__size"]  = np.nan
        
    if count < len(conf["filters"]):
        if count > 1:
            catpsf_status = "Not-complete"
        else:
            catpsf_status = "Not-started"

    checks_dict[f"CatPSF__status"] = catpsf_status


    ############################################################################
    # Save checks df

    tmp_df = pd.DataFrame()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for key, value in checks_dict.items():
            tmp_df[key] = [value]

    # Save full df
    output_df_full = os.path.join(calibration_path,
                                "checks_full.csv")

    checks_df = tmp_df.copy()
    checks_df.to_csv(output_df_full, index = False)

    # Save summary
    output_df_summary = os.path.join(calibration_path,
                                "checks_summary.csv")

    summary_cols = ["Field", "Calib", "fits_are_checkable", 
                    "SExPhotDual__status", "SExPhotRes__status",
                    "SExPhotSingle__status", "PSFphot__status", 
                    "Xmatch__status", "ZP_XPSP__status", "ZP_final__status", 
                    "ZP_gaiascale__status", "MosaicPlot__status", 
                    "CatDual__status", "CatSingle__status", "CatPSF__status"]

    checks_summary_df = checks_df.loc[:,summary_cols]
    checks_summary_df.to_csv(output_df_summary, index = False)