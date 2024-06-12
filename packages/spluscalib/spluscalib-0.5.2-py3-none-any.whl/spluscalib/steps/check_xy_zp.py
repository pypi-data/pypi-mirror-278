# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                                check_xy_zp.py
#      Checks the homogeneity of the zero-points across the CCD
# ******************************************************************************

"""
Produces plots to check the homogeneity of the zero-points across the CCD

The S-PLUS field is given as the first command line argument. Configurations
are set in the config file, given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------
convert_calib_catalog_2_fits()
fix_XY_rotation()
compute_xycheck_maps()
plot_xy_check()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

Assumes that at least calibration_external.py, and possibly calibration_stloc.py
and calibration_internal.py, have already been run for this field.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 check_xy_zp.py *field_name* *config_file*

----------------
"""

################################################################################
# Import external packages

import os
import sys

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

    ############################################################################
    # Get directories

    field_path = os.path.join(conf['run_path'], field)

    suffix = ut.calibration_suffix(conf)
    calibration_path = os.path.join(field_path, f'Calibration_{suffix}')

    external_cal_path = os.path.join(calibration_path, 'external')
    stloc_cal_path = os.path.join(calibration_path, 'stlocus')
    internal_cal_path = os.path.join(calibration_path, 'internal')
    gaiascale_cal_path = os.path.join(calibration_path, 'gaiascale')
    xycheck_path = os.path.join(calibration_path, 'xycheck')
    xycheck_plots_path = os.path.join(calibration_path, 'xycheck', 'plots')

    photometry_path = os.path.join(field_path, 'Photometry')
    dual_path       = os.path.join(photometry_path, 'dual')
    detection_path  = os.path.join(dual_path, 'detection')
    single_path     = os.path.join(photometry_path, 'single')
    psf_path        = os.path.join(photometry_path, 'psf')



    log_path = os.path.join(calibration_path, 'logs')

    ############################################################################
    # Initiate log file

    ut.makedir(log_path)
    ut.makedir(xycheck_path)
    ut.makedir(xycheck_plots_path)

    log_file_name = os.path.join(log_path, 'check_xy_zp.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(calibration_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")


################################################################################
# Begin script


# ***************************************************
#    Convert catalogs to fits
# ***************************************************

def convert_calib_catalog_2_fits():
    """
    Converts catalogs from ascii to fits
    """

    print("")
    ut.printlog(('********** '
                 'Converting calib catalog to fits '
                 '**********'),
                log_file)
    print("")

    # Get final calibrated catalog
    if 'calibration_gaiascale' in conf['run_steps']:
        catalog_name = f"{field}_mag_gaiascale.cat"
        catalog_file = os.path.join(gaiascale_cal_path,
                                    catalog_name)

    elif 'calibration_internal' in conf['run_steps']:
        catalog_name = f"{field}_mag_int.cat"
        catalog_file = os.path.join(internal_cal_path,
                                    catalog_name)

    elif 'calibration_stloc' in conf['run_steps']:
        catalog_name = f"{field}_mag_stlocus.cat"
        catalog_file = os.path.join(stloc_cal_path,
                                    catalog_name)

    else:
        catalog_name = f"{field}_mag_ext.cat"
        catalog_file = os.path.join(external_cal_path,
                                    catalog_name)

    save_name = f'{field}_mag_final.fits'
    save_file = os.path.join(xycheck_path, save_name)

    if not os.path.exists(save_file):

        cmd = f"java -jar {conf['path_to_stilts']} tcopy "
        cmd += f"in={catalog_file} ifmt=ascii "
        cmd += f"out={save_file} ofmt=fits"

        ut.printlog(cmd, log_file)
        os.system(cmd)

    else:
        ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    convert_calib_catalog_2_fits()


# ***************************************************
#    fix X,Y rotation
# ***************************************************

def fix_XY_rotation():
    """
    Fixes XY rotation of S-PLUS images
    """

    print("")
    ut.printlog(('********** '
                 'Computing X_ALIGN, Y_ALIGN '
                 '**********'),
                log_file)
    print("")

    cat_name = f'{field}_mag_final.fits'
    cat_file = os.path.join(xycheck_path, cat_name)

    if conf['calibration_photometry'].lower() == "dual":
        transform_file = os.path.join(detection_path, 
                                      f"{field}_detection_x0y0l.csv")
        
    elif conf['calibration_photometry'].lower() == "single":
        transform_file = os.path.join(single_path, "catalogs", 
                                f"{field}_R_single_x0y0l.csv")
        
    elif conf['calibration_photometry'].lower() == "psf":
        transform_file = os.path.join(psf_path, "catalogs",
                                f"{field}_R_psf_x0y0l.csv")
        

    save_name = f'{field}_mag_final_xycorr.fits'
    save_file = os.path.join(xycheck_path, save_name)

    if not os.path.exists(save_file):

        ut.fix_xy_rotation(catalog=cat_file,
                           save_file=save_file,
                           transform_file=transform_file,
                           xcol = 'X', ycol = 'Y')

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    fix_XY_rotation()


# ***************************************************
#    Compute XY maps
# ***************************************************

def compute_xycheck_maps():
    """
    Computes XY-check maps
    """

    print("")
    ut.printlog(('********** '
                 'Computing XY-check maps '
                 '**********'),
                log_file)
    print("")

    cat_name = f'{field}_mag_final_xycorr.fits'
    cat_file = os.path.join(xycheck_path, cat_name)

    xbins = conf['XY_correction_xbins']
    ybins = conf['XY_correction_ybins']

    # For the check maps, use a 6x6 grid (less data/bin available)
    xbins[2] = 6
    ybins[2] = 6

    filters = conf["external_sed_pred"] + conf["gaiaxpsp_sed_pred"]
    mag_l_list = (conf["external_zp_fitting_mag_low"] +
                  conf["gaiaxpsp_zp_fitting_mag_low"])
    mag_u_list = (conf["external_zp_fitting_mag_up"] +
                  conf["gaiaxpsp_zp_fitting_mag_up"])

    for filt, mag_l, mag_u in zip(conf['filters'], mag_l_list, mag_u_list):

        mag_cut = [mag_l, mag_u]

        save_name = f"xy_check_{filt}.npy"
        save_file = os.path.join(xycheck_path, save_name)

        if not os.path.exists(save_file):

            ut.get_xy_check_grid(data_file=cat_file,
                                 save_file=save_file,
                                 mag=filt,
                                 xbins=xbins,
                                 ybins=ybins,
                                 mag_cut=mag_cut)

            ut.printlog(f"Created file {save_file}.", log_file)

        else:
            ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    compute_xycheck_maps()


# ***************************************************
#    Plot XY maps
# ***************************************************

def plot_xy_check():
    """
    Plots XY-check maps
    """

    print("")
    ut.printlog(('********** '
                 'Plotting XY-check maps '
                 '**********'),
                log_file)
    print("")

    for filt in conf['filters']:

        grid_name = f"xy_check_{filt}.npy"
        grid_file = os.path.join(xycheck_path, grid_name)

        save_name = f"xy_check_{filt}.png"
        save_file = os.path.join(xycheck_plots_path, save_name)

        xbins = conf['XY_correction_xbins']
        ybins = conf['XY_correction_ybins']

        # For the check maps, use a 6x6 grid (less data/bin available)
        xbins[2] = 6
        ybins[2] = 6

        if not os.path.exists(save_file):

            ut.plot_xy_correction_grid(grid_file=grid_file,
                                       save_file=save_file,
                                       mag=filt,
                                       xbins=xbins,
                                       ybins=ybins)

            ut.printlog(f"Created file {save_file}.", log_file)

        else:
            ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    plot_xy_check()
