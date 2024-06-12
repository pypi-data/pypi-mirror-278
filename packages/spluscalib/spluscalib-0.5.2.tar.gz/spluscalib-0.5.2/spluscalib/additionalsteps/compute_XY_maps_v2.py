# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                        compute_XY_correction_maps_v2.py
#      Computes XY zero-points offsets in relation to the reference catalog
# ******************************************************************************

"""
Computes XY zero-points offsets in relation to the reference catalog

Command line arguments for this script are, respectivelly:
1) Location of the S-PLUS fields list file
2) Location of the configuration file used in the calibration
3) Location to save the intermediary calibration catalogs
4) Number of bins in the x-axis
5) Number of bins in the y-axis

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

convert_2_fits()
fix_XY_rotation()
concatenate_calib_catalogs()
compute_xy_maps()
plot_xy_maps()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
This script should be run individually and not within the pipeline.py script

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 compute_XY_correction_maps_v2.py *field_list_file* *config_file* *save_path* nx ny

----------------
"""

################################################################################
# Import external packages

import os
import sys

addsteps_path = os.path.split(__file__)[0]
pipeline_path = os.path.split(addsteps_path)[0]
spluscalib_path = os.path.split(pipeline_path)[0]

sys.path.append(spluscalib_path)

################################################################################
# Import spluscalib packages

from spluscalib import utils as ut

if __name__ == "__main__":
    ############################################################################
    # Read parameters

    field_list_file = sys.argv[1]
    config_file = sys.argv[2]
    save_path = sys.argv[3]

    conf = ut.pipeline_conf(config_file)

    suffix = ut.calibration_suffix(conf)

    nx = int(sys.argv[4])
    ny = int(sys.argv[5])

    ############################################################################
    # Initiate log file

    ut.makedir(save_path)

    #log_file_name = os.path.join(save_path, 'compute_XY_maps.log')
    log_file_name = ut.gen_logfile_name('compute_XY_maps.log')
    log_file = os.path.join(save_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")

    ############################################################################
    # Reading field list

    ut.printlog("*********** Reading field list **********", log_file)

    fields = ut.load_field_list(field_list_file)

    ut.printlog(f"Running the pipeline for fields:", log_file)
    ut.printlog(f"{fields}", log_file)

    xbins = [0, 9600, nx]
    ybins = [0, 9600, ny]

################################################################################
# Begin script

if __name__ == "__main__":
    plots_path = os.path.join(save_path, 'plots')
    ut.makedir(plots_path)

# ***************************************************
#    Convert catalogs to fits
# ***************************************************

def convert_2_fits():

    """
    Converts catalogs from ascii to fits
    """

    for field in fields:
        cat_name = f'{field}_mag_ext.cat'
        cat_step = 'external'

        cat_file = os.path.join(conf['save_path'], f'{field}',
                                f'Calibration_{suffix}', cat_step,
                                cat_name)

        save_name = f'{field}_mag_ext.fits'
        save_file = os.path.join(save_path, save_name)

        if not os.path.exists(save_file):

            cmd = f"java -jar {conf['path_to_stilts']} tcopy "
            cmd += f"in={cat_file} ifmt=ascii "
            cmd += f"out={save_file} ofmt=fits"

            ut.printlog(cmd, log_file)
            os.system(cmd)

        else:
            ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    convert_2_fits()

# ***************************************************
#    fix X,Y rotation
# ***************************************************

def fix_XY_rotation():

    """
    Fixes XY rotation of S-PLUS images
    """

    for field in fields:

        cat_name = f'{field}_mag_ext.fits'
        cat_file = os.path.join(save_path, cat_name)

        save_name = f'{field}_mag_ext_xycorr.fits'
        save_file = os.path.join(save_path, save_name)

        xy_rotation_name = f"{field}_detection_x0y0l.csv"
        xy_rotation_file = os.path.join(conf['save_path'], f'{field}',
                                             'Photometry', f'dual',
                                             'detection', xy_rotation_name)

        if not os.path.exists(save_file):

            ut.fix_xy_rotation(catalog = cat_file,
                               save_file = save_file,
                               xcol = 'X',
                               ycol = 'Y',
                               transform_file=xy_rotation_file)


            ut.printlog(f"Created file {save_file}", log_file)

        else:
            ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    fix_XY_rotation()

# ***************************************************
#    Combine calibrated catalogs
# ***************************************************

def concatenate_calib_catalogs():

    """
    Concatenates calibration catalogs after the external calibration step
    """

    print("")
    ut.printlog(('********** '
                 'Concatenating external calibrated magnitudes '
                 '**********'),
                 log_file)
    print("")

    cat_name = '{field}_mag_ext_xycorr.fits'
    cat_file = os.path.join(save_path, cat_name)

    # Start save name
    save_name = 'concat_mag_ext_xycorr.cat'
    save_file = os.path.join(save_path, save_name)

    if not os.path.exists(save_file):

        # Create list of field catalogs
        catalogs_list = []

        for field in fields:
            catalogs_list.append(cat_file.format(field=field))

        ut.concat_data(files_list=catalogs_list,
                       save_file=save_file)

        ut.printlog(f"Created catalog {save_file}", log_file)

    else:
        ut.printlog(f"File {save_name} already exists", log_file)


if __name__ == "__main__":
    concatenate_calib_catalogs()


# ***************************************************
#    Compute XY maps
# ***************************************************

def compute_xy_maps():

    """
    Computes XY correction maps
    """

    print("")
    ut.printlog(('********** '
                 'Computing XY correction maps '
                 '**********'),
                 log_file)
    print("")

    cat_name = 'concat_mag_ext_xycorr.cat'
    cat_file = os.path.join(save_path, cat_name)

    for filt in conf["filters"]:
        #SPLUS_F378_offsets_grid
        save_name = f"SPLUS_{filt}_offsets_grid.npy"
        save_file = os.path.join(save_path, save_name)

        if not os.path.exists(save_file):

            ut.get_xy_correction_grid(data_file = cat_file,
                                      save_file = save_file,
                                      mag       = "SPLUS_"+filt,
                                      mag_ref   = "mod",
                                      xbins     = xbins,
                                      ybins     = ybins)

            ut.printlog(f"Created file {save_file}.", log_file)

        else:
            ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    compute_xy_maps()


# ***************************************************
#    Plot XY maps
# ***************************************************

def plot_xy_maps():

    """
    Plots XY correction maps
    """

    print("")
    ut.printlog(('********** '
                 'Plotting XY correction maps '
                 '**********'),
                 log_file)
    print("")

    for filt in conf["filters"]:

        grid_name = f"SPLUS_{filt}_offsets_grid.npy"
        grid_file = os.path.join(save_path, grid_name)

        save_name = f"xy_corr_map_{filt}.png"
        save_file = os.path.join(plots_path, save_name)

        if not os.path.exists(save_file):

            ut.plot_xy_correction_grid(grid_file = grid_file,
                                       save_file = save_file,
                                       mag       = filt,
                                       xbins     = xbins,
                                       ybins     = ybins)

            ut.printlog(f"Created file {save_file}.", log_file)

        else:
            ut.printlog(f"File {save_file} already exists.", log_file)


if __name__ == "__main__":
    plot_xy_maps()