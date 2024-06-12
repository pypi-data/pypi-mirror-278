# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                              photometry_res.py
#                restricted aperture photometry in dual mode
# ******************************************************************************

"""
Runs SExtractor in dual mode for one S-PLUS field and a list of filters to 
obtain 'restricted' auto magnitudes, which employ SExtractor parameter:

Runs after photometry dual and edits its final output catalog

The S-PLUS field is given as the first command line argument.

The set of filters, location of S-PLUS images, default SExtractor configuration
and param files, filters used to build the detection image, and the output path
must be set in the configuration file given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

create_res_photometry_path()
generate_res_sexconfig_files()
unpack_detection_image()
run_sex_res()
convert_detection_fits_to_fz()
rename_res_columns()
crossmatch_res_dual_catalogs()
remove_res_dual_duplicate_columns()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 photometry_res.py *field_name* *config_file*

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

print(ut.__file__)
print()

if __name__ == "__main__":
    ############################################################################
    # Read parameters

    field     = sys.argv[1]
    config_file = sys.argv[2]

    conf = ut.pipeline_conf(config_file)

    ############################################################################
    # Get directories

    field_path      = os.path.join(conf['run_path'], field)
    photometry_path = os.path.join(field_path, 'Photometry')
    dual_path       = os.path.join(photometry_path, 'dual')
    catalogs_path    = os.path.join(dual_path, 'catalogs')
    detection_path   = os.path.join(dual_path, 'detection')

    res_path        = os.path.join(photometry_path, 'res')
    res_sexconf_path = os.path.join(res_path, 'sexconf')
    res_catalog_path = os.path.join(res_path, 'catalogs')

    images_path     = os.path.join(field_path, 'Images')

    log_path        = os.path.join(photometry_path, 'logs')

    ############################################################################
    # Create Photometry directory

    ut.makedir(field_path)
    ut.makedir(photometry_path)
    ut.makedir(log_path)

    ############################################################################
    # Initiate log file

    log_file_name = os.path.join(log_path, 'photometry_res.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(photometry_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")

    ############################################################################
    # Log configuration

    ut.printlog("Dual mode photometry parameters:", log_file,
                color = "blue", attrs=["bold"])

    dual_mode_params = ['run_path', 'filters', 'path_to_images', 'inst_zp',
                        'use_weight', 'path_to_sex', 'sex_config_res', 
                        'sex_param_res', 'detection_image']

    for param in dual_mode_params:
        try:
            ut.printlog(f"{param}: {conf[param]}", log_file,
                        color = "blue")
        except KeyError:
            ut.printlog(f"{param}: NONE", log_file,
                        color = "red")

################################################################################
# Begin script

# ***************************************************
#    If photometry path does not exist -> create
# ***************************************************


def create_res_photometry_path():

    """
    Creates the directories for the restricted photometry step of the pipeline
    """
    
    print("")
    ut.printlog(('********** '
                 'Generating Restricted Photometry paths '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    # Create dual mode photometry path
    ut.makedir(res_path)

    # Create dual mode sexconf path
    ut.makedir(res_sexconf_path)

    # Create dual mode catalogs path
    ut.makedir(res_catalog_path)


if __name__ == "__main__":
    create_res_photometry_path()


# ***************************************************
#    Generate SExconfig files
# ***************************************************


def generate_res_sexconfig_files():

    """
    Generates the restricted-mode sexconfig file for all filters
    """

    print("")
    ut.printlog(('********** '
                 'Generating Restricted Photometry config files '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    # Default SExconfig and SExparam files
    default_sexconfig = conf['sex_config_res']
    default_sexparam  = conf['sex_param_res']

    # Generate configuration for each filter
    for filt in conf['filters']:

        # Generate location of config file
        conf_file_name = f"{field}_{filt}_res.sex"
        save_file = os.path.join(res_sexconf_path, conf_file_name)

        # Generate location of output catalog file
        catalog_name = f"sex_{field}_{filt}_res.fits"
        catalog_file = os.path.join(res_catalog_path, catalog_name)

        # Get location of image file
        image_name = f"{field}_{filt}_swp.fits"
        image_file = os.path.join(images_path, image_name)

        # Get location of detection image file
        detection_name = f"{field}_detection.fits"
        detection_file = os.path.join(detection_path, detection_name)

        if not os.path.exists(save_file):

            ut.get_sex_config(save_file = save_file,
                              default_sexconfig = default_sexconfig,
                              default_sexparam  = default_sexparam,
                              catalog_file      = catalog_file,
                              image_file        = image_file,
                              inst_zp           = conf['inst_zp'],
                              path_to_sex       = conf['path_to_sex'],
                              use_weight        = conf['use_weight'],
                              mode              = 'dual',
                              detection_file    = detection_file)

            ut.printlog(("Generated restricted mode sexconfig for field "
                         f"{field}, filter {filt}"), log_file,
                         color = "green")

        else:
            ut.printlog(("Restricted mode sexconfig already obtained for field "
                         f"{field}, filter {filt}"), log_file,
                         color = "white", attrs=["dark"])

    # Copy sexparam file to field config directory (for proper documentation)
    cmd = f'cp {default_sexparam} {res_sexconf_path}'
    ut.printlog("$ "+cmd, log_file, color = "green")
    os.system(cmd)


if __name__ == "__main__":
    generate_res_sexconfig_files()


# ***************************************************
#    Unpack Detection images
# ***************************************************

def unpack_detection_image():

    """
    Unpacks the .fz detection image files into .fits files
    """

    print("")
    ut.printlog(('********** '
                 'Unpacking .fz detection image '
                 '**********'),
                log_file)
    print("")

    det_image_name = f"{field}_detection.fits"
    det_image_fits_file = os.path.join(detection_path, det_image_name)
    det_weight_fits_file = det_image_fits_file.replace(".fits", "weight.fits")

    det_image_fz_file = det_image_fits_file.replace(".fits", ".fits.fz")
    det_weight_fz_file = det_weight_fits_file.replace(".fits", ".fits.fz")

    images_fits = [det_image_fits_file, det_weight_fits_file]
    images_fz   = [det_image_fz_file, det_weight_fz_file]
    names       = ['Detection', 'Detection weight']

    for image_fits, image_fz, name in zip(images_fits, images_fz, names):
        if not os.path.exists(image_fits):

            ut.printlog(f"Unpacking {name} {image_fz}", log_file,
                        color="yellow")
            ut.fz2fits(image_fz)

        else:
            ut.printlog(f"Image {image_fits} already exists",
                        log_file, color="white", attrs=["dark"])


if __name__ == "__main__":
    unpack_detection_image()


# ***************************************************
#    Run SExtractor in Dual Mode
# ***************************************************


def run_sex_res():

    """
    Runs SExtractor in Restricted mode for all filters
    """

    print("")
    ut.printlog(('********** '
                 'Running SeX in Restricted mode '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    for filt in conf['filters']:

        # Generate location of output catalog file
        catalog_name = f"sex_{field}_{filt}_res.fits"
        catalog_file = os.path.join(res_catalog_path, catalog_name)

        if not os.path.exists(catalog_file):

            # Get location of image file
            image_name = f"{field}_{filt}_swp.fits"
            image_file = os.path.join(images_path, image_name)

            # Get location of detection image file
            detection_name = f"{field}_detection.fits"
            detection_file = os.path.join(detection_path, detection_name)

            # Generate location of config file
            conf_file_name = f"{field}_{filt}_res.sex"
            sexconf_file   = os.path.join(res_sexconf_path, conf_file_name)

            # Run SExtractor
            if conf['direct_path_to_sex']:
                sex_location = conf['path_to_sex']
            else:
                sex_location = os.path.join(conf['path_to_sex'], 'src', 'sex')

            cmd = (f"{sex_location} {detection_file}, {image_file} "
                   f"-c {sexconf_file}")

            ut.printlog("$ "+cmd, log_file, color = "cyan")
            os.system(cmd)

        else:
            ut.printlog(("Restricted photometry already obtained for field "
                         f"{field}, filter {filt}"), log_file,
                         color = "white", attrs = ["dark"])


if __name__ == "__main__":
    run_sex_res()


# ***************************************************
#    Convert detection .fits to .fz
# ***************************************************

def convert_detection_fits_to_fz():

    """
    Converts detection image, detection weight, detection .aper and
    detection .segm from .fits to .fz

    Then, remove the .fits files.
    """

    print("")
    ut.printlog(('********** '
                 'Converting detection .fits to .fz '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    det_image_name = f"{field}_detection.fits"
    det_image_file = os.path.join(detection_path, det_image_name)

    det_weight_file = det_image_file.replace(".fits", "weight.fits")
    det_aper_file   = det_image_file.replace(".fits", ".aper.fits")
    det_segm_file   = det_image_file.replace(".fits", ".segm.fits")

    images = [det_image_file, det_weight_file, det_aper_file, det_segm_file]
    names  = ['Detection', 'Detection weight', 'Detection aper',
              'Detection segm']

    for image, name in zip(images, names):
        if not os.path.exists(image+'.fz'):

            # Compress fits
            cmd = f"fpack {image}"
            ut.printlog("$ " + cmd, log_file, color = "cyan")
            os.system(cmd)

        else:
            ut.printlog(f"{name} image already compressed.", log_file,
                        color = "white", attrs = ["dark"])

        if os.path.exists(image + '.fz'):
            # Remove fits
            cmd = f"rm {image}"
            ut.printlog("$ " + cmd, log_file, color = "red")
            os.system(cmd)

        else:
            ut.printlog(f"{name} fits image already deleted.", 
                        log_file, color = "white", attrs = ["dark"])


if __name__ == "__main__":
    convert_detection_fits_to_fz()


# ***************************************************
#    Rename restricted mag columns
# ***************************************************
    
def rename_res_columns():

    """
    Renames restricted aperture columns
    """

    print("")
    ut.printlog(('********** '
                 'Renaming Restricted aperture columns '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    for filt in conf['filters']:

        # Generate location of output catalog file
        catalog_name = f"sex_{field}_{filt}_res.fits"
        catalog_file = os.path.join(res_catalog_path, catalog_name)

        # rename_complete_check_file
        check_name = f"rename_check_{field}_{filt}.txt"
        check_file = os.path.join(res_catalog_path, check_name)

        if not os.path.exists(check_file):
            ut.rename_restricted_aper_columns(catalog_file)

            with open(check_file, 'w') as f:
                f.write("True")

            ut.printlog(("Renamed restricted mode columns for field "
                         f"{field}, filter {filt}"), log_file,
                         color = "green")

        else:
            ut.printlog(("Restricted mode columns already renamed for field "
                         f"{field}, filter {filt}"), log_file,
                         color = "white", attrs=["dark"])


if __name__ == "__main__":
    rename_res_columns()

# ***************************************************
#    Crossmatch res + dual mode catalogs
# ***************************************************

def crossmatch_res_dual_catalogs():

    """
    Crossmatches restricted aperture columns to previously ontained dual mode
    catalog
    """

    print("")
    ut.printlog(('********** '
                 'Crossmatching Restricted and dual mode catalogs '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    for filt in conf['filters']:

        # Generate location of catalog files
        res_catalog_name = f"sex_{field}_{filt}_res.fits"
        res_catalog_file = os.path.join(res_catalog_path, res_catalog_name)

        dual_catalog_name = f"sex_{field}_{filt}_dual.fits"
        dual_catalog_file = os.path.join(catalogs_path, dual_catalog_name)

        # rename_complete_check_file
        check_name = f"res_crossmatch_check_{field}_{filt}.txt"
        check_file = os.path.join(catalogs_path, check_name)

        if not os.path.exists(check_file):
            # Start tmatchn cmd
            cmd = f"java -jar {conf['path_to_stilts']} tmatch2 "

            cmd += f"ifmt1=fits in1={dual_catalog_file} "
            cmd += f"values1='ALPHA_J2000 DELTA_J2000' "

            cmd += f"ifmt2=fits in2={res_catalog_file} "
            cmd += f"values2='ALPHA_J2000_RES DELTA_J2000_RES' "

            cmd += f"out={dual_catalog_file} ofmt=fits "
            cmd += f"matcher=sky params=1 join=all1 "

            ut.printlog(cmd, log_file)
            os.system(cmd)

            ut.printlog(f"Crossmatched dual and restricted catalogs", log_file)

            with open(check_file, 'w') as f:
                f.write("True")

            ut.printlog(("Crossmatched dual and restricted catalogs "
                         f"{field}, filter {filt}"), log_file,
                         color = "green")

        else:
            ut.printlog(("Dual and restricted catalogs already crossmatched "
                         f"{field}, filter {filt}"), log_file,
                         color = "white", attrs=["dark"])


if __name__ == "__main__":
    crossmatch_res_dual_catalogs()