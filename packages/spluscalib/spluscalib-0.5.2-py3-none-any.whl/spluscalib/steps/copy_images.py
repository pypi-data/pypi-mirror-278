# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                               copy_images.py
#        Copies the images of a given field to the calibration directory
# ******************************************************************************

"""
Copies fiels images from a database to the calibration directory.

The S-PLUS field is given as the first command line argument. Configurations
are set in the config file, given as the second command line argument.

--------------------------------------------------------------------------------
   FUNCTIONS:
--------------------------------------------------------------------------------

check_for_fz_images()
check_for_fits_images()
get_images_from_directory()
get_images_from_ssh()
unpack_images()
save_header_of_fits_images()

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
Ideally this script should only be run through the pipeline.py script.

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$python3 copy_images.py *field_name* *config_file*

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

    if conf["images_sshpass"]:
        sshpass = sys.argv[3]

    ############################################################################
    # Get directories

    field_path = os.path.join(conf['run_path'], field)
    field_log_path = os.path.join(conf['run_path'], field, 'logs')

    images_path = os.path.join(field_path, 'Images')
    log_path = os.path.join(images_path, 'logs')

    photometry_path = os.path.join(field_path, 'Photometry')

    ############################################################################
    # Create Images directory

    ut.makedir(field_path)
    ut.makedir(images_path)
    ut.makedir(log_path)

    ############################################################################
    # Initiate log file

    log_file_name = os.path.join(log_path, 'copy_images.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(images_path, log_file_name)

    with open(log_file, "w") as log:
        log.write("")

################################################################################
# Begin script

############################################################################
# Copy fz images

# ***************************************************
#    Check if .fz images already exist in run_path
# ***************************************************

def check_for_fz_images():

    """
    Checks if all needed .fz images exist in the run_path
    """

    print("")
    ut.printlog(('********** '
                 'Checking if all .fz image files already exist '
                 '**********'),
                log_file)
    print("")

    # Check for .fz files
    all_fz = True

    for filt in conf['filters']:
        if conf['images_sshpass']:
            image_name = f'{field}_{filt}_swp.fits.fz'
        else:
            image_name = f'{field}_{filt}_swp.fz'

        image_fz = os.path.join(images_path, image_name)
        if not os.path.exists(image_fz):
            all_fz = False

        # Check for weight image
        if conf["use_weight"]:
            if conf['images_sshpass']:
                weight_name = f'{field}_{filt}_swpweight.fits.fz'
                weight_fz = os.path.join(images_path, weight_name)
            else:
                weight_name = f'{field}_{filt}_swpweight.fz'
                weight_fz = os.path.join(images_path, weight_name)

            if not os.path.exists(weight_fz):
                all_fz = False

    return all_fz


if __name__ == "__main__":
    has_all_fz = check_for_fz_images()


# ***************************************************
#    Check if images already exist in run_path
# ***************************************************

def check_for_fits_images():

    """
    Checks if all needed .fits images already exist in the run_path
    """

    print("")
    ut.printlog(('********** '
                 'Checking if all .fits image files already exist '
                 '**********'),
                log_file)
    print("")

    # Check for .fits files
    all_fits = True

    for filt in conf['filters']:
        image_name = f'{field}_{filt}_swp.fits'
        image_fits = os.path.join(images_path, image_name)

        if not os.path.exists(image_fits):
            all_fits = False

        # Check for weight image
        if conf["use_weight"]:
            weight_name = f'{field}_{filt}_swpweight.fits'
            weight_fits = os.path.join(images_path, weight_name)

            if not os.path.exists(weight_fits):
                all_fits = False

    return all_fits


if __name__ == "__main__":
    has_all_fits = check_for_fits_images()


# ***************************************************
#    Get images from a directory or...
# ***************************************************

def get_images_from_directory():

    """
    Copies image from the source directory
    """

    print("")
    ut.printlog(('********** '
                 'Copying images from source directory '
                 '**********'),
                log_file)
    print("")

    for filt in conf['filters']:

        image_name = f'{field}_{filt}_swp.fz'
        image_db_fz = os.path.join(conf['path_to_images'], field,
                                   image_name)
        image_fz = os.path.join(images_path, image_name)

        if not os.path.exists(image_fz):

            ut.printlog(f"Copying image {image_name}", log_file,
                        color="yellow")

            cmd = f"cp {image_db_fz} {images_path}"
            ut.printlog(cmd, log_file, color="green")
            os.system(cmd)

        else:
            ut.printlog(f"Image {image_fz} already exists",
                        log_file, color="white", attrs=["dark"])

        if conf['use_weight']:

            weight_name = f'{field}_{filt}_swpweight.fz'
            weight_db_fz = os.path.join(conf['path_to_images'], field,
                                   weight_name)
            weight_fz = os.path.join(images_path, weight_name)

            if not os.path.exists(weight_fz):
                cmd = f"cp {weight_db_fz} {images_path}"
                ut.printlog(cmd, log_file, color="green")
                os.system(cmd)

            else:
                ut.printlog(f"Image {weight_fz} already exists",
                            log_file, color="white", attrs=["dark"])


if __name__ == "__main__":
    if not (has_all_fz or has_all_fits):
        if not conf["images_sshpass"] and not 'copy_local_images' in conf["run_steps"]:
            get_images_from_directory()


# ***************************************************
#    Get images from ssh
# ***************************************************

def get_images_from_ssh():

    """
    Copies image from the source by ssh
    """

    print("")
    ut.printlog(('********** '
                 'Copying images from source by ssh '
                 '**********'),
                log_file)
    print("")

    sshuser = conf["sshpass_user"]
    sship = conf["sshpass_ip"]
    sshpath = conf["sshpass_path"]

    for filt in conf['filters']:

        # Deal with JYPE images ending with .fz and MAR ending with .fits.fz
        if sship == '10.180.3.152':
            image_name = f'{field}_{filt}_swp.fits.fz'
        elif sship == '10.180.3.104':
            image_name = f'{field}_{filt}_swp.fz'
        elif sship == 'splus3101.iag.usp.br':
            image_name = f'{field}_{filt}_swp.fz'            
        else:
            image_name = f'{field}_{filt}_swp.fits.fz'

        image_db_fz = os.path.join(sshpath, field, image_name)
        image_fz = os.path.join(images_path, image_name)

        new_image_fz = image_fz.replace(".fits.fz", ".fz")

        if not os.path.exists(new_image_fz):

            ut.printlog(f"Copying by sshpass image {image_name}",
                        log_file, color="yellow")

            cmd = f"sshpass -p '{sshpass}' scp {sshuser}@{sship}:{image_db_fz} "
            cmd += f"{images_path}"

            cmd_hidepass = cmd.replace(sshpass, "*" * len(sshpass))
            ut.printlog(cmd_hidepass, log_file, color="green")
            os.system(cmd)

            cmd = f"mv {image_fz} {new_image_fz}"
            ut.printlog(cmd, log_file, color="green")
            os.system(cmd)

        else:
            ut.printlog(f"Image {image_fz} already exists",
                        log_file, color="white", attrs=["dark"])


        if conf['use_weight']:

            # Deal with JYPE images ending with .fz and MAR ending with .fits.fz
            if sship == '10.180.3.152':
                weight_name = f'{field}_{filt}_swpweight.fits.fz'
            elif sship == '10.180.3.104':
                weight_name = f'{field}_{filt}_swpweight.fz'
            elif sship == 'splus3101.iag.usp.br':
                weight_name = f'{field}_{filt}_swpweight.fz'
            else:
                weight_name = f'{field}_{filt}_swpweight.fits.fz'

            weight_db_fz = os.path.join(sshpath, field, weight_name)
            weight_fz = os.path.join(images_path, weight_name)

            new_weight_fz = weight_fz.replace(".fits.fz", ".fz")

            if not os.path.exists(new_weight_fz):

                cmd = f"sshpass -p '{sshpass}' scp "
                cmd += f"{sshuser}@{sship}:{weight_db_fz} "
                cmd += f"{images_path}"

                cmd_hidepass = cmd.replace(sshpass, "*" * len(sshpass))
                ut.printlog(cmd_hidepass, log_file, color="green")
                os.system(cmd)

                cmd = f"mv {weight_fz} {new_weight_fz}"
                ut.printlog(cmd, log_file, color="green")
                os.system(cmd)

            else:
                ut.printlog(f"Image {weight_fz} already exists",
                            log_file,
                            color="white", attrs=["dark"])


def copy_images_from_local_directory():
    for filt in conf['filters']:

        # Deal with JYPE images ending with .fz and MAR ending with .fits.fz
        if conf["reduction"] == 'MAR':
            image_name = f'{field}_{filt}_swp.fits.fz'
        else:
            image_name = f'{field}_{filt}_swp.fz'

        image_db_fz = os.path.join(conf["local_path"], field, image_name)
        image_fz = os.path.join(images_path, image_name)

        new_image_fz = image_fz.replace(".fits.fz", ".fz")

        if not os.path.exists(new_image_fz):

            ut.printlog(f"Copying image {image_name}",
                        log_file, color="yellow")

            cmd = f"cp {image_db_fz} {images_path}"
            ut.printlog(cmd, log_file, color="green")
            os.system(cmd)

            cmd = f"mv {image_fz} {new_image_fz}"
            ut.printlog(cmd, log_file, color="green")
            os.system(cmd)

        else:
            ut.printlog(f"Image {image_fz} already exists",
                        log_file, color="white", attrs=["dark"])


        if conf['use_weight']:
            if conf["reduction"] == 'MAR':
                weight_name = f'{field}_{filt}_swpweight.fits.fz'
            else:
                image_name = f'{field}_{filt}_swpweight.fz'
            
            weight_db_fz = os.path.join(conf["local_path"], field, weight_name)
            weight_fz = os.path.join(images_path, weight_name)

            new_weight_fz = weight_fz.replace(".fits.fz", ".fz")

            if not os.path.exists(new_weight_fz):
                cmd = f"cp {weight_db_fz} {images_path}"
                ut.printlog(cmd, log_file, color="green")
                os.system(cmd)

                cmd = f"mv {weight_fz} {new_weight_fz}"
                ut.printlog(cmd, log_file, color="green")
                os.system(cmd)

            else:
                ut.printlog(f"Image {weight_fz} already exists",
                            log_file,
                            color="white", attrs=["dark"])


if __name__ == "__main__":
    if not (has_all_fz or has_all_fits):
        if conf["images_sshpass"]:
            get_images_from_ssh()
        if not conf["images_sshpass"] and 'copy_local_images' in conf["run_steps"]:
            copy_images_from_local_directory()


# ***************************************************
#    Unpack images
# ***************************************************

def unpack_images():

    """
    Unpacks the .fz files into .fits files
    """

    print("")
    ut.printlog(('********** '
                 'Unpacking .fz images '
                 '**********'),
                log_file)
    print("")

    for filt in conf['filters']:

        image_name = f'{field}_{filt}_swp.fz'
        image_fz = os.path.join(images_path, image_name)
        image_fits = image_fz.replace(".fz", ".fits")

        if not os.path.exists(image_fits):

            ut.printlog(f"Unpacking image {image_fz}", log_file,
                        color="yellow")
            ut.fz2fits(image_fz)

        else:
            ut.printlog(f"Image {image_fits} already exists",
                        log_file, color="white", attrs=["dark"])

        if conf['use_weight']:
            weight_fz = image_fz.replace(".fz", "weight.fz")
            weight_fits = weight_fz.replace(".fz", ".fits")

            if not os.path.exists(weight_fits):
                ut.printlog(f"Unpacking weight {weight_fz}",
                            log_file, color="yellow")
                ut.fz2fits(weight_fz)

            else:
                ut.printlog(f"Image {weight_fits} already exists",
                            log_file, color="white", attrs=["dark"])


if __name__ == "__main__":
    if conf["unpack_images"] and not has_all_fits:
        unpack_images()


# ***************************************************
#    Check again for all fits
# ***************************************************

if __name__ == "__main__":
    has_all_fits = check_for_fits_images()


# ***************************************************
#    Save headers
# ***************************************************

def save_header_of_fits_images():

    """
    Saves header of the fits images in a txt file
    """

    print("")
    ut.printlog(('********** '
                 'Saving header of the fits images '
                 '**********'),
                log_file)
    print("")

    # Get and/or create headers directory
    images_headers = os.path.join(images_path, "headers")

    if not os.path.exists(images_headers):
        cmd = f"mkdir {images_headers}"
        ut.printlog(cmd, log_file, color="yellow")
        os.system(cmd)

    # Save header for each filter
    for filt in conf['filters']:

        image_name = f'{field}_{filt}_swp.fz'
        image_fz = os.path.join(images_path, image_name)
        image_fits = image_fz.replace(".fz", ".fits")

        header_name = image_name.replace(".fz", ".header")
        header_file = os.path.join(images_headers, header_name)

        if not os.path.exists(header_file):

            ut.save_fits_header(image_fits=image_fits,
                                output_file=header_file)

            ut.printlog((f"Saved header of image {image_fits} to file "
                         f"{header_file}"), log_file,
                        color="yellow")

        else:
            ut.printlog(f"Header of {image_fits} already saved",
                        log_file, color="white", attrs=["dark"])

        # Also save header of weight images
        if conf['use_weight']:
            weight_fz = image_fz.replace(".fz", "weight.fz")
            weight_fits = weight_fz.replace(".fz", ".fits")

            wheader_file = header_file.replace(".header", "weight.header")

            if not os.path.exists(wheader_file):

                ut.save_fits_header(image_fits=weight_fits,
                                    output_file=wheader_file)

                ut.printlog((f"Saved header of image {weight_fits} to file "
                             f"{wheader_file}"), log_file,
                            color="yellow")

            else:
                ut.printlog(f"Header of {weight_fits} already saved",
                            log_file, color="white", attrs=["dark"])


if __name__ == "__main__":
    if has_all_fits:
        save_header_of_fits_images()
