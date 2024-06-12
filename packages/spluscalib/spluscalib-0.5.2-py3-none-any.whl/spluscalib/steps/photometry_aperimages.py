# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                           photometry_aperimages.py
#                       Generates photometry .aper images
# ******************************************************************************

"""
Generates .aper images for the detection image in the dual mode photometry

The S-PLUS field is given as the first command line argument.

The set of filters, location of S-PLUS images, default SExtractor configuration
and param files, filters used to build the detection image, and the output path
must be set in the configuration file given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

unpack_images()
run_sex_detection_aperAUTO()
run_sex_detection_aperPETRO()
convert_aper_fits_to_fz()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 photometry_aperimages.py *field_name* *config_file*

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

    field     = sys.argv[1]
    config_file = sys.argv[2]

    conf = ut.pipeline_conf(config_file)

    ############################################################################
    # Get directories

    field_path      = os.path.join(conf['run_path'], field)
    photometry_path = os.path.join(field_path, 'Photometry')
    dual_path       = os.path.join(photometry_path, 'dual')
    detection_path  = os.path.join(dual_path, 'detection')

    log_path        = os.path.join(photometry_path, 'logs')

    ############################################################################
    # Create Photometry directory

    ut.makedir(log_path)

    ############################################################################
    # Initiate log file

    log_file_name = os.path.join(log_path, 'photometry_aperimages.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(photometry_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")

    ############################################################################
    # Log configuration

    ut.printlog("Dual mode photometry parameters:", log_file,
                color = "blue", attrs=["bold"])

    dual_mode_params = ['run_path', 'filters', 'path_to_images', 'inst_zp',
                        'use_weight', 'path_to_sex', 'sex_config', 'sex_param',
                        'detection_image']

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
#   Unpack detection image
# ***************************************************

def unpack_images():
    """
    Unpacks detection image .fz file
    """

    print("")
    ut.printlog(('********** '
                 'Unpacking detection image '
                 '**********'),
                 log_file, color = "yellow")
    print("")


    image_name = f"{field}_detection.fits.fz"
    image_fz = os.path.join(detection_path, image_name)
    image_fits = image_fz[:-3]

    if not os.path.exists(image_fits):

        ut.printlog(f"Unpacking image {image_fz}", log_file,
                    color="yellow")
        ut.fz2fits(image_fz)

        cmd = f"mv {image_fz.replace('.fz', '.fits')} {image_fits}"
        ut.printlog("$ " + cmd, log_file, color="cyan")
        os.system(cmd)

    else:
        ut.printlog(f"Image {image_fits} already exists",
                    log_file, color="white", attrs=["dark"])

    if conf['use_weight']:
        weight_fz = image_fz.replace(".fits.fz", "weight.fits.fz")
        weight_fits = weight_fz[:-3]

        if not os.path.exists(weight_fits):
            ut.printlog(f"Unpacking weight {weight_fz}",
                        log_file, color="yellow")
            ut.fz2fits(weight_fz)

            cmd = f"mv {weight_fz.replace('.fz', '.fits')} {weight_fits}"
            ut.printlog("$ " + cmd, log_file, color="cyan")
            os.system(cmd)


        else:
            ut.printlog(f"Image {weight_fits} already exists",
                        log_file, color="white", attrs=["dark"])


if __name__ == "__main__":
    unpack_images()


# ***************************************************
#   Run SExtractor in Detection image for .aperAUTO
# ***************************************************

def run_sex_detection_aperAUTO():

    """
    Run SExtractor in Detection image
    """

    print("")
    ut.printlog(('********** '
                 'Running SeX on detection image to generate aperAUTO '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    conf_file_name = f"{field}_detection.sex"
    sexconf_file   = os.path.join(detection_path, conf_file_name)

    image_name = f"{field}_detection.fits"
    image_file = os.path.join(detection_path, image_name)
    image_auto = image_file.replace(".fits", ".aperAUTO.fits")
    image_autofz = image_auto + '.fz'

    catalog_name = f"tmp_{field}_detection_catalog.fits"
    catalog_file = os.path.join(detection_path, catalog_name)


    # Run SExtractor
    if conf['direct_path_to_sex']:
        sex_location = conf['path_to_sex']
    else:
        sex_location = os.path.join(conf['path_to_sex'], 'src', 'sex')
    
    if not os.path.exists(image_auto) and not os.path.exists(image_autofz):

        cmd = f"{sex_location} {image_file} -c {sexconf_file}"
        cmd += f" -CATALOG_NAME '{catalog_file}'"
        cmd += " -PHOT_APERTURES '0'"
        cmd += " -PHOT_PETROPARAMS '0,0'"
        cmd += " -CHECKIMAGE_TYPE 'APERTURES'"
        cmd += f" -CHECKIMAGE_NAME '{image_auto}'"

        ut.printlog("$ "+cmd, log_file, color = "cyan")
        os.system(cmd)

        # Remove tmp catalog file
        cmd = f"rm {catalog_file}"
        ut.printlog("$ "+cmd, log_file, color = "cyan")
        os.system(cmd)

    else:
        ut.printlog(f"aperAUTO image already obtained for field {field}",
                    log_file, color = "white", attrs = ["dark"])


if __name__ == "__main__":
    run_sex_detection_aperAUTO()


# ***************************************************
#   Run SExtractor in Detection image for .aperPETRO
# ***************************************************

def run_sex_detection_aperPETRO():

    """
    Run SExtractor in Detection image
    """

    print("")
    ut.printlog(('********** '
                 'Running SeX on detection image to generate aperPETRO '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    conf_file_name = f"{field}_detection.sex"
    sexconf_file   = os.path.join(detection_path, conf_file_name)

    image_name = f"{field}_detection.fits"
    image_file = os.path.join(detection_path, image_name)
    image_petro = image_file.replace(".fits", ".aperPETRO.fits")
    image_petrofz = image_petro + '.fz'

    catalog_name = f"tmp_{field}_detection_catalog.fits"
    catalog_file = os.path.join(detection_path, catalog_name)

    # Run SExtractor
    if conf['direct_path_to_sex']:
        sex_location = conf['path_to_sex']
    else:
        sex_location = os.path.join(conf['path_to_sex'], 'src', 'sex')

    if not os.path.exists(image_petro) and not os.path.exists(image_petrofz):

        cmd = f"{sex_location} {image_file} -c {sexconf_file}"
        cmd += f" -CATALOG_NAME '{catalog_file}'"
        cmd += " -PHOT_APERTURES '0'"
        cmd += " -PHOT_AUTOPARAMS '0,0'"
        cmd += " -CHECKIMAGE_TYPE 'APERTURES'"
        cmd += f" -CHECKIMAGE_NAME '{image_petro}'"

        ut.printlog("$ "+cmd, log_file, color = "cyan")
        os.system(cmd)

        # Remove tmp catalog file
        cmd = f"rm {catalog_file}"
        ut.printlog("$ "+cmd, log_file, color = "cyan")
        os.system(cmd)

    else:
        ut.printlog(f"aperPETRO image already obtained for field {field}",
                    log_file, color = "white", attrs = ["dark"])


if __name__ == "__main__":
    run_sex_detection_aperPETRO()


# ***************************************************
#   Convert aper images from .fits to .fz
# ***************************************************

def convert_aper_fits_to_fz():

    """
    Converts aper images from .fits to .fz

    Then, remove the .fits files.
    """

    print("")
    ut.printlog(('********** '
                 'Converting aper .fits to .fz '
                 '**********'),
                 log_file, color = "yellow")
    print("")

    det_image_name = f"{field}_detection.fits"
    det_image_file = os.path.join(detection_path, det_image_name)
    det_image_weight = det_image_file.replace(".fits", "weight.fits")

    aperAUTO_file   = det_image_file.replace(".fits", ".aperAUTO.fits")
    aperPETRO_file  = det_image_file.replace(".fits", ".aperPETRO.fits")

    images = [det_image_file, det_image_weight, aperAUTO_file, aperPETRO_file]
    names  = ['detection', 'detectionweight', 'aperAUTO', 'aperPETRO']

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
            ut.printlog(f"{name} fits image already deleted.", log_file,
                        color = "white", attrs = ["dark"])


if __name__ == "__main__":
    convert_aper_fits_to_fz()
