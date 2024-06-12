# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                          concatenate_zp_catalogs.py
#                   Concatenates zp-files of a list of fields
# ******************************************************************************

"""
Concatenates zp-files of a list of fields in a single file for all steps of the
pipeline

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

concat_gaiaXPSP()
concat_external()
concat_gaiascale_gaia()
concat_gaiascale_splus()
concat_final_zps()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
This script should be run individually and not within the pipeline.py script

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 fit_zp_offsets.py *field_list_file* *config_file* *save_path*[opt]

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

    conf = ut.pipeline_conf(config_file)

    calib = conf['calibration_name']
    calib_path = conf['save_path']

    ############################################################################
    # Automatic save_path

    try:
        save_path = sys.argv[3]
    except IndexError:
        field_list_file_name = os.path.basename(field_list_file).replace(".fields",
                                                                        "")

        save_path = os.path.join(conf['save_path'], 'ZPs_' + field_list_file_name)

    if not os.path.exists(save_path):
        os.system( f'mkdir {save_path}')

    ############################################################################
    # Initiate log file

    log_file_name = os.path.join(save_path, 'concat_zp_catalogs.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(save_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")

    ############################################################################
    # Reading field list

    ut.printlog("*********** Reading field list **********", log_file)

    fields = ut.load_field_list(field_list_file)

    ut.printlog(f"Running the script for fields:", log_file)
    ut.printlog(f"{fields}", log_file)

################################################################################
# Begin script

# ***************************************************
#    Concat Gaia XPSP zps
# ***************************************************

def concat_gaiaXPSP():

    """
    Concatenates Gaia XPSP zero points in a single file
    """

    print("")
    ut.printlog(('********** '
                 'Concatenating gaia XPSP ZPs '
                 '**********'),
                log_file)
    print("")

    save_name = f"concat_gaiaxpsp_ZPs.csv"
    save_file = os.path.join(save_path, save_name)

    if not os.path.exists(save_file):

        fields_zps = {}

        for field in fields:
            zp_file = os.path.join(calib_path, field,
                                    f"Calibration_{calib}",
                                    'gaiaXPSP', f'{field}_gaiaxpsp.zp')

            fields_zps[field] = zp_file

        ########################
        # Get concat catalog

        ut.zp_concat_catalogs(fields_zps  = fields_zps,
                              save_file   = save_file,
                              filters     = conf["gaiaxpsp_sed_pred"])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    concat_gaiaXPSP()


# ***************************************************
#    Concat external zps
# ***************************************************

def concat_external():

    """
    Concatenates external zero points in a single file
    """

    print("")
    ut.printlog(('********** '
                 'Concatenating external ZPs '
                 '**********'),
                log_file)
    print("")

    save_name = f"concat_external_ZPs.csv"
    save_file = os.path.join(save_path, save_name)

    if not os.path.exists(save_file):

        fields_zps = {}

        for field in fields:
            zp_file = os.path.join(calib_path, field,
                                    f"Calibration_{calib}",
                                    'external', f'{field}_external.zp')

            fields_zps[field] = zp_file

        ########################
        # Get concat catalog

        ut.zp_concat_catalogs(fields_zps  = fields_zps,
                              save_file   = save_file,
                              filters     = conf["external_sed_pred"])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    concat_external()


# ***************************************************
#    Concat gaiascale gaia zps
# ***************************************************

def concat_gaiascale_gaia():

    """
    Concatenates gaiascale (gaia) zero points in a single file
    """

    print("")
    ut.printlog(('********** '
                 'Concatenating gaiascale (gaia) ZPs '
                 '**********'),
                log_file)
    print("")

    save_name = f"concat_gaiascale_gaia_ZPs.csv"
    save_file = os.path.join(save_path, save_name)

    if not os.path.exists(save_file):

        fields_zps = {}

        for field in fields:
            zp_file = os.path.join(calib_path, field,
                                    f"Calibration_{calib}",
                                    'gaiascale', f'{field}_gaiascale_gaia.zp')

            fields_zps[field] = zp_file

        ########################
        # Get concat catalog

        ut.zp_concat_catalogs(fields_zps  = fields_zps,
                              save_file   = save_file,
                              filters     = conf["gaiascale_sed_pred"])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    concat_gaiascale_gaia()


# ***************************************************
#    Concat gaiascale splus zps
# ***************************************************

def concat_gaiascale_splus():

    """
    Concatenates gaiascale (splus) zero points in a single file
    """

    print("")
    ut.printlog(('********** '
                 'Concatenating gaiascale (splus) ZPs '
                 '**********'),
                log_file)
    print("")

    save_name = f"concat_gaiascale_splus_ZPs.csv"
    save_file = os.path.join(save_path, save_name)

    if not os.path.exists(save_file):

        fields_zps = {}

        for field in fields:
            zp_file = os.path.join(calib_path, field,
                                    f"Calibration_{calib}",
                                    'gaiascale', f'{field}_gaiascale_splus.zp')

            fields_zps[field] = zp_file

        ########################
        # Get concat catalog

        ut.zp_concat_catalogs(fields_zps  = fields_zps,
                              save_file   = save_file,
                              filters     = conf["gaiascale_sed_fit"])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    concat_gaiascale_splus()


# ***************************************************
#    Concat final zps
# ***************************************************

def concat_final_zps():

    """
    Concatenates final zero points in a single file
    """

    print("")
    ut.printlog(('********** '
                 'Concatenating final ZPs '
                 '**********'),
                log_file)
    print("")

    save_name = f"concat_final_ZPs.csv"
    save_file = os.path.join(save_path, save_name)

    if not os.path.exists(save_file):

        fields_zps = {}

        for field in fields:
            zp_file = os.path.join(calib_path, field,
                                    f"Calibration_{calib}",
                                    f'{field}_final.zp')

            fields_zps[field] = zp_file

        ########################
        # Get concat catalog

        ut.zp_concat_catalogs(fields_zps  = fields_zps,
                              save_file   = save_file,
                              filters     = conf["gaiascale_sed_fit"])

        ut.printlog(f"Created file {save_file}", log_file)

    else:
        ut.printlog(f"Catalog {save_name} already exists", log_file)


if __name__ == "__main__":
    concat_final_zps()