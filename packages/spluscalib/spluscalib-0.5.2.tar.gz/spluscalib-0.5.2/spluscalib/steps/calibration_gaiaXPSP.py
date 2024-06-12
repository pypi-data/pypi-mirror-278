# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                            calibration_gaiaXPSP.py
#             Runs the gaia XPSP calibration step of the pipeline
# ******************************************************************************

"""
Obtains the gaia XPSP calibration zero-points by comparing the synthetic
magnitudes from gaiaxpy to S-PLUS instrumental magnitudes

The S-PLUS field is given as the first command line argument. Configurations
are set in the config file, given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

copy_splus_inst_gaiaXPSP_catalog()
get_gaiaxpsp_calib_zero_points()
add_gaiaxpsp_offset_to_splus_reference_calibration()
apply_gaiaxpsp_zero_points()
plot_gaiaxpsp_zp()
copy_splus_instrumental_catalog_to_xpsp_path()
apply_gaiaxpsp_zero_points_to_maginst()
crossmatch_gaiaxpsp_calib_and_all_references()
correct_extinction_crossmatched_gaiaxpsp_calib_catalog()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

Assumes that crossmatch.py has already been run for this field.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 calibration_gaiaXPSP.py *field_name* *config_file*

----------------
"""

################################################################################
# Import external packages

import os
import sys
import copy

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

    field     = sys.argv[1]
    config_file = sys.argv[2]

    conf = ut.pipeline_conf(config_file)

    try:
        print(conf['reference_catalog'])
    except KeyError:
        conf['reference_catalog'] = []

    if conf['reference_catalog'] == ['']:
        conf['reference_catalog'] = []

    ############################################################################
    # Get directories

    field_path      = os.path.join(conf['run_path'], field)
    crossmatch_path = os.path.join(field_path, 'Crossmatch')

    suffix = ut.calibration_suffix(conf)
    calibration_path   = os.path.join(field_path, f'Calibration_{suffix}')
    gaiaxpsp_cal_path  = os.path.join(calibration_path, 'gaiaXPSP')
    gaiaxpsp_plot_path = os.path.join(gaiaxpsp_cal_path, 'plots')

    log_path = os.path.join(calibration_path, 'logs')

    calib_phot = conf['calibration_photometry']

    ############################################################################
    # Initiate log file

    ut.makedir(calibration_path)
    ut.makedir(gaiaxpsp_cal_path)
    ut.makedir(gaiaxpsp_plot_path)
    ut.makedir(log_path)

    log_file_name = os.path.join(log_path, 'calibration_gaiaXPSP.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(calibration_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")

################################################################################
# Begin script

# ***************************************************
#    Copy instrumental magnitudes catalog
# ***************************************************

def copy_splus_inst_gaiaXPSP_catalog():

    """
    Copy S-PLUS instrumental magnitudes to gaiaXPSP calibration path
    """

    print("")
    ut.printlog(('********** '
                 'Copying Gaia XPSP + S-PLUS instrumental magnitudes catalog '
                 '**********'),
                 log_file)
    print("")

    cmatch_name = f'{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.fits'
    cmatch_file = os.path.join(crossmatch_path, cmatch_name)

    save_name = f'{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.cat'
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):

        cmd = f"java -jar {conf['path_to_stilts']} tcopy "
        cmd += f"in={cmatch_file} ifmt=fits "
        cmd += f"out={save_file} ofmt=ascii"
        ut.printlog(cmd, log_file)
        os.system(cmd)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    copy_splus_inst_gaiaXPSP_catalog()


# ***************************************************
#    Get external calibration zero points
# ***************************************************

def get_gaiaxpsp_calib_zero_points():

    """
    Obtains the gaia XPSP calibration zero-points
    """

    print("")
    ut.printlog(('********** '
                 'Getting gaia XPSP calibration ZPs '
                 '**********'),
                 log_file)
    print("")

    catalog_name = f'{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.cat'
    catalog_file = os.path.join(gaiaxpsp_cal_path, catalog_name)

    save_name = f"{field}_gaiaxpsp_tmp.zp"
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):
        ut.zp_estimate(catalog = catalog_file,
                       save_file = save_file,
                       filters_list = conf['gaiaxpsp_sed_pred'],
                       mag_low = conf['gaiaxpsp_zp_fitting_mag_low'],
                       mag_up = conf['gaiaxpsp_zp_fitting_mag_up'],
                       gaiaXPSP = True)

        ut.printlog(f"Created zp file {save_file}", log_file)

    else:
        ut.printlog(f"ZP file {save_name} already exists", log_file)


if __name__ == "__main__":
    get_gaiaxpsp_calib_zero_points()


# ***************************************************
#    Add offset to S-PLUS reference calibration
# ***************************************************

def add_gaiaxpsp_offset_to_splus_reference_calibration():

    """
    Adds offset to S-PLUS reference calibration
    """

    if conf['offset_include_after'].lower() == "gaiaXPSP":
        print("")
        ut.printlog(('********** '
                     'Adding offset to S-PLUS reference calibration '
                     '**********'),
                     log_file)
        print("")

    gaiaxpsp_zp_name = f"{field}_gaiaxpsp_tmp.zp"
    gaiaxpsp_zp_file = os.path.join(gaiaxpsp_cal_path, gaiaxpsp_zp_name)

    save_name = f"{field}_gaiaxpsp.zp"
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):

        if conf['offset_include_after'].lower() == "gaiaxpsp":
            offset_zp_name = f'offset_refcalib.zp'
            offset_zp_file = os.path.join(gaiaxpsp_cal_path, offset_zp_name)

            cmd = f"cp {conf['offset_to_splus_refcalib']} {offset_zp_file}"
            ut.printlog(cmd, log_file)
            os.system(cmd)

            zp_file_list = [gaiaxpsp_zp_file, offset_zp_file]

            filters = []
            for filt in conf['filters']:
                filters.append(f"SPLUS_{filt}")

            # Combine zero-points
            ut.zp_add(zp_file_list=zp_file_list,
                      save_file=save_file,
                      filters=filters,
                      inst_zp=0)

        else:
            cmd = f"cp {gaiaxpsp_zp_file} {save_file}"
            os.system(cmd)

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"File {save_name} already exists", log_file)


if __name__ == "__main__":
    add_gaiaxpsp_offset_to_splus_reference_calibration()

# ***************************************************
#    Apply Zero Points
# ***************************************************


def apply_gaiaxpsp_zero_points():

    """
    Applies gaiaxpsp zero-points to mag_inst catalog
    """

    print("")
    ut.printlog(('********** '
                 'Applying gaiaxpsp zero-points to mag_inst gaia XPSP catalog '
                 '**********'),
                 log_file)
    print("")

    catalog_name = f'{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.cat'
    catalog_file = os.path.join(gaiaxpsp_cal_path, catalog_name)

    zp_name = f"{field}_gaiaxpsp.zp"
    zp_file = os.path.join(gaiaxpsp_cal_path, zp_name)

    save_name = f"{field}_mag_gaiaxpsp.cat"
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):
        ut.zp_apply(catalog   = catalog_file,
                    save_file = save_file,
                    zp_file   = zp_file)

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    apply_gaiaxpsp_zero_points()


# ***************************************************
#          Plot gaiaXPSP ZPs fitting
# ***************************************************

def plot_gaiaxpsp_zp():

    """
    Makes diagnostic plots of the external zp fitting process
    """

    print("")
    ut.printlog(('********** '
                 'Plotting gaiaxpsp zp-fitting process '
                 '**********'),
                 log_file)
    print("")

    catalog_name = f'{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.cat'
    catalog_file = os.path.join(gaiaxpsp_cal_path, catalog_name)

    zp_name = f"{field}_gaiaxpsp.zp"
    zp_file = os.path.join(gaiaxpsp_cal_path, zp_name)

    for filt, mag_l, mag_u in zip(conf['gaiaxpsp_sed_pred'],
                                  conf['gaiaxpsp_zp_fitting_mag_low'],
                                  conf['gaiaxpsp_zp_fitting_mag_up']):

        mag_cut = [mag_l, mag_u]

        save_name = f"{field}_{filt}_gaiaxpsp.png"
        save_file = os.path.join(gaiaxpsp_plot_path, save_name)

        if not os.path.exists(save_file):
            ut.plot_zp_fitting(sed_fit_file = catalog_file,
                               zp_file      = zp_file,
                               save_file    = save_file,
                               filt         = filt,
                               mag_cut      = mag_cut,
                               gaiaXPSP     = True)

            ut.printlog(f"Saved plot {save_file}", log_file)

        else:
            ut.printlog(f"Plot {save_name} already made", log_file)


if __name__ == "__main__":
    plot_gaiaxpsp_zp()


# ***************************************************
#    Copying all mag inst catalog
# ***************************************************

def copy_splus_instrumental_catalog_to_xpsp_path():

    """
    Copy S-PLUS instrumental magnitudes to xpsp calibration path
    """

    print("")
    ut.printlog(('********** '
                 'Copying S-PLUS instrumental magnitudes catalog to xpsp path '
                 '**********'),
                 log_file)
    print("")

    cmatch_name = f'{field}_SPLUS_{calib_phot}.fits'
    cmatch_file = os.path.join(crossmatch_path, cmatch_name)

    save_name = f'{field}_SPLUS_{calib_phot}.cat'
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):

        cmd = f"java -jar {conf['path_to_stilts']} tcopy "
        cmd += f"in={cmatch_file} ifmt=fits "
        cmd += f"out={save_file} ofmt=ascii"
        ut.printlog(cmd, log_file)
        os.system(cmd)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    copy_splus_instrumental_catalog_to_xpsp_path()

# ***************************************************
#    Apply Zero Points to all mag inst
# ***************************************************


def apply_gaiaxpsp_zero_points_to_maginst():

    """
    Applies gaiaxpsp zero-points to mag_inst catalog
    """

    print("")
    ut.printlog(('********** '
                 'Applying gaiaxpsp zero-points to mag_inst catalog '
                 '**********'),
                 log_file)
    print("")

    catalog_name = f'{field}_SPLUS_{calib_phot}.cat'
    catalog_file = os.path.join(gaiaxpsp_cal_path, catalog_name)

    zp_name = f"{field}_gaiaxpsp.zp"
    zp_file = os.path.join(gaiaxpsp_cal_path, zp_name)

    save_name = f"{field}_mag_gaiaxpsp_all.cat"
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):
        ut.zp_apply(catalog   = catalog_file,
                    save_file = save_file,
                    zp_file   = zp_file)

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    apply_gaiaxpsp_zero_points_to_maginst()


# ***************************************************
#       Crossmatch with reference catalog
# ***************************************************

def crossmatch_gaiaxpsp_calib_and_all_references():
    """
    Combines S-PLUS after gaiaxpsp calib and reference catalogs
    """

    print("")
    ut.printlog(('********** '
                 'Crossmatching S-PLUS after gaiaxpsp to reference catalogs '
                 '**********'),
                log_file)
    print("")

    # Get number of reference catalogs
    nref = len(conf['reference_catalog'])

    # Include S-PLUS catalog in the tmatchn
    splus_cat = f"{field}_mag_gaiaxpsp_all.cat"
    splus_cat_file = os.path.join(gaiaxpsp_cal_path, splus_cat)

    # Include GAIA
    if conf["gaia_reference"].lower() == "dr3":
        gaia_cat = f'{field}_GAIADR3.fits'
    else:
        gaia_cat = f'{field}_GAIADR2.fits'

    gaia_cat_file = os.path.join(crossmatch_path, gaia_cat)

    # Start save name
    save_name = ut.crossmatch_catalog_name(field, conf, gaiaXPSP=True)
    save_file = os.path.join(gaiaxpsp_cal_path, save_name)

    if not os.path.exists(save_file):

        # Start tmatchn cmd
        cmd = f"java -jar {conf['path_to_stilts']} tmatchn "
        cmd += f"nin={nref + 2} "

        cmd += f"ifmt1=ascii in1={splus_cat_file} "
        cmd += f"values1='RAJ2000 DEJ2000' join1=match "

        cmd += f"ifmt2=fits in2={gaia_cat_file} "

        if conf["gaia_reference"].lower() == "dr3":
            cmd += f"values2='GAIADR3_RAJ2000 GAIADR3_DEJ2000' join2=match "
        else:
            cmd += f"values2='GAIADR2_RAJ2000 GAIADR2_DEJ2000' join2=match "

        for i in range(nref):
            ref = conf['reference_catalog'][i]

            ref_cat = f'{field}_{ref}.fits'
            ref_cat_file = os.path.join(crossmatch_path, ref_cat)

            values = f"{ref}_RAJ2000 {ref}_DEJ2000"
            cmd += f"ifmt{i + 3}=fits in{i + 3}={ref_cat_file} "
            cmd += f"values{i + 3}='{values}' join{i + 3}=match "

        cmd += f"out={save_file} ofmt=fits "
        cmd += f"matcher=sky params=3 multimode=group "

        ut.printlog(cmd, log_file)
        os.system(cmd)

        ut.printlog(f"Created catalog {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    try:
        print(conf["reference_catalog"])
        crossmatch_gaiaxpsp_calib_and_all_references()
    except KeyError:
        pass


# ***************************************************
#    Correct extinction
# ***************************************************

def correct_extinction_crossmatched_gaiaxpsp_calib_catalog():
    """
    Generates crossmatched catalog with extinction correction
    """

    print("")
    ut.printlog(('********** '
                 'Applying exctinction correction '
                 '**********'),
                log_file)
    print("")

    ###############################
    # Get crossmatched catalog file
    cmatch_name = ut.crossmatch_catalog_name(field, conf, gaiaXPSP=True)
    cmatch_file = os.path.join(gaiaxpsp_cal_path, cmatch_name)

    ##################
    # Apply correction
    correction = conf['extinction_correction']
    ebv_map_path = conf['extinction_maps_path']

    save_file = cmatch_file.replace(".fits",
                                    f"_ebvcorr_{correction}.fits")

    save_ebv_file = save_file.replace("ebvcorr", "radecebv")
    save_ebv_file = save_ebv_file.replace(".fits", ".csv")

    if not os.path.exists(save_file) or not os.path.exists(save_ebv_file):
        ut.correct_extinction(catalog=cmatch_file,
                              save_file=save_file,
                              correction=correction,
                              ebv_maps_path=ebv_map_path,
                              save_EBV=True,
                              save_EBV_file=save_ebv_file)

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Extinction corrected catalog already exists",
                    log_file)


if __name__ == "__main__":
    if conf['extinction_correction'].lower() != 'none':
        try:
            print(conf["reference_catalog"])
            correct_extinction_crossmatched_gaiaxpsp_calib_catalog()
        except KeyError:
            pass