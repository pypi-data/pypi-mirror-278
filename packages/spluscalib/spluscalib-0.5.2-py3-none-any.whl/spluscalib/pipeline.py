# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                                 pipeline.py
#             Runs all the steps of the S-PLUS calibration pipeline
# ******************************************************************************


"""
This scripts runs the steps of the calibration pipeline

--------------------------------------------------------------------------------
   INPUTS:
--------------------------------------------------------------------------------
All inputs are taken from the config_file

--------------------------------------------------------------------------------
   COMMENTS:
--------------------------------------------------------------------------------
User must not change anything in this code. Changes to choose which steps to
run should be made in the config_file

config_file.py
    run_steps        = [*list of stepś*]

    possible steps are:
        The following steps are necessary to complete the calibration
        'photometry_single': obtain aperture photometry in single mode
        'photometry_dual'  : obtain aperture photometry in dual mode
        'photometry_psf'   : obtain psf photometry
        'correction_xy'    : corrects XY position zero-points inhomogeneities
        'aper_corretion'   : applies aperture correction to fixed aperture

--------------------------------------------------------------------------------
   USAGE:
--------------------------------------------------------------------------------
$ python pipeline_final *field_list_file* *config_file*

the field_list_file should be an ascii file where each line is the name of one
field to calibrate.
----------------
"""

################################################################################
# Import external packages

import os
import sys
import getpass

from termcolor import cprint

usage_message = """
USAGE:

option1: list of fields
$spluscalib  *field_list_file* *config_file*

option2: single field
$spluscalib  *field_name* *config_file* --onefield

"""

pipeline_path = os.path.split(__file__)[0]

sys.path.append(pipeline_path)

################################################################################
# Import spluscalib packages

import utils as ut

################################################################################
# Read parameters

if __name__ == "__main__":
    cprint("""
    ************************************************************************
    *                                                                      *
    *                   Starting the calibration pipeline                  *
    *                                                                      *
    ************************************************************************
    """, color = "cyan")

    cwd = os.getcwd()

    try:
        field_list_file = os.path.join(cwd, sys.argv[1])
        config_file = os.path.join(cwd, sys.argv[2])

    except IndexError:
        print(usage_message)
        sys.exit()

    # Read additional arguments (for transfering to other scripts)
    sys_argvs = ""
    if len(sys.argv) >= 3:
        for i in range(3, len(sys.argv)):
            sys_argvs += f" {sys.argv[i]}"

    pipeline_path = os.path.split(__file__)[0]

    cprint(config_file, color = "white", attrs=["dark"])
    cprint("******* reading the configuration file *******", color = "yellow")
    conf = ut.pipeline_conf(config_file)

    ############################################################################
    # Create save path directory

    ut.makedir(conf['save_path'])
    ut.makedir(conf['run_path'])

    logs_path = os.path.join(conf['run_path'], 'logs')
    ut.makedir(logs_path)

    ############################################################################
    # Initiate log file

    log_file_name = os.path.join(logs_path, 'pipeline.log')
    log_file_name = ut.gen_logfile_name(log_file_name)
    log_file = os.path.join(conf['run_path'], log_file_name)

    with open(log_file, "w") as log:
        log.write("")

    ############################################################################
    # Reading parameters

    print("\n\n")

    ut.printlog("*********** Reading configuratrion file **********", log_file, 
                color = "yellow")

    for param in list(conf.keys()):
        ut.printlog(f"{param}: {conf[param]}", log_file, 
                    color = "blue")

    print("\n\n")


    ############################################################################
    # Get sshpass

    if conf["images_sshpass"] and ('copy_images' in conf['run_steps']):
        ut.printlog("*********** Requesting ssh password **********", log_file,
                    color = "yellow")

        ut.printlog(f"ssh IP: {conf['sshpass_ip']}", log_file)
        ut.printlog(f"ssh user: {conf['sshpass_user']}", log_file)
        ut.printlog(f"ssh path: {conf['sshpass_path']}", log_file)

        sshpass = getpass.getpass("enter ssh password:")

    else:
        sshpass = ""

    ############################################################################
    # Reading field list

    ut.printlog("*********** Reading field list **********", log_file,
            color = "yellow")

    if '--onefield' in sys.argv:
        fields = [sys.argv[1]]
    else:
        fields = ut.load_field_list(field_list_file)

    ut.printlog(f"Running the pipeline for fields:", log_file, color = "yellow")
    ut.printlog(f"{fields}", log_file, 
                color = "yellow", attrs = ["bold"])

    ############################################################################
    # Running pipeline for each field

    for field in fields:

        ut.printlog(f"""
        ************************************************************************
        *                                                                      *
        *                Working on field {field:37}*
        *                                                                      *
        ************************************************************************
        """, log_file, color = "cyan", attrs = ["bold"])

        #################
        # Make field path
        field_path = os.path.join(conf['run_path'], field)
        logs_path = os.path.join(field_path, 'logs')

        field_images_path = os.path.join(field_path, 'Images')
        
        if "--skip_missing_images" in sys.argv:
            source_images_path = os.path.join(conf["path_to_images"], field)
            if not os.path.exists(source_images_path):
                ut.printlog(f"{field} images not found. Skipping to next field\n\n",
                            log_file, color = "white", attrs = ["dark"])
                continue

        if not os.path.exists(field_path):
            ut.makedir(field_path)
            ut.printlog(f"Created directory {field_path}.", log_file,
                        color = "green", attrs=["bold"])

            ut.makedir(logs_path)
            ut.printlog(f"Created directory {logs_path}.", log_file,
                        color = "green", attrs=["bold"])
            
        else:
            ut.printlog(f"Directory {field_path} already exists.", log_file,
                        color = "white", attrs=["bold", "dark"])

        
        print("")

        ###################
        # Copy files already present in save_path
        
        if conf['run_path'] != conf['save_path']:
            field_save_path = os.path.join(conf['save_path'], field)
            cmd = f"rsync --update -haz --progress {field_save_path} {conf['run_path']}"
            ut.printlog(cmd, log_file, color = "blue")
            os.system(cmd)
            print("")

        ###################
        # Prepare field log

        log_field_name = os.path.join(logs_path, f'{field}.log')
        log_field_name = ut.gen_logfile_name(log_field_name)
        log_field_file = os.path.join(conf['run_path'], log_field_name)

        with open(log_file, "w") as log:
            log.write("")

        # Make backup of config file
        cmd = f"cp {config_file} {logs_path}"
        ut.printlog(cmd, log_field_file, color = "green")
        os.system(cmd)

        # Run steps

        ########################################################################
        # Copy local images
        if 'local_path' in conf:
            if conf["local_path"] and ('copy_local_images' in conf['run_steps']):
                ut.printlog("*********** Copying local files **********", log_file, color = "yellow")

                script = os.path.join(pipeline_path,'steps','copy_images.py')
                cmd = f'python3 {script} {field} {conf_file} {sshpass} {sys_argvs}'

                ut.printlog(cmd, log_field_file,
                            color = "blue", on_color = "on_white")
                out = os.popen(cmd).read()
                ut.printlog(out, log_field_file, color = "white", on_color = "on_white")

                print("\n\n")
        
        # Copy images
        if 'copy_images' in conf['run_steps']:

            script = os.path.join(pipeline_path,'steps','copy_images.py')
            cmd = f'python3 {script} {field} {config_file} {sshpass} {sys_argvs}'

            if conf["images_sshpass"]:
                cmd_hidepass = cmd.replace(sshpass, "*" * len(sshpass))
            else:
                cmd_hidepass = cmd

            ut.printlog(cmd_hidepass, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")


        ############
        # Check fits
        fits_check = ut.check_fits_consistency(logs_path = logs_path, 
                                            images_path = field_images_path)

        if conf['pause_on_warnings']:
            if fits_check is None:
                print()
                print(("You can disable the pause on warnings option by "
                    "including the following line in the config file:"))
                print()
                ut.termcolor.cprint("pause_on_warnings                False", 
                                    color="blue")
                print()
                ut.termcolor.cprint("Check warning!!!", color="red")
                ask_continue = input('Press enter to continue.')


        ########################################################################
        # Run the photometry
        if 'photometry_single' in conf['run_steps']:

            final_file = os.path.join(field_path, 'Photometry', 'single', 
                                      'master',
                                  f"{field}_master_photometry_only_single.fits")

            if not os.path.exists(final_file):
                script = os.path.join(pipeline_path,'steps',
                'photometry_single.py')
                cmd = f'python3 {script} {field} {config_file}'
                ut.printlog(cmd, log_field_file, 
                            color = "blue", on_color = "on_white")
                os.system(cmd)

                print("\n\n")

            else:
                ut.printlog((f"File {final_file} already exists.\n"
                            f"Skipping single mode photometry for {field}.\n"),
                            log_file, color = "grey", on_color = "on_white")

        if 'photometry_dual' in conf['run_steps']:

            final_file = os.path.join(field_path, 'Photometry', 'dual', 
            'master',
                                    f"{field}_master_photometry_only_dual.fits")

            if not os.path.exists(final_file):
                script = os.path.join(pipeline_path, 'steps', 
                                      'photometry_dual.py')
                cmd = f'python3 {script} {field} {config_file}'
                ut.printlog(cmd, log_field_file,
                            color = "blue", on_color = "on_white")
                os.system(cmd)

                print("\n\n")

            else:
                ut.printlog((f"File {final_file} already exists.\n"
                            f"Skipping dual mode photometry for {field}.\n"),
                            log_file, color = "grey", on_color = "on_white")


        if 'photometry_aperimages' in conf['run_steps']:

            final_file = os.path.join(field_path, 'Photometry', 'dual', 
                                      'detection',
                                    f"{field}_detection.aperPETRO.fits.fz")

            if not os.path.exists(final_file):
                script = os.path.join(pipeline_path, 'steps',
                                    'photometry_aperimages.py')
                cmd = f'python3 {script} {field} {config_file}'
                ut.printlog(cmd, log_field_file,
                            color = "blue", on_color = "on_white")
                os.system(cmd)

                print("\n\n")

            else:
                ut.printlog((f"File {final_file} already exists.\n"
                            f"Skipping .aper images generation for {field}.\n"),
                            log_file, color = "grey", on_color = "on_white")


        if 'photometry_res' in conf['run_steps']:
            
            final_filt = conf['filters'][-1]

            final_file = os.path.join(field_path, 'Photometry', 'dual', 
                                      'catalogs',
                               f"res_crossmatch_check_{field}_{final_filt}.txt")

            if not os.path.exists(final_file):
                script = os.path.join(pipeline_path, 'steps', 
                                      'photometry_res.py')
                cmd = f'python3 {script} {field} {config_file}'
                ut.printlog(cmd, log_field_file,
                            color = "blue", on_color = "on_white")
                os.system(cmd)

                print("\n\n")

            else:
                ut.printlog((f"File {final_file} already exists.\n"
                         f"Skipping restricted mode photometry for {field}.\n"),
                            log_file, color = "grey", on_color = "on_white")


        if 'photometry_psf' in conf['run_steps']:

            final_file = os.path.join(field_path, 'Photometry', 'psf', 'master',
                                    f"{field}_master_photometry_only_psf.fits")

            if not os.path.exists(final_file):
                script = os.path.join(pipeline_path, 'steps', 
                                      'photometry_psf.py')
                cmd = f'python3 {script} {field} {config_file}'
                ut.printlog(cmd, log_field_file,
                            color = "blue", on_color = "on_white")
                os.system(cmd)

                print("\n\n")

            else:
                ut.printlog((f"File {final_file} already exists.\n"
                            f"Skipping psf photometry for {field}.\n"),
                            log_file, color = "grey", on_color = "on_white")

        if 'correction_xy' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 'correction_xy.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'correction_aper' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 'correction_aper.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'photometry_id' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 'photometry_ID.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'photometry_master' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'photometry_master.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        ########################################################################
        # Crossmatch with reference

        if 'crossmatch' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 'crossmatch.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        ########################################################################
        # Perform calibration

        if 'calibration_gaiaXPSP' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_gaiaXPSP.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'calibration_external' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_external.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'calibration_stloc' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_stloc.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'calibration_internal' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_internal.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'calibration_gaiascale' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_gaiascale.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if 'calibration_diagnostic' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_diagnostic.py')
            cmd = f'python3 {script} {field} {config_filele}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        # It only needs to check for calibration_external to know if any 
        # calibration is being run.
        if (('calibration_external' in conf['run_steps']) or
            ('calibration_gaiaXPSP' in conf['run_steps'])):

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_finalzp.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        if (('calibration_external' in conf['run_steps']) or
            ('calibration_gaiaXPSP' in conf['run_steps'])):

            script = os.path.join(pipeline_path, 'steps', 'check_xy_zp.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        ########################################################################
        # Generate final catalogs

        if 'calibration_catalog' in conf['run_steps']:

            script = os.path.join(pipeline_path, 'steps', 
                                  'calibration_catalog.py')
            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        ########################################################################
        # Generate quality checks

        if 'quality_check' in conf['run_steps']:

            if "--dual_quality_check" in sys.argv:
                script = os.path.join(pipeline_path, 'quality_check.py')
            else:
                if conf['calibration_photometry'].lower() in ['single', 'dual']:
                    script = os.path.join(pipeline_path, 'quality_check.py')
                elif conf['calibration_photometry'].lower() in ['psf']:
                    script = os.path.join(pipeline_path, 'quality_check_PSF.py')

            cmd = f'python3 {script} {field} {config_file}'
            ut.printlog(cmd, log_field_file,
                        color = "blue", on_color = "on_white")
            os.system(cmd)

            print("\n\n")

        ########################################################################
        # Plot mosaics

        if 'plot_mosaic_calib' in conf['run_steps']:
            suffix = ut.calibration_suffix(conf)
            mosaic_file = os.path.join(field_path, f"Calibration_{suffix}",
                                        f"{field}_{suffix}_mosaic.png")

            plot_mosaic = True
            if os.path.exists(mosaic_file):
                if not conf["overwrite_mosaic_plot"]:
                    plot_mosaic = False

            if plot_mosaic:
                script = os.path.join(pipeline_path,
                                    'steps',
                                    'plot_mosaic_calib_v3.py')
                cmd = f'python3 {script} {field} {config_file}'
                ut.printlog(cmd, log_field_file,
                            color = "blue", on_color = "on_white")
                os.system(cmd)

            else:
                ut.printlog("Mosaic plot already exists and configuration is "
                            "set not to overwrite.", log_field_file)

            print("\n\n")

        ########################################################################
        # Do final checks
            
        script = os.path.join(pipeline_path,
                                    'steps',
                                    'final_checks.py')
        cmd = f'python3 {script} {field} {config_file}'
        ut.printlog(cmd, log_field_file,
                    color = "blue", on_color = "on_white")
        os.system(cmd)
            
        ########################################################################

        ###################
        # Remove fits files

        if conf['remove_fits']:

            for filt in conf['filters']:
                image_name = f'{field}_{filt}_swp.fz'
                image_fz = os.path.join(field_images_path, image_name)
                image_fits = image_fz.replace(".fz", ".fits")

                # Only remove .fits if .fz exists:
                if os.path.exists(image_fz) and os.path.exists(image_fits):

                    ut.printlog(f"Removing image {image_fits}", log_field_file,
                                color = "red")

                    cmd = f"rm {image_fits}"
                    ut.printlog(cmd, log_field_file, color = "yellow")
                    os.system(cmd)

                if conf['use_weight']:

                    weight_fz = image_fz.replace(".fz", "weight.fz")
                    weight_fits = weight_fz.replace(".fz", ".fits")

                    if os.path.exists(weight_fz) and os.path.exists(weight_fits):
                        ut.printlog(f"Removing weight {weight_fits}",
                                    log_field_file, color = "yellow")

                        cmd = f"rm {weight_fits}"
                        ut.printlog(cmd, log_field_file, color = "red")
                        os.system(cmd)

        #################################
        # Remove all images, including fz

        if conf["remove_images"]:
            ut.printlog(f"Removing images, including .fz",
                        log_field_file, color = "yellow")

            cmd = f"rm {field_images_path}/*.fz"
            ut.printlog(cmd, log_field_file, color = "red", attrs = ["bold"])
            os.system(cmd)

            cmd = f"rm {field_images_path}/*.fits"
            ut.printlog(cmd, log_field_file, color = "red", attrs = ["bold"])
            os.system(cmd)

        #########################
        # Sync run_path and save_path field to save_path
        if conf['save_path'] != conf['run_path']:
            
            cmd = f"rsync --update -haz --progress {field_path} {conf['save_path']}"
            ut.printlog(cmd, log_field_file, color = "blue")
            os.system(cmd)
            
            cmd = f"rm -r {field_path}"
            ut.printlog(cmd, log_field_file, color = "red", attrs=["bold"])
            os.system(cmd)
        
