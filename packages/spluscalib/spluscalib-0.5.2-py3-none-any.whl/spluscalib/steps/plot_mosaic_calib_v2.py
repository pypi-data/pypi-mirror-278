# -*- coding: utf-8 -*-

# ******************************************************************************
#                          S-PLUS CALIBRATION PIPELINE
#                             plot_mosaic_calib.py
#            Produces the diagnostic plots in the end of the pipeline
# ******************************************************************************

"""
Produces the diagnostic plots in the end of the pipeline

The S-PLUS field is given as the first command line argument. Configurations
are set in the config file, given as the second command line argument.

--------------------------------------------------------------------------------

Deprecated - see plot_mosaic_calib_v3

----------------
"""

################################################################################
# Import external packages

from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import os
import sys
import copy

from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import BaseEclipticFrame
from astropy.time import Time
from matplotlib.patches import Polygon
import matplotlib.image as mpimg
import matplotlib.transforms as mtransforms
import matplotlib.colors as pltcolors
from scipy import stats

import cartopy.crs as ccrs

################################################################################
# Import spluscalib packages

steps_path = os.path.split(__file__)[0]
pipeline_path = os.path.split(steps_path)[0]
spluscalib_path = os.path.split(pipeline_path)[0]

sys.path.append(spluscalib_path)

from spluscalib import utils as ut

################################################################################
# Read parameters

field = sys.argv[1]
config_file = sys.argv[2]

conf = ut.pipeline_conf(config_file)

################################################################################
# Standard parameters

path_to_filters = os.path.join(spluscalib_path, "stellarlibrary", "resources",
                               "filters")

splus_footprint_file = os.path.join(pipeline_path, "steps", "resources",
                                    "splus_footprint.csv")
splus_footprint = pd.read_csv(splus_footprint_file)


logo_file = os.path.join(pipeline_path, "steps", "resources", "logo.png")
logo = mpimg.imread(logo_file)

color1 = "#111111"
color2 = "#FFFFFF"
color3 = "#DB1D1D"
color4 = "#4821D6"
color5 = "#F1CE09"
color6 = "#59a3fa"
color0 = "#000000"

DRs_path = os.path.join(pipeline_path, "steps",
                        "resources", "splus_drs")

DRs = {"DR1": os.path.join(DRs_path, "dr1.csv"),
       "DR2": os.path.join(DRs_path, "dr2.csv"),
       "DR3": os.path.join(DRs_path, "dr3.csv"),
       "DR4": os.path.join(DRs_path, "dr4.csv")}

obs_database_file  = conf["obs_database"]
obs_database = pd.read_csv(obs_database_file, encoding='latin-1',
                           low_memory=False)

obs_database_finaldate = conf["obs_database_finaldate"]
obs_database_finaldate = Time(obs_database_finaldate,
                              format='isot', scale='utc')

try:
    final_zp_dist_file = conf["final_zp_dist_ref"]
    final_zp_dist = pd.read_csv(final_zp_dist_file)
except:
    final_zp_dist_file = None
    final_zp_dist = None

try:
    gaia_zp_dist_file  = conf["gaia_zp_dist_ref"]
    gaia_zp_dist = pd.read_csv(gaia_zp_dist_file)
except:
    gaia_zp_dist_file = None
    gaia_zp_dist = None

filters_splus_order = {"SPLUS_U": 0,
                       "SPLUS_F378": 1,
                       "SPLUS_F395": 2,
                       "SPLUS_F410": 3,
                       "SPLUS_F430": 4,
                       "SPLUS_G": 5,
                       "SPLUS_F515": 6,
                       "SPLUS_R": 7,
                       "SPLUS_F660": 8,
                       "SPLUS_I": 9,
                       "SPLUS_F861": 10,
                       "SPLUS_Z": 11}

filters_gaia_order = {"GAIA_BP": 0,
                      "GAIA3_BP": 0,
                      "GAIA_G": 3,
                      "GAIA3_G": 3,
                      "GAIA_RP": 6,
                      "GAIA3_RP": 6}

filters_splus     = conf["filters"]
for i in range(len(filters_splus)):
    filters_splus[i] = "SPLUS_" + filters_splus[i]

filters_ref       = conf["external_sed_fit"]
filters_gaia      = conf["gaiascale_sed_pred"]
filters_splus_ext = conf["external_sed_pred"]
filters_xpsp      = conf["gaiaxpsp_sed_pred"]

try:
    filters_splus_stlocus = conf["stellar_locus_fit"]
except:
    filters_splus_stlocus = []

################################################################################
# Read filt info cols

filt_info_cols_2 = pd.read_csv(os.path.join(pipeline_path, "steps", "resources",
                                            "filt_info_cols_2.csv"))

rename = {}
for col in filt_info_cols_2.columns:
    rename[col] = col.replace(" ", "")

filt_info_cols_2.rename(columns=rename, inplace=True)

################################################################################
# Read isochrones

isoc_path = conf["isochrones_path"]
isoc1e8 = pd.read_csv(os.path.join(isoc_path, "isoc1e8.dat"),
                      delim_whitespace = True, escapechar = "#")
isoc1e9 = pd.read_csv(os.path.join(isoc_path, "isoc1e9.dat"),
                      delim_whitespace = True, escapechar = "#")
isoc1e10 = pd.read_csv(os.path.join(isoc_path, "isoc1e10.dat"),
                       delim_whitespace = True, escapechar = "#")

isocs = [isoc1e8, isoc1e9, isoc1e10]

################################################################################
# Get field info

field_path = os.path.join(conf['save_path'], field)
calib = conf["calibration_name"]
suffix = ut.calibration_suffix(conf)

calibration = conf["calibration_name"]
photometry = conf["calibration_photometry"]
reduction = conf["reduction"]
reference = conf["reference_catalog"]
extinction = conf["extinction_correction"]

################################################################################
# Assign field type
def assign_tile_type(tile):

    if "STRIPE" in tile:
        type = "STRIPE82"

    elif "SPLUS-s" in tile:
        type = "SPLUS-s"

    elif "SPLUS-n" in tile:
        type = "SPLUS-n"

    elif "HYDRA" in tile:
        type = "HYDRA"

    elif "SHAPLEY" in tile:
        type = "CHANCES"

    elif "LUPUS" in tile:
        type = "LUPUS"

    elif ("MC" in tile) and ("MCT" not in tile):
        type = "MC"

    elif "SPLUS-d" in tile:
        type = "SPLUS-d"

    elif "SPLUS-b" in tile:
        type = "SPLUS-b"

    elif (tile[0] == "A") and ("Ast" not in tile) and ("Abell" not in tile):
        type = "CHANCES"

    elif "NGC" in tile:
        type = "NGC"

    elif "Ast" in tile:
        type = "Ast"

    elif "Abell" in tile:
        type = "CHANCES"

    elif "CN2020B78" in tile:
        type = "CN2020B78"

    elif "CN2019A93" in tile:
        type = "CN2019A93"

    elif "SFCG" in tile:
        type = "SFCG"

    elif "ZWII108" in tile:
        type = "CHANCES"

    else:
        type = tile

    return type

field_type = assign_tile_type(field)
conf["field_type"] = field_type

field_type

################################################################################
# Get position of the field

try:
    img_R = os.path.join(field_path, "Images", f"{field}_R_swp.fz")
    hdr_R = fits.open(img_R)[1].header

    field_RA = np.around(hdr_R["CRVAL1"], 2)
    field_DEC = np.around(hdr_R["CRVAL2"], 2)

    c = SkyCoord(field_RA, field_DEC, frame='icrs', unit='deg')
    field_RAhms = f"{c.ra.hms[0]:02.0f}:{c.ra.hms[1]:02.0f}:{c.ra.hms[2]:04.1f}"
    field_DECdms = f"{c.dec.dms[0]:+03.0f}:{c.dec.dms[1]:02.0f}:{c.dec.dms[2]:04.1f}"

except FileNotFoundError:
    field_RA = np.nan
    field_DEC = np.nan

    field_RAhms = f"NaN"
    field_DECdms = f"NaN"

################################################################################
# Read catalogs
calib_phot = conf["calibration_photometry"]

detections_file  = os.path.join(field_path, "Crossmatch",
                                f"{field}_SPLUS_{calib_phot}.fits")

detections = fits.open(detections_file)[1].data

################################################
# Load crossmatches ############################

gaia_xmatch_file = os.path.join(field_path, f"Calibration_{calib}",
                                "gaiascale", "splus_gaia.fits")

gaia_xmatch = fits.open(gaia_xmatch_file )[1].data


gaiaxpsp_xmatch_file = os.path.join(field_path, f"Calibration_{calib}",
                                "gaiaXPSP",
                                f"{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.cat")

gaiaxpsp_xmatch = ut.load_data(gaiaxpsp_xmatch_file)


################################################
########


########
if 'photometry_dual' in conf['run_steps']:
    x0y0l_file = os.path.join(field_path, "Photometry", "dual",
                              "detection", f"{field}_detection_x0y0l.csv")

try:
    x0y0l_data = pd.read_csv(x0y0l_file)
except FileNotFoundError:
    x0y0l_data = None

########
# EBV correction catalog
ref_xmatch_name  = ut.crossmatch_catalog_name(field, conf)
ref_xmatch_file  = os.path.join(field_path, "Crossmatch", ref_xmatch_name)
extinction = conf["extinction_correction"]
ebv_xmatch_file = ref_xmatch_file.replace(".fits",
                                          f"_radecebv_{extinction}.csv")
ebv_data = pd.read_csv(ebv_xmatch_file)

try:
    stlocus_reference_file = conf["stellar_locus_reference"]
    stlocus_reference = pd.read_csv(stlocus_reference_file,
                                    delim_whitespace = True, escapechar = "#")
except FileNotFoundError:
    stlocus_reference = None

if conf['add_gaiascale_to_final_zp']:
    catalog_file = os.path.join(field_path, f"Calibration_{calib}", "gaiascale",
                                f"{field}_mag_gaiascale.cat")
else:
    catalog_file = os.path.join(field_path, f"Calibration_{calib}", "external",
                                f"{field}_mag_ext.cat")

catalog = pd.read_csv(catalog_file, delim_whitespace = True, escapechar = "#")

models_file = conf["path_to_models"]
models = pd.read_csv(models_file, delim_whitespace = True, escapechar = "#")

########
# ZP data

zp_xpsp_data_file = os.path.join(field_path, f"Calibration_{calib}", "gaiaXPSP",
                                f"{field}_SPLUS_{calib_phot}_gaiaXPSP_phot.cat")

zp_ext_data_file = os.path.join(field_path, f"Calibration_{calib}", "external",
                                f"{field}_ref_sed_fit.cat")
zp_gsc_data_file = os.path.join(field_path, f"Calibration_{calib}", "gaiascale",
                                f"{field}_gaiascale_sed_fit.cat")

zp_xpsp_data = pd.read_csv(zp_xpsp_data_file,
                          delim_whitespace = True, escapechar = "#")
zp_ext_data = pd.read_csv(zp_ext_data_file,
                          delim_whitespace = True, escapechar = "#")
zp_gsc_data = pd.read_csv(zp_gsc_data_file,
                          delim_whitespace = True, escapechar = "#")

zp_xpsp_file = os.path.join(field_path, f"Calibration_{calib}", "gaiaXPSP",
                           f"{field}_gaiaxpsp_tmp.zp")
zp_ext_file = os.path.join(field_path, f"Calibration_{calib}", "external",
                           f"{field}_external_tmp.zp")
zp_gsc_file = os.path.join(field_path, f"Calibration_{calib}", "gaiascale",
                           f"{field}_gaiascale_gaia.zp")
zp_gsc_mean_file = os.path.join(field_path, f"Calibration_{calib}", "gaiascale",
                           f"{field}_gaiascale_splus.zp")
zp_final_file = os.path.join(field_path, f"Calibration_{calib}",
                           f"{field}_final.zp")

zp_xpsp = ut.zp_read(zp_xpsp_file)
zp_ext = ut.zp_read(zp_ext_file)
zp_gsc = ut.zp_read(zp_gsc_file)
zp_gsc_mean = ut.zp_read(zp_gsc_mean_file)
zp_final = ut.zp_read(zp_final_file)
    
########
# xychecks

xychecks_path = os.path.join(field_path, f"Calibration_{calib}", "xycheck")
xychecks = {}

for filt in filters_splus:
    xychecks[filt] = np.load(os.path.join(xychecks_path,
                     f"xy_check_{filt.replace('SPLUS_', '')}.npy"))

################################################################################
# Read info from images headers

# Extract images headers
images_path = os.path.join(field_path, "Images")
def rms(x):
   return np.sqrt(np.mean(x ** 2))

# Create hdr info df
hdrs_info_df = {}
hdrs_info_df["FIELD"] = []
hdrs_info_df["FILTER"] = []
hdrs_info_df["LAMBDAeff"] = []
hdrs_info_df["ALAMBDA_AV"] = []
hdrs_info_df["REDUCTION"] = []
hdrs_info_df["REDUCTION_DATE"] = []
hdrs_info_df["NCOMBINE"] = []
hdrs_info_df["EXPTIMEind"] = []
hdrs_info_df["EXPTIMEtot"] = []
hdrs_info_df["FWHMSEXT"] = []
hdrs_info_df["FWHMSRMS"] = []
hdrs_info_df["GAIN"] = []
hdrs_info_df["AIRMASS_MEAN"] = []
hdrs_info_df["AIRMASS_SDEV"] = []
hdrs_info_df["IMAGES"] = []

hdrs_info_df["offset_inst_mag"] = []
hdrs_info_df["external_sed_fit"] = []
hdrs_info_df["external_sed_pred"] = []
hdrs_info_df["stellar_locus_fit"] = []
hdrs_info_df["internal_sed_fit"] = []
hdrs_info_df["internal_sed_pred"] = []
hdrs_info_df["offset_to_splus_refcalib"] = []
hdrs_info_df["gaiascale_sed_fit"] = []
hdrs_info_df["gaiascale_sed_pred"] = []

# AIRMASS comes from the obs database
f_field = obs_database["OBJECT"] == field

field_images_hdrs = {}

for filt in filters_splus:
    filt_2 = filt.replace("SPLUS_", "")
    image_file = os.path.join(images_path, f"{field}_{filt_2}_swp.fz")

    try:
        header = fits.open(image_file)[1].header
    except FileNotFoundError:
        header = {}
        header_keys = ["DATE", "NCOMBINE", "GAIN", "EXPTIME", "TEXPOSED",
                       "HIERARCH MAR PRO FWHMSEXT", "HIERARCH MAR PRO FWHMSRMS",
                       "HIERARCH OAJ PRO FWHMSEXT", "HIERARCH MAR PRO FWHMSRMS"]

        for key in header_keys:
            header[key] = np.nan

    field_images_hdrs[filt] = header


for filt in filters_splus:
    hdr = field_images_hdrs[filt]
    hdrs_info_df["FIELD"].append(field)
    hdrs_info_df["FILTER"].append(filt)

    hdrs_info_df["LAMBDAeff"].append(ut._lambda_eff[filt])
    hdrs_info_df["ALAMBDA_AV"].append(ut._Alambda_Av[filt])

    hdrs_info_df["REDUCTION"].append(conf["reduction"])

    try:
        hdrs_info_df["REDUCTION_DATE"].append(Time(hdr["DATE"],
                                                   format='isot', scale='utc'))
    except ValueError:
        hdrs_info_df["REDUCTION_DATE"].append(np.nan)

    N = hdr["NCOMBINE"]
    hdrs_info_df["NCOMBINE"].append(N)

    hdrs_info_df["GAIN"].append(hdr["GAIN"])

    f_filt = obs_database["FILTER"] == filt.replace("SPLUS_", "")
    obs_database[f_field & f_filt]

    airmass = obs_database.loc[f_field & f_filt, "AIRMASS"].values
    try:
        hdrs_info_df["AIRMASS_MEAN"].append(np.mean(airmass))
    except ZeroDivisionError:
        hdrs_info_df["AIRMASS_MEAN"].append(np.nan)
    except TypeError:
        hdrs_info_df["AIRMASS_MEAN"].append(np.nan)

    try:
        hdrs_info_df["AIRMASS_SDEV"].append(np.std(airmass))
    except ZeroDivisionError:
        hdrs_info_df["AIRMASS_SDEV"].append(np.nan)
    except TypeError:
        hdrs_info_df["AIRMASS_SDEV"].append(np.nan)

    if conf['reduction'] == "MAR":

        # Get list of exposure times
        try:
            exp_list = []
            for i in range(N):
                exp_list.append(str(hdr[f"EXP_{i}"]))

            # Get string of unique values
            exp_list = list(set(exp_list))
            indEXPTIME = ", ".join(exp_list)
            hdrs_info_df["EXPTIMEind"].append(indEXPTIME)

            images = []
            for i in range(N):
                images.append(hdr[f"COMB_{i}"].replace("proc_", ""))

            hdrs_info_df["IMAGES"].append(images)


        except KeyError:
            hdrs_info_df["EXPTIMEind"].append(np.nan)
            hdrs_info_df["IMAGES"].append(np.nan)
        except TypeError:
            hdrs_info_df["EXPTIMEind"].append(np.nan)
            hdrs_info_df["IMAGES"].append(np.nan)

        # Get total exptime
        hdrs_info_df["EXPTIMEtot"].append(hdr["EXPTIME"])
        hdrs_info_df["FWHMSEXT"].append(hdr["HIERARCH MAR PRO FWHMSEXT"])
        hdrs_info_df["FWHMSRMS"].append(hdr["HIERARCH MAR PRO FWHMSRMS"])


    elif conf['reduction'] == 'JYPE':
        hdrs_info_df["EXPTIMEind"].append(np.nan)

        hdrs_info_df["EXPTIMEtot"].append(hdr["TEXPOSED"])
        hdrs_info_df["FWHMSEXT"].append(hdr["HIERARCH OAJ PRO FWHMSEXT"])
        hdrs_info_df["FWHMSRMS"].append(hdr["HIERARCH OAJ PRO FWHMSRMS"])

        hdrs_info_df["IMAGES"].append(np.nan)

    try:
        if conf["offset_inst_mag"].lower() != "none":
            inst_offset = ut.zp_read(conf["offset_inst_mag"])
            hdrs_info_df["offset_inst_mag"].append(inst_offset[filt])
        else:
            hdrs_info_df["offset_inst_mag"].append(None)
    except KeyError:
        hdrs_info_df["offset_inst_mag"].append(None)
    except FileNotFoundError:
        hdrs_info_df["offset_inst_mag"].append("ERR")

    try:
        if conf["offset_to_splus_refcalib"].lower() != "none":
            calib_offset = ut.zp_read(conf["offset_to_splus_refcalib"])
            hdrs_info_df["offset_to_splus_refcalib"].append(calib_offset[filt])
        else:
            hdrs_info_df["offset_to_splus_refcalib"].append(None)
    except KeyError:
        hdrs_info_df["offset_to_splus_refcalib"].append(None)
    except FileNotFoundError:
        hdrs_info_df["offset_to_splus_refcalib"].append("ERR")

    for step in ["external_sed_fit", "stellar_locus_fit",
                 "internal_sed_fit","gaiascale_sed_fit"]:
        try:
            if filt in conf[step]:
                hdrs_info_df[step].append(True)
            else:
                hdrs_info_df[step].append(False)
        except KeyError:
            hdrs_info_df[step].append(False)

    for step, step2 in zip(["external_sed_fit",  "internal_sed_fit",
                            "gaiascale_sed_fit"],
                           ["external_sed_pred",  "internal_sed_pred",
                            "gaiascale_sed_pred"]):
        try:
            if filt in conf[step2]:
                hdrs_info_df[step2].append(True)
            else:
                if filt in conf[step]:
                    hdrs_info_df[step2].append(None)
                else:
                    hdrs_info_df[step2].append(False)
        except KeyError:
            hdrs_info_df[step2].append(False)


hdrs_info_df = pd.DataFrame(hdrs_info_df)

################################################################################
# Get filters colors

def wavelength_to_hex(wavelength, gamma=0.8):
    '''This converts a given wavelength of light to an
    approximate hex color value. The wavelength must be given
    in angstrons in the range from 3000 A through 10000 A

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength) / 10.

    if 200 <= wavelength < 300:
        attenuation = 0.3 + 0.7 * (wavelength - 200) / (440 - 200)
        R = ((-(wavelength - 440) / (440 - 200)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 300 <= wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 300) / (440 - 300)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 440 <= wavelength <= 490:
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif 490 <= wavelength <= 510:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif 580 <= wavelength <= 645:
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif 645 <= wavelength <= 1000:
        attenuation = 0.3 + 0.7 * (1000 - wavelength) / (1000 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0
    R *= 255
    G *= 255
    B *= 255

    color = f'#{int(R):02X}{int(G):02X}{int(B):02X}'
    return color

# Get colors for all filters
filters_colors = {}

all_filters = filters_ref + filters_splus + filters_gaia
for filt in all_filters:
    lambda_ref = ut._lambda_ref[filt]
    filters_colors[filt] = wavelength_to_hex(lambda_ref)

################################################################################
# Mosaic
#            0     1     2     3     4     5     6     7     8     9     A     B     C     D     E
mosaic = [['00', '00', '00', '03', '03', '05', '05', '05', '05', '09', '09', '09', '09', '09', '09', '0F', '0F', '0F', '0I', '0I', '0I'], # 0
          ['10', '10', '10', '13', '14', '14', '14', '14', '14', '09', '09', '09', '09', '09', '09', '0F', '0F', '0F', '1I', '1I', '1I'], # 1
          ['10', '10', '10', '13', '14', '14', '14', '14', '14', '09', '09', '09', '09', '09', '09', '0F', '0F', '0F', '1I', '1I', '1I'], # 2
          ['10', '10', '10', '33', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F', '3F', '3F', '3I', '3I', '3I'], # 3
          ['40', '40', '40', '33', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F', '3F', '3F', '3I', '3I', '3I'], # 4
          ['50', '50', '50', '53', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E', '3F', '3F', '3F', '5I', '5I', '5I'], # 5
          ['50', '50', '50', '63', '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D', '6E', '6F', '6F', '6F', '5I', '5I', '5I'], # 6
          ['70', '70', '70', '73', '74', '75', '76', '77', '78', '79', '7A', '7B', '7C', '7D', '7E', '6F', '6F', '6F', '7I', '7J', '7K'], # 7
          ['70', '70', '70', '83', '84', '85', '86', '87', '88', '89', '8A', '8B', '8C', '8D', '8E', '6F', '6F', '6F', '8I', '8I', '8I'], # 8
         ]

################################################################################
# Define plots

def plot_DR(field, ax, label_color, conf, former_DRs):

    field_drs = []

    for key in former_DRs.keys():
        dr_fields = pd.read_csv(former_DRs[key])["NAME"]

        if field in list(dr_fields):
            field_drs.append(key)
        elif field.replace("-", "_") in list(dr_fields):
            field_drs.append(key)
        elif field.replace("_", "-") in list(dr_fields):
            field_drs.append(key)

    if conf["data_release_name"] not in list(former_DRs.keys()):
        field_drs.append(conf["data_release_name"])

    box_l = 0.09
    box_h = 0.12
    box_cy = 0.25
    box_cx = 0.5 - (len(field_drs)-1) * box_l/2
    #box_cx = 0.21

    for dr in field_drs:
        if dr == conf["data_release_name"]:
            color = label_color
        else:
            color = "#666666"

        ax.fill_between([box_cx-box_l/2, box_cx+box_l/2],
                         [box_cy-box_h/2, box_cy-box_h/2],
                         [box_cy+box_h/2, box_cy+box_h/2],
                         color = color, alpha = 0.3,
                         transform = ax.transAxes)

        ax.text(box_cx, box_cy, dr, ha = "center", va = "center", color = label_color, transform = ax.transAxes, fontsize = 11)
        ax.plot([box_cx-box_l/2, box_cx-box_l/2], [box_cy-box_h/2, box_cy+box_h/2], color = label_color, lw = 0.5, alpha = 0.3, transform = ax.transAxes)
        box_cx += box_l

def plot_sky(field_ra, field_dec, splus_footprint, ax, color_label,
             point_color = "#FFFFFF"):
    ra = np.array(splus_footprint["RA_d"])
    dec = np.array(splus_footprint["DEC_d"])
    ax.scatter(ra, dec, s = 1, marker = '.', alpha = 0.4,
               transform=ccrs.Geodetic(), zorder = 2, color = "#666666")
    ax.invert_xaxis()

    ax.scatter(field_ra, field_dec, marker = 'x', s = 80, alpha = 0.8,
               transform=ccrs.Geodetic(), zorder = 2, color = point_color)

    # Plot paralelos
    for mra in [-180, -150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150, 180]:
        m1_de = np.arange(-90, 90, 0.1)
        m1_ra = np.full(len(m1_de), mra)
        ax.plot(-m1_ra, m1_de, transform=ccrs.Geodetic(), color = color_label,
                lw = 0.5, alpha = 0.1, zorder = -1)

    # plot meridianos
    for pde in [-75, -60, -45, -30, -15, 0, 15, 30, 45, 60, 75]:
        p2_ra = np.arange(-180, 180, 0.1)
        p2_de = np.full(len(p2_ra), pde)
        ax.plot(-p2_ra, p2_de, transform=ccrs.Geodetic(), color = color_label,
                lw = 0.5, alpha = 0.1, zorder = -1)
        
def plot_filters(filter_list, filters_colors, ax, path_to_filters = "",
                 zorder = 1, alpha = 1, legend = False, loc = 9,
                 label_color = "#000000", lambda_eff = None, alambda_av = None):

    if lambda_eff is not None:
        leffmax = lambda_eff[filter_list[-1]]
        ax.text(leffmax+500, 0.05, r"$\lambda_\mathrm{eff}$",
                color = label_color, ha = 'left', va = 'bottom', fontsize = 9,
                alpha = 0.6, zorder = 20)
        ax.text(leffmax+500, 0.2, r"$A_\lambda / A_V$", color = label_color,
                ha = 'left', va = 'bottom', fontsize = 9, alpha = 0.6,
                zorder = 20)


    for filt in filter_list:

        # load data
        filter_data = pd.read_csv(os.path.join(path_to_filters, filt+".dat"),
                                  delim_whitespace=True)

        Norm = np.nanmax(filter_data.iloc[:,1])

        # get color for the plot
        color = filters_colors[filt]

        linewidth = 1

        # plot the filter
        x = filter_data.iloc[:,0]
        y = filter_data.iloc[:,1]/Norm
        x = np.concatenate(([x[0]], x, [list(x)[-1]]))
        y = np.concatenate(([0], y, [0]))

        if zorder != -1:
            ax.fill_between(x, 0, y,
                color = color, zorder = zorder, alpha = 0.3)

            linewidth = 1

        ax.plot(x, y,
                color = color, zorder = zorder, alpha = alpha,
                label = filt, linewidth = linewidth)

        if lambda_eff is not None:
            leff = lambda_eff[filt]
            ax.text(leff, 0.05, f"{leff:.2f}", color = filters_colors[filt],
                    ha = 'center', va = 'bottom', fontsize = 9, zorder = 20)
            ax.plot([leff, leff], [0, 0.04], color = filters_colors[filt],
                    lw = 1)

            AlAv = alambda_av[filt]
            ax.text(leff, 0.2, f"{AlAv:.2f}", color = filters_colors[filt],
                    ha = 'center', va = 'bottom', fontsize = 9, zorder = 20)

    if legend:
        if len(filter_list) <= 6:
            ncol = len(filter_list)
            bbox = (0., 0.55, 1., 0.3)
            ax.set_ylim((-0.3, 1.7))
        else:
            ncol = 4
            bbox = (0., 0., 1., 0.9)
            ax.set_ylim((-0.3, 2))

        ax.legend(loc = loc, bbox_to_anchor=bbox, ncol = ncol, fontsize = 9,
                  labelcolor = label_color, frameon=False)

    else:
        ax.set_ylim((-0.3, 1.2))

    # Plot labels
    ax.text(4000, -0.2, r"4000 $\AA$", ha = "center", color = label_color,
            fontsize = 18, alpha = 0.5)

    for x in range(6000, 12000, 2000):
        ax.text(x, -0.2, x, ha = "center", color = label_color, fontsize = 18,
                alpha = 0.5)

    # Plot ticks
    for x in range(4000, 12000, 2000):
        ax.plot([x,x], [-0.1, 0.0], color = label_color, lw = 0.5, alpha = 0.5)

    for x in range(3000, 11000, 1000):
        ax.plot([x,x], [-0.07, 0.0], color = label_color, lw = 0.5, alpha = 0.4)

    for x in range(3500, 11000, 500):
        ax.plot([x,x], [-0.05, 0], color = label_color, lw = 0.5, alpha = 0.3)

    ax.text(0.98, 0.95, "Filter System", fontsize = 18, color = label_color,
                ha='right', va='top', transform = ax.transAxes)
    # Remove original ticks
    ax.set_yticks([])
    ax.set_xticks([])

    ax.set_xlim((3000, 10600))

def plot_xy_grid(x0y0l_data, ax, conf, line_color = "#00AAFF"):

    #ax.scatter(x, y, color = label_color, s = 1, alpha = 0.05, marker = '.', zorder = -10)

    xbins = conf["XY_correction_xbins"]
    ybins = conf["XY_correction_ybins"]

    u0 = xbins[0]
    v0 = ybins[0]

    lu = xbins[1]-xbins[0]
    lv = ybins[1]-ybins[0]

    Nu = 6+1
    Nv = 6+1

    x0 = x0y0l_data["x0"][0]
    y0 = x0y0l_data["y0"][0]
    angle = x0y0l_data["angle"][0]
    margin = x0y0l_data["margin"][0]

    x0 = x0 + margin
    y0 = y0 + margin

    ##################################
    # Line 0
    L0u = np.linspace(u0, u0+lu, Nu)
    L0v = np.full(Nv, v0)

    # Line 1
    L1u = np.full(Nu, u0+lu)
    L1v = np.linspace(v0, v0+lv, Nv)

    # Line 2
    L2u = np.linspace(u0, u0+lu, Nu)
    L2v = np.full(Nv, v0+lv)

    # Line 3
    L3u = np.full(Nu, u0)
    L3v = np.linspace(v0, v0+lv, Nv)

    ###################################
    # Transform vertices
    L0x = x0 + L0u*np.cos(angle) + L0v*np.sin(angle)
    L0y = y0 - L0u*np.sin(angle) + L0v*np.cos(angle)

    L1x = x0 + L1u*np.cos(angle) + L1v*np.sin(angle)
    L1y = y0 - L1u*np.sin(angle) + L1v*np.cos(angle)

    L2x = x0 + L2u*np.cos(angle) + L2v*np.sin(angle)
    L2y = y0 - L2u*np.sin(angle) + L2v*np.cos(angle)

    L3x = x0 + L3u*np.cos(angle) + L3v*np.sin(angle)
    L3y = y0 - L3u*np.sin(angle) + L3v*np.cos(angle)

    ###################################
    # Plot lines

    # Vertical
    for i in range(Nu):
        ax.plot([L0x[i],L2x[i]], [L0y[i], L2y[i]],
                color = line_color, zorder = 200, lw = 1, alpha = 1)

    # Horizontal
    for i in range(Nv):
        ax.plot([L1x[i],L3x[i]], [L1y[i], L3y[i]],
                color = line_color, zorder = 200, lw = 1, alpha = 1)

    ##################################3
    #ax.set_xlim(0, 11000)
    #ax.set_ylim(0, 11000)

def plot_detections(detections,  ax, label_color, ref_xmatch, xpsp_xmatch,
                    xmatch_color = "#880066", xpsp_color = "#08c902"):

    # Detections
    Ndet = len(detections["X"])
    ax.scatter(detections["X"], detections["Y"], color = label_color, s = 1,
               marker = '.', alpha = 0.2)

    ax.scatter([], [], color = label_color, s = 20, marker = '.', alpha = 0.3,
           label = f"Detections ({Ndet})")

    # SPLUSxReference
    Nref = len(ref_xmatch["X"])
    ref_label = conf["reference_catalog"] + ["Gaia" + conf['gaia_reference']]
    ax.scatter(ref_xmatch["X"], ref_xmatch["Y"], color = xmatch_color, s = 15,
               marker = 'o', alpha = 0.8,
               label = f"{ref_label} ({Nref})")

    # SPLUSxpsp
    Nxpsp = len(xpsp_xmatch["X"])
    ref_label = "GaiaXPSP"
    ax.scatter(xpsp_xmatch["X"], xpsp_xmatch["Y"], color = xpsp_color, s = 7,
               marker = 'o', alpha = 0.8,
               label = f"{ref_label} ({Nxpsp})")

    ax.legend(loc = 9, ncol=2, frameon=False,
              labelcolor = color2, fontsize = 14)

    ax.text(0.5, 0.03, "X [px]", fontsize = 16, color = label_color,
            ha='center', va='center', transform = ax.transAxes)
    ax.text(0.03, 0.5, "Y [px]", rotation = 90, fontsize = 16, color = color2,
            ha='center', va='center', transform = ax.transAxes)

    for x in [1000, 4000, 7000, 10000]:
        ax.text(x, 500, x, fontsize = 14, alpha = 0.5, color = label_color,
                ha='center', va='top')
        ax.plot([x,x], [0, 100], alpha = 0.5, color = label_color)
    for x in np.arange(1000, 11000, 1000):
        ax.plot([x,x], [50, 100], alpha = 0.2, color = label_color)

    for y in [1000, 4000, 7000, 10000]:
        ax.text(500, y, y, rotation = 90, fontsize = 14, alpha = 0.5,
                color = label_color, ha='right', va='center')
        ax.plot([0, 100], [y,y], alpha = 0.5, color = label_color)
    for y in np.arange(1000, 11000, 1000):
        ax.plot([50, 100], [y,y], alpha = 0.2, color = label_color)


    ax.set_xlim(0,11500)
    ax.set_ylim(0,11500)

def plot_calib_steps(ax, filters_ref, filters_splus, filters_gaia, conf,
                     label_color, filters_colors, bg_color = "#000000"):

    stepsfit = ["external_sed_fit", "stellar_locus_fit", "internal_sed_fit",
                "gaiascale_sed_fit"]
    stepsfit_i = [0, 2, 3, 5]
    stepspred = ["external_sed_pred", "internal_sed_pred","gaiascale_sed_pred"]
    stepspred_i = [1, 4, 6]

    ax.text(0.5, 0.91, "external", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(3.5, 0.91, "internal", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(5.5, 0.91, "Gaia-scale", ha = "center", va = "top", fontsize = 12,
            color = label_color)

    ax.text(2, 0.91, "Stellar", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(2, 0.88, "locus", ha = "center", va = "top", fontsize = 12,
            color = label_color)

    ax.text(0, 0.88, "fit", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(3, 0.88, "fit", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(5, 0.88, "fit", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(1, 0.88, "pred", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(4, 0.88, "pred", ha = "center", va = "top", fontsize = 12,
            color = label_color)
    ax.text(6, 0.88, "pred", ha = "center", va = "top", fontsize = 12,
            color = label_color)

    filters_all = filters_ref + [""] + filters_splus + [""] + filters_gaia
    y0 = 0.82
    yf = 0.05
    yfilt = np.linspace(y0, yf, len(filters_all))

    dy = yfilt[0] - yfilt[1]

    for filt, y in zip(filters_all, yfilt):
        if filt != "":
            ax.text(-0.6, y, filt, ha = "right", va = "center",
                    fontsize = 10, color = filters_colors[filt])
        else:
            ax.plot([-1.8, 6.3], [y, y], color = label_color, zorder = -2,
                    alpha = 0.5, lw = 1)

    ax.plot([-1.8, 6.3], [0.85, 0.85], color = label_color, zorder = -2,
            alpha = 0.5, lw = 1)

    for stepfit, i in zip(stepsfit, stepsfit_i):
        for filt, y in zip(filters_all, yfilt):

            if filt == "":
                continue

            try:
                if filt in conf[stepfit]:
                    ax.scatter([i], [y], color = filters_colors[filt],
                               s = 50, marker = 'o',
                               edgecolor = filters_colors[filt])
            except KeyError:
                        pass


    for steppred, i in zip(stepspred, stepspred_i):
        for filt, y in zip(filters_all, yfilt):

            if filt == "":
                continue

            try:
                if filt in conf[steppred]:
                    ax.scatter([i], [y], color = filters_colors[filt],
                               s = 50, marker = 'o',
                               edgecolor = filters_colors[filt])
                elif filt in conf[steppred.replace("pred", "fit")]:
                    ax.plot([i], [y], color = filters_colors[filt],
                            marker = 'o', fillstyle = 'none', markersize = 7)

            except KeyError:
                pass

    ax.fill_between([-0.5, 1.5], [yf-dy/2, yf-dy/2], [0.945, 0.945],
                    color = label_color, zorder = -2, alpha = 0.02)
    ax.fill_between([2.5, 4.5], [yf-dy/2, yf-dy/2], [0.945, 0.945],
                    color = label_color, zorder = -2, alpha = 0.02)

    ax.text(3, 0.985, "Calibration steps", ha = "center", va = "top",
            fontsize = 16, color = label_color)

    ax.set_xlim(-2, 7)
    ax.set_ylim(0, 1.02)


def plot_obs_date(hdrs_info_df, obs_database, obs_database_finaldate, ax,
                  filters, label_color, bg_color, filters_colors):
    x0 = 2014.7
    xf = 2026
    xi = 2016

    yf = 0
    yi = -len(filters)

    airmass0 = 1
    airmassf = 2
    deltaairmass = airmassf - airmass0

    ax.set_xlim(x0, xf)
    ax.set_ylim(-len(filters), 0)

    # Set final date
    findate = obs_database_finaldate.decimalyear
    ax.fill_between([findate, xf], [yi, yi], [yf, yf], color=bg_color,
                    zorder=2, alpha=0.5)
    ax.fill_between([x0, xi], [yi, yi], [yf, yf], color=bg_color,
                    zorder=2, alpha=0.5)

    ax.plot([findate, findate], [yi, yf], color="#FF0000", lw=0.5,
            label="last obs. DB update")
    ax.plot([], [], color=label_color, lw=0.5, label="Reduction date")
    ax.legend(loc=5, frameon=False, fontsize=14, labelcolor=label_color)

    # Highlight epochs that used different GAINS - Datas aproximadas!!!
    ax.fill_between([x0, 2017.5], [yi, yi], [yf, yf], color=label_color,
                    zorder=-1, alpha=0.025)
    ax.fill_between([2020.5, 2022.2479], [yi, yi], [yf, yf], color=label_color,
                    zorder=-1, alpha=0.025)

    # Plot year and months lines
    skip = True
    for year in range(xi, int(np.floor(xf))):
        d = Time(f'{year}-1-1T00:00:00', format='isot', scale='utc')
        xline = d.decimalyear
        # if xline < findate:
        if skip:
            skip = False
        else:
            ax.text(xline, yi + 0.1, f"{xline:.0f}", ha="center",
                    color=label_color, fontsize=12, alpha=0.8)

        ax.plot([xline, xline], [yi, yf], color=label_color, alpha=0.1, lw=0.5)

        for month in range(2, 13):
            d = Time(f'{year}-{month}-1T00:00:00', format='isot',
                     scale='utc')
            xline = d.decimalyear
            # if xline < findate:
            if month == 7:
                ax.plot([xline, xline], [yi, yf], color=label_color,
                        alpha=0.075, lw=0.5)
            else:
                ax.plot([xline, xline], [yi, yf], color=label_color,
                        alpha=0.05, lw=0.5)

    # Plot airmass labels
    ax.text(findate, yi + 0.1, "AIRMASS", ha="right", va="bottom",
            rotation=90, color=label_color, fontsize=8,
            alpha=0.5)

    for i in range(1, len(filters) + 1):
        ax.text(xi, -i, f"{airmass0:.1f}", ha="left", va="bottom", rotation=0,
                color="#666666", fontsize=6)
        ax.text(xi, -i + 0.5, f"{airmass0 + deltaairmass / 2:.1f}", ha="left",
                va="bottom", rotation=0, color="#666666", fontsize=6)
        ax.plot([xi, findate], [-i - 0.5, -i - 0.5], ls="--",
                color=label_color, alpha=0.2, lw=0.5)
    ax.plot([xi, findate], [-0.5, -0.5], ls="--", color=label_color,
            alpha=0.2, lw=0.5)

    ###############################
    # Plot the data

    for i in range(len(filters)):
        filt = filters[i]
        yi0 = -i - 1
        yif = -i

        deltay = yif - yi0

        # Color background
        ax.fill_between([x0, xf], [yi0, yi0], [yif, yif],
                        color=filters_colors[filt], zorder=-1, alpha=0.1)
        ax.plot([xi, findate], [-i - 1, -i - 1], ls="-",
                color=filters_colors[filt], alpha=0.5, lw=0.5)
        ax.text(xi - 0.02, yi0 + 0.5, filt, color=filters_colors[filt],
                va="center", ha="right", fontsize=12)

        # Plot filter reduction dat
        f = hdrs_info_df["FILTER"] == filt
        reduction_date = hdrs_info_df.loc[f, "REDUCTION_DATE"].values[0].decimalyear
        ax.plot([reduction_date, reduction_date], [-i - 1, -i], ls="-",
                color=label_color, alpha=1, lw=0.5)

        # Get all filter observations in the database
        filtdb = filt.replace("SPLUS_", "")
        f = (obs_database['OBJECT'] == field) & (obs_database['FILTER'] == filtdb)
        obs_filter = obs_database[f]

        # List of images used in the reduction
        f_header = hdrs_info_df["FILTER"] == filt
        reduction_images = hdrs_info_df.loc[f_header, "IMAGES"].values

        # Plot observations
        for o in range(len(obs_filter)):
            obs_date = list(obs_filter["year"])[o]
            obs_airmass = list(obs_filter["AIRMASS"])[o]
            obs_image = list(obs_filter["FILENAME"])[o]
            obs_image.replace(".fits", "")
            obs_image.replace(".fz", "")

            # Calculate y-axis value of airmass for this filter
            obs_y = yi0 + deltay * (obs_airmass - airmass0) / deltaairmass

            if obs_image in reduction_images:
                ax.plot([obs_date], [obs_y], color=filters_colors[filt],
                        marker='o', fillstyle='none', markersize=5,
                        zorder=1000)
            else:
                ax.plot([obs_date], [obs_y], color=filters_colors[filt],
                        marker='o', markersize=5, zorder=1000)

def plot_config(conf, ax, label_color):
    cols = {"type": conf["field_type"],
            "calibration": conf["calibration_name"],
            "reduction": conf["reduction"]}

    i = 1
    for ref in conf["reference_catalog"]:
        cols[f"calib. ref.{i}"] = ref

    cols["calib. phot."] = conf["calibration_photometry"]

    if conf["calibration_photometry"].lower() == "dual":
        cols["det. image"] = ", ".join(conf["detection_image"])

    cols["inst_zp"] = f"{conf['inst_zp']:.1f}"

    cols["use_weight"] = conf["use_weight"]
    cols["XY_correction"] = conf["sex_XY_correction"]

    if conf["extinction_correction"].lower() == "none":
        cols["ISM extinction"] = None
    else:
        cols["ISM extinction"] = conf["extinction_correction"]

    cols["Bayesian fit"] = conf["model_fitting_bayesian"]

    try:
        if conf["offset_to_splus_refcalib"].lower() == "none":
            cols["calib. offset"] = None
        else:
            cols["calib. offset"] = True
            cols["offset after:"] = conf["offset_include_after"]
    except KeyError:
        cols["calib. offset"] = None

    try:
        cols["gaia reference"] = conf["gaia_reference"]
    except KeyError:
        cols["gaia reference"] = "DR2"

    print(cols)

    y = 0.80
    dy = 0.055

    ax.text(0.05, 0.98, "Calibration\nConfiguration", fontsize=13,
            color=label_color, horizontalalignment='left',
            verticalalignment='top', transform=ax.transAxes)

    for key in cols.keys():
        ax.text(0.05, y, key, fontsize=12, color="#666666",
                horizontalalignment='left', verticalalignment='center',
                transform=ax.transAxes)

        if cols[key] is None:
            ax.text(0.95, y, "NONE", fontsize=13, color="#FFA500",
                    horizontalalignment='right',
                    verticalalignment='center', transform=ax.transAxes)
        elif isinstance(cols[key], bool):
            if cols[key]:
                ax.text(0.95, y, "TRUE", fontsize=13, color="#00DD00",
                        horizontalalignment='right',
                        verticalalignment='center', transform=ax.transAxes)
            else:
                ax.text(0.95, y, "FALSE", fontsize=13, color="#FFA500",
                        horizontalalignment='right',
                        verticalalignment='center', transform=ax.transAxes)
        else:
            ax.text(0.95, y, cols[key], fontsize=13, color=label_color,
                    horizontalalignment='right',
                    verticalalignment='center', transform=ax.transAxes)

        y -= dy

def plot_splus_filter_info_2(ax, filters_splus, hdrs_info_df, filt_info_cols,
                             label_color, filters_colors):
    x0 = -3

    for j in range(len(filt_info_cols)):
        colname = filt_info_cols["colname"][j].replace(" ", "")
        coldisplay = filt_info_cols["coldisplay"][j].replace(" ", "")
        coldisplay = coldisplay.replace("[", " [")

        y = filt_info_cols["yvalue"][j]
        ax.text(x0, y, coldisplay, ha="left", fontsize=14, color=label_color,
                va="center")

    for i in range(len(filters_splus)):
        filt = filters_splus[i]
        color = filters_colors[filt]
        ax.text(i, 0.97, filt.replace("_", "\n"), va="top", fontsize=14,
                color=color, ha="center")

        for j in range(len(filt_info_cols)):
            colname = filt_info_cols["colname"][j].replace(" ", "")
            y = filt_info_cols["yvalue"][j]

            typ = filt_info_cols.loc[j, "type"].replace(" ", "")
            value = hdrs_info_df.loc[i, colname]

            vl2 = filt_info_cols.loc[j, "vl2"]
            cl2 = filt_info_cols.loc[j, "cl2"].replace(" ", "")
            vl1 = filt_info_cols.loc[j, "vl1"]
            cl1 = filt_info_cols.loc[j, "cl1"].replace(" ", "")

            vu2 = filt_info_cols.loc[j, "vu2"]
            cu2 = filt_info_cols.loc[j, "cu2"].replace(" ", "")
            vu1 = filt_info_cols.loc[j, "vu1"]
            cu1 = filt_info_cols.loc[j, "cu1"].replace(" ", "")

            color = filt_info_cols.loc[j, "c0"].replace(" ", "")
            if color == "filt":
                color = filters_colors[filt]

            try:
                if value is not None:
                    if value <= float(vl1):
                        color = cl1
                    if value <= float(vl2):
                        color = cl2
                    if value >= float(vu1):
                        color = cu1
                    if value >= float(vu2):
                        color = cu2
            except:
                pass

            if typ == "float":
                try:
                    ax.text(i, y, f"{value:.2f}", fontsize=14, color=color, va="center", ha="center")
                except ValueError:
                    pass
                except TypeError:
                    pass

            if typ == "int":
                try:
                    ax.text(i, y, f"{value:.0f}", fontsize=14, color=color, va="center", ha="center")
                except ValueError:
                    pass
                except TypeError:
                    pass

    ax.plot([x0 - 0.2, 11.4], [0.86, 0.86], color=label_color, lw=0.5)
    # ax.plot([-0.5,11.5], [0.01, 0.01], color = label_color, lw = 0.5)

    # ax.fill_between([0,1], [0., 0.], [1., 1.], color = label_color, zorder = -10, transform = ax.transAxes, alpha = 0.05)
    ax.set_xlim(x0 - 0.5, 11.5)
    ax.set_ylim(0, 1)

def plot_ebv_dist(ebv_data, ax, conf, label_color):
    ebv = ebv_data["EBV"]

    # Remove NaNs
    ebv = ebv[~np.isnan(ebv)]
    maxebv = np.nanmax(ebv)
    meanebv = np.nanmean(ebv)
    medianebv = np.nanmedian(ebv)
    q25ebv, q75ebv = np.nanpercentile(ebv, [25, 75])
    ebviqr = q75ebv - q25ebv
    sdevebv = np.nanstd(ebv)

    ax.plot([], [], alpha=0.0,
            label=f"mean(" + r"E$_\mathrm{B-V}$ = " + f"{meanebv:.4f})",
            color=label_color)
    ax.plot([], [], alpha=0.0,
            label=f"sdev(" + r"E$_\mathrm{B-V}$ = " + f"{sdevebv:.4f})",
            color=label_color)

    if (medianebv+2*sdevebv) <= 0.1:
        ax.set_xlim(0.0, 0.1)
        color = "#b77642"
        xticks_major = [0.02, 0.04, 0.06, 0.08]
        xticks_minor = [0.01, 0.03, 0.05, 0.07, 0.09]
        xticks_mminor = np.arange(0.002, 0.1, 0.002)

    elif (medianebv+2*sdevebv) <= 0.3:
        ax.set_xlim(0.0, 0.3)
        color = "#ffa500"
        xticks_major = [0.05, 0.1, 0.15, 0.20, 0.25]
        xticks_minor = [0.025, 0.075, 0.125, 0.175, 0.225, 0.275]
        xticks_mminor = np.arange(0.005, 0.3, 0.005)

    elif (medianebv+2*sdevebv) <= 1.0:
        ax.set_xlim(0.0, 1)
        color = "#ff7f2a"
        xticks_major = [0.2, 0.4, 0.6, 0.8]
        xticks_minor = [0.1, 0.3, 0.5, 0.7, 0.9]
        xticks_mminor = np.arange(0.02, 1.0, 0.02)

    else:
        ax.set_xlim(0.0, 5)
        color = "#ff0000"
        xticks_major = [1, 2, 3, 4]
        xticks_minor = [0.5, 1.5, 2.5, 3.5, 4.5]
        xticks_mminor = np.arange(0.1, 5.0, 0.1)

    parts = ax.violinplot(ebv, [0], points=60, widths=1, showmeans=False,
                          showextrema=True, vert=False, showmedians=False,
                          bw_method=0.5)

    ax.scatter([np.mean(ebv)], [0], color=color)

    parts['bodies'][0].set_facecolor(color)
    # parts['bodies'][0].set_edgecolor(color2)
    parts['bodies'][0].set_alpha(0.3)

    parts['cbars'].set_edgecolor(color)
    parts['cbars'].set_alpha(0.5)

    # parts['cmedians'].set_edgecolor(filters_colors[filt])
    parts['cmaxes'].set_edgecolor(color)
    parts['cmaxes'].set_alpha(0.5)

    parts['cmins'].set_edgecolor(color)
    parts['cmins'].set_alpha(0.5)

    # Plot vertical lines
    ax.text(0.98, 0.06, r"E$_\mathrm{B-V}$", ha="right", va="bottom",
            color=label_color, fontsize=16, alpha=0.5,
            transform=ax.transAxes)
    ax.text(0.07, 0.93, f"Source: {conf['extinction_correction']}",
            ha="left", va="top", color=label_color, fontsize=14,
            alpha=1, transform=ax.transAxes)

    for x in xticks_major:
        ax.plot([x, x], [-0.7, 1.5], lw=0.5, alpha=0.2, zorder=-5,
                color=label_color)
        ax.text(x, -0.9, x, ha="center", va="bottom", color=label_color,
                fontsize=16, alpha=0.5)
    for x in xticks_minor:
        ax.plot([x, x], [-0.7, 1.5], lw=0.5, alpha=0.1, zorder=-5,
                color=label_color)
    for x in xticks_mminor:
        ax.plot([x, x], [-0.7, 1.5], lw=0.5, alpha=0.05, zorder=-5,
                color=label_color)

    ax.set_ylim(-1, 1)
    ax.legend(labelcolor=color, fontsize=16, frameon=False, loc=1)

    ax.fill_between([0, 0.06], [0, 0], [1, 1], color=color0, alpha=0.3,
                    transform=ax.transAxes)
    ax.plot([0.06, 0.06], [0, 1], color=color0, lw=0.5, transform=ax.transAxes)
    ax.text(0.015, 0.5, "Extinction Corr.", color=color, ha="left", va="center",
            fontsize=16, rotation=90,
            transform=ax.transAxes, alpha=0.8)


def plot_Alambda_dist(ebv_data, ax, filters_splus, alambda_av,
                      filters_colors, label_color):
    ebv = ebv_data["EBV"]
    ebv = ebv[~np.isnan(ebv)]

    Av = 3.1 * ebv

    maxAv = np.nanmax(Av)
    maxebv = np.nanmax(ebv)

    medianebv = np.nanmedian(ebv)
    medianAv = np.nanmedian(Av)
    sdevAv = np.nanstd(Av)

    if medianebv <= 0.1:
        color = "#b77642"
    elif medianebv <= 0.3:
        color = "#ffa500"
    elif medianebv <= 1.0:
        color = "#ff7f2a"
    else:
        color = "#ff0000"

    for i in range(len(filters_splus)):
        filt = filters_splus[i]

        Alambda = alambda_av[filt] * Av

        parts = ax.violinplot(Alambda, [i], points=60, widths=0.7,
                              showmeans=False, showextrema=True,
                              showmedians=False, bw_method=0.5)

        ax.scatter([i], [np.mean(Alambda)], color=filters_colors[filt],
                   alpha=0.5)

        parts['bodies'][0].set_facecolor(filters_colors[filt])
        # parts['bodies'][0].set_edgecolor(color2)
        parts['bodies'][0].set_alpha(0.5)

        parts['cbars'].set_edgecolor(filters_colors[filt])
        parts['cbars'].set_alpha(0.5)
        # parts['cmedians'].set_edgecolor(filters_colors[filt])
        parts['cmaxes'].set_edgecolor(filters_colors[filt])
        parts['cmaxes'].set_alpha(0.5)
        parts['cmins'].set_edgecolor(filters_colors[filt])
        parts['cmins'].set_alpha(0.5)

        if filt == "SPLUS_U":
            ax.text(i, 0, "SPLUS", ha="center", va="bottom", rotation=0,
                    color=filters_colors[filt], fontsize=10,
                    alpha=0.8, zorder=-2)

        if (medianAv+2*sdevAv) <= 0.3:
            ax.set_ylim(-0.04, 0.3)
            ax.text(i, -0.03, filt.replace("SPLUS_", ""), ha="center",
                    va="bottom", rotation=0, color=filters_colors[filt],
                    fontsize=12, alpha=0.8, zorder=-2)

            yticks_major = [0, 0.05, 0.1, 0.15, 0.20, 0.25]
            yticks_minor = [0.025, 0.075, 0.125, 0.175, 0.225]

        elif (medianAv+2*sdevAv) <= 1.0:
            ax.set_ylim(-0.12, 1)
            ax.text(i, -0.09, filt.replace("SPLUS_", ""), ha="center",
                    va="bottom", rotation=0,
                    color=filters_colors[filt], fontsize=12, alpha=0.8,
                    zorder=-2)

            yticks_major = [0, 0.2, 0.4, 0.6, 0.8]
            yticks_minor = [0.1, 0.3, 0.5, 0.7]
            # ax.text(i, 0.9, r"$A_{"+f"{filt.replace('SPLUS_', '')}"+r"}$", ha = "center", va = "center", color = filters_colors[filt], fontsize = 16, alpha = 1)

        else:
            ax.set_ylim(-0.6, 5)
            ax.text(i, -0.04, filt.replace("SPLUS_", ""), ha="center",
                    va="bottom", rotation=0,
                    color=filters_colors[filt], fontsize=12, alpha=0.8,
                    zorder=-2)

            yticks_major = [0, 1, 2, 3, 4]
            yticks_minor = [0.5, 1.5, 2.5, 3.5]

    for y in yticks_major:
        ax.plot([-1, 12], [y, y], lw=0.5, alpha=0.2, zorder=-5,
                color=label_color)
        ax.text(11.5, y, y, ha="center", va="bottom", rotation=0,
                color=label_color, fontsize=14, alpha=0.5, zorder=-2)
    for y in yticks_minor:
        ax.plot([-1, 12], [y, y], lw=0.5, alpha=0.1, zorder=-5,
                color=label_color)

    ax.text(0.01, 0.93, r"A$_\lambda$ [mag]", ha="left", va="top",
            rotation=0, color=color, fontsize=16, alpha=0.8,
            zorder=-2, transform=ax.transAxes)

    ax.plot([-1, 12], [0, 0], lw=0.5, alpha=0.5, zorder=-5, color=label_color)

    ax.set_xlim(-0.5, len(filters_splus) + 1)

def plot_zp_fitting(filt, zp_fitting_data, zp_data="", ax=plt, mag_low=14,
                    mag_up=18, label_color="#000000", zoom=False,
                    filters_colors = None, xpsp = False, xlim = [12, 20]):

    x = zp_fitting_data[filt + "_mod"]
    y = zp_fitting_data[filt + "_mod"] - zp_fitting_data[filt]


    if zp_data != "":
        zp = zp_data[filt]

    ax.scatter(x, y, color=label_color, marker='.', s=1, alpha=0.1, zorder=1)

    # Get color
    if filters_colors is not None:
        filt_color = filters_colors[filt]
    else:
        filt_color = "#666666"

    # Plot fitting range
    f = (x >= mag_low) & (x <= mag_up)
    if not xpsp:
        logg = zp_fitting_data["logg"]
        f = f & (logg > 3)

    ax.scatter(x[f], y[f], color=filt_color, marker='.', s=5,
               alpha=0.7, zorder=3)

    ax.plot([9.8, 23], [0, 0], ls='-', lw=1, color=label_color,
            zorder=-1, alpha=0.15)

    # Remove original ticks
    ax.set_yticks([])
    ax.set_xticks([])

    if zoom:

        if zp_data != "":
            ax.plot([mag_low, mag_low], [zp - 0.25, zp + 0.25],
                    ls='-', lw=1, color=filt_color, zorder=1, alpha=0.4)
            ax.plot([mag_up, mag_up], [zp - 0.25, zp + 0.25],
                    ls='-', lw=1, color=filt_color, zorder=1, alpha=0.4)

            ax.plot(xlim, [zp_data[filt], zp_data[filt]],
                    ls='--', lw=2, color=filt_color, zorder=2)
            ax.text(xlim[1]-0.3, zp_data[filt] - 0.15, f"{zp_data[filt]:.3f}",
                    va="center", ha="right", color=filt_color,
                    fontsize=17, alpha=0.8)

        # Plot ticks
        for y in np.arange(-0.5, 1, 0.5):
            ax.text(xlim[0]+0.2, y, f"{y:0.1f}", va="center", ha="left",
                    color=label_color, fontsize=11, alpha=0.5,
                    rotation=90)

        for y in np.arange(-1, 1, 0.5):
            ax.plot([12, 22], [y, y], color=label_color, lw=1,
                    alpha=0.1, zorder=-5)

        for y in np.arange(-1, 1, 0.25):
            ax.plot([12, 22], [y, y], color=label_color, lw=1, alpha=0.05,
                    zorder=-5)

        for y in np.arange(-1, 1, 0.05):
            ax.plot([12, 22], [y, y], color=label_color, lw=1, alpha=0.02,
                    zorder=-5)

        for x in [13, 15, 17, 19]:
            if (x > xlim[0]) & (x < xlim[1]):
                ax.text(x, -1 + 0.1, x, ha="center", color=label_color,
                        fontsize=10, alpha=0.5)

        ax.text(xlim[1]-0.5, -1 + 0.1, r"mag$_{\mathrm{AB}}$", ha="right",
                color=label_color, fontsize=9, alpha=0.5)
        ax.text(xlim[0]+0.4, 1 - 0.12, r"$\Delta$mag", ha="left", va="top",
                rotation=90, color=label_color, fontsize=9,
                alpha=0.5)

        for x in np.arange(13, 20, 2):
            ax.plot([x, x], [-1, -1 + 0.05], color=label_color, lw=1, alpha=0.5)

        for x in np.arange(14, 20, 1):
            ax.plot([x, x], [-1, -1 + 0.025], color=label_color, lw=1, alpha=0.4)

        ax.set_facecolor(filt_color)
        ax.patch.set_alpha(0.1)

        ax.set_xlim(xlim)
        ax.set_ylim(-1, 1)

    else:

        if zp_data != "":
            ax.plot([mag_low, mag_low], [zp - 0.5, zp + 0.5], ls='-', lw=1, color=filt_color, zorder=1, alpha=0.4)
            ax.plot([mag_up, mag_up], [zp - 0.5, zp + 0.5], ls='-', lw=1, color=filt_color, zorder=1, alpha=0.4)

            ax.plot(xlim, [zp_data[filt], zp_data[filt]], ls='--', lw=2, color=filt_color, zorder=2)
            ax.text(xlim[1]-0.3, zp_data[filt] - 0.6, f"{zp_data[filt]:.3f}", va="center", ha="right", color=filt_color,
                    fontsize=17, alpha=0.8)

        # ax.text(21.7, 5.5, filt, va = "center", ha = "right", color = label_color, fontsize = 10, alpha = 0.8)

        # Plot ticks
        for y in np.arange(0, 6, 2):
            ax.text(xlim[0]+0.2, y, f"{y:0d}", va="center", ha="left", color=label_color, fontsize=10, alpha=0.5, rotation=90)

        for y in np.arange(0, 6, 2):
            ax.plot([12, 20], [y, y], color=label_color, lw=1, alpha=0.05, zorder=-5)

        for y in np.arange(-3, 6, 2):
            ax.plot([12, 20], [y, y], color=label_color, lw=1, alpha=0.02, zorder=-5)

        for y in np.arange(-3.5, 6, 1):
            ax.plot([12, 20], [y, y], color=label_color, lw=1, alpha=0.01, zorder=-5)

        for x in [13, 15, 17, 19]:
            if (x > xlim[0]) & (x < xlim[1]):
                ax.text(x, -2 + 0.2, x, ha="center", color=label_color,
                        fontsize=10, alpha=0.5)

        ax.text(xlim[1]-0.5, -2 + 0.2, r"mag$_{\mathrm{AB}}$", ha="right", color=label_color, fontsize=9, alpha=0.5)
        ax.text(xlim[0]+0.4, 6 - 0.12, r"$\Delta$mag", ha="left", va="top", rotation=90, color=label_color, fontsize=9,
                alpha=0.5)

        for x in np.arange(13, 20, 2):
            ax.plot([x, x], [-2, -2 + 0.1], color=label_color, lw=1, alpha=0.5)

        for x in np.arange(14, 20, 1):
            ax.plot([x, x], [-2, -2 + 0.05], color=label_color, lw=1, alpha=0.4)

        ax.set_facecolor(filt_color)
        ax.patch.set_alpha(0.1)

        ax.set_xlim(xlim)
        ax.set_ylim(-2, 6)


def plot_stloc_zp_fitting(filt, zp_fitting_data, stlocus_ref_cat, conf, zp_data="", ax=plt, label_color="#FFFFFF", zoom=False,
                    filters_colors = None):

    if filters_colors is None:
        color = "#666666"
    else:
        color = filters_colors[filt]
    
    if zp_data != "":
        zp = zp_data[filt]

    filt_x0 = conf["stellar_locus_color_ref"][0]
    filt_x1 = conf["stellar_locus_color_ref"][1] 

    reference_x = stlocus_ref_cat.loc[:, filt_x0] - stlocus_ref_cat.loc[:, filt_x1]
    cat_data_x  = zp_fitting_data.loc[:, filt_x0] - zp_fitting_data.loc[:, filt_x1]


    color_range = conf["stellar_locus_color_range"]
    nbins = conf["stellar_locus_N_bins"]

    filt_ref = conf["stellar_locus_filt_ref"]
    
    bins = np.linspace(color_range[0], color_range[1], nbins)
    delta_bin = bins[1] - bins[0]

    delta_mag = []

    reference_bin_y_list = []
    data_bin_y_list = []

    remove_bad_data = (zp_fitting_data.loc[:, filt].values != -99) & \
                  (zp_fitting_data.loc[:, filt].values != 99) & \
                  (zp_fitting_data.loc[:, filt_ref].values != -99) & \
                  (zp_fitting_data.loc[:, filt_ref].values != 99) & \
                  (zp_fitting_data.loc[:, filt_x0].values != -99) & \
                  (zp_fitting_data.loc[:, filt_x0].values != 99) & \
                  (zp_fitting_data.loc[:, filt_x1].values != -99) & \
                  (zp_fitting_data.loc[:, filt_x1].values != 99)

    print(remove_bad_data.shape)
        
    for bin_i in bins[:-1]:

        reference_bin_cut = (reference_x >= bin_i) & \
                            (reference_x < bin_i + delta_bin)

        print(bin_i)
        print(delta_bin)
        data_bin_cut = (cat_data_x >= bin_i) & \
                       (cat_data_x < bin_i + delta_bin) & \
                       remove_bad_data

        
        reference_bin_y = stlocus_ref_cat.loc[reference_bin_cut, filt] - \
                          stlocus_ref_cat.loc[reference_bin_cut, filt_ref]

        data_bin_y = zp_fitting_data.loc[data_bin_cut, filt] - \
                     zp_fitting_data.loc[data_bin_cut, filt_ref]

        mean_reference_bin_y = ut.mean_robust(reference_bin_y)

        cut_outliers = (data_bin_y > -5) & (data_bin_y < 5)
        mean_data_bin_y = ut.mean_robust(data_bin_y[cut_outliers], 0.5, 0.5)

        delta_mag.append(mean_reference_bin_y - mean_data_bin_y)

        ####
        reference_bin_y_list.append(mean_reference_bin_y)
        data_bin_y_list.append(mean_data_bin_y)
        ####

    delta_mag = np.array(delta_mag)

    reference_bin_y_list = np.array(reference_bin_y_list)
    data_bin_y_list = np.array(data_bin_y_list)

    # Get order to remove max and min values
    o = np.argsort(delta_mag)

    zp = ut.mean_robust(delta_mag[o][1:-1])
    #########
    x = np.array(bins[:-1]) + delta_bin/2

    ax.scatter(reference_x,
                stlocus_ref_cat.loc[:, filt] - stlocus_ref_cat.loc[:, filt_ref],
                zorder = 1, alpha = 0.02, color = "#AAAAAA", marker='.', s=5,)

    ax.scatter(x[o][1:-1], reference_bin_y_list[o][1:-1],
                s = 30, c = label_color, zorder = 3)

    ax.scatter(x[o][0], reference_bin_y_list[o][0],
                s = 30, c = label_color, marker = 'x', zorder = 3)

    ax.scatter(x[o][-1], reference_bin_y_list[o][-1],
                s = 30, c = label_color, marker = 'x', zorder = 3)

    ax.plot(x, reference_bin_y_list, color = label_color, zorder = 4)
       
    x_data = cat_data_x[remove_bad_data]
    y_data = zp_fitting_data.loc[remove_bad_data, filt] - \
             zp_fitting_data.loc[remove_bad_data, filt_ref]

    ax.scatter(x_data, y_data, c = color, zorder=2, alpha=0.2, marker='.', s=5,)

    ax.scatter(x[o][1:-1], data_bin_y_list[o][1:-1],
                s = 30, c = color, zorder = 5)

    ax.scatter(x[o][0], data_bin_y_list[o][0],
                s = 30, c = color, marker = 'x', zorder = 5)

    ax.scatter(x[o][-1], data_bin_y_list[o][-1],
                s = 30, c = color, marker = 'x', zorder = 5)

    ax.plot(x, data_bin_y_list, color = color, zorder = 6)


    if zp_data != "":
        for i in range(1, len(x)-1):
            xx = [x[o][i], x[o][i]]
            yy = [data_bin_y_list[o][i], data_bin_y_list[o][i]+zp_data[filt]]
    
            ax.plot(xx, yy, color = color, ls = '--', lw = 1, alpha = 0.8)
    
        ax.text(x[1], data_bin_y_list[1]+zp_data[filt]/2, 
                f"{zp_data[filt]:.3f}", va="center", ha="left", color=color,
                fontsize=17, alpha=0.8)

            
    ymax = np.nanmax((np.max(reference_bin_y_list),
                  np.max(data_bin_y_list))) + 1
    ymin = np.nanmin((np.min(reference_bin_y_list),
                  np.min(data_bin_y_list))) - 1
    #ymin, ymax = [0, 3]

    ax.text(0.02, 0.5, f"{filt} - {filt_ref}", va = "center", ha = 'left', color = label_color,
        fontsize = 10, rotation = 90, transform = ax.transAxes, alpha = 0.4)

    ax.text(0.5, 0.98, f"{filt_x0} - {filt_x1}", va = "top", ha = 'center', color = label_color,
        fontsize = 10, rotation = 0, transform = ax.transAxes, alpha = 0.4)


    for yl in np.arange(-3,3,0.5):
        ax.plot([color_range[0]-0.4, color_range[1]+0.1], [yl, yl], color=label_color, lw=1, alpha=0.05, zorder=-5)    

    for yl in np.arange(-3.25,3.25,0.5):
        ax.plot([color_range[0]-0.4, color_range[1]+0.1], [yl, yl], color=label_color, lw=1, alpha=0.02, zorder=-5)    

    ax.text(color_range[0], ymin + 0.15, color_range[0], ha = "center", va = "bottom", color = label_color, alpha = 0.4, fontsize = 9)    
    ax.text(color_range[1], ymin + 0.15, color_range[1], ha = "center", va = "bottom", color = label_color, alpha = 0.4, fontsize = 9)    
    
    for xl in np.arange(color_range[0]-0.3, color_range[1]+0.3, 0.3):
        ax.plot([xl, xl], [ymin, ymin + 0.1], color=label_color, lw=1, alpha=0.5, zorder=5)    

    for xl in np.arange(color_range[0]-0.3, color_range[1]+0.3, 0.1):
        ax.plot([xl, xl], [ymin, ymin + 0.075], color=label_color, lw=1, alpha=0.2, zorder=5)    

    ax.set_facecolor(color)
    ax.patch.set_alpha(0.1)
    #ax.set_xlabel(f"{filt_x0} - {filt_x1}")
    #ax.set_ylabel(f"{filt} - {filt_ref}")
    ax.set_ylim((ymin, ymax))
    ax.set_xlim(color_range[0]-0.4, color_range[1]+0.1)

################################################################################

def plot_xycheck(grid, filt, ax, filters_colors, label_color,
                 bg_color="#000000", clim=[-0.02, 0.02]):
    xbins = conf["XY_correction_xbins"]
    ybins = conf["XY_correction_ybins"]

    Nxgrid = grid.shape[0]
    Nygrid = grid.shape[1]

    dx = ((xbins[1] - xbins[0]) / (Nxgrid - 1)) / 2.
    dy = ((ybins[1] - ybins[0]) / (Nygrid - 1)) / 2.

    xbins_grid = np.linspace(xbins[0] + dx, xbins[1] + dx, Nxgrid)
    ybins_grid = np.linspace(ybins[0] + dy, ybins[1] + dy, Nygrid)

    xbins_lines = np.linspace(xbins[0], xbins[1], Nxgrid)
    ybins_lines = np.linspace(ybins[0], ybins[1], Nygrid)

    xx, yy = np.meshgrid(xbins_grid, ybins_grid, sparse=False)

    cmap = pltcolors.LinearSegmentedColormap.from_list("",
                [filters_colors[filt], bg_color, filters_colors[filt]])

    ax.pcolor(xx, yy, grid.T, vmin=clim[0], vmax=clim[1], cmap=cmap)

    ax.vlines(xbins_lines, xbins[0], xbins[1], color=label_color, linewidth=0.5,
              alpha=0.4)
    ax.hlines(ybins_lines, ybins[0], ybins[1], color=label_color, linewidth=0.5,
              alpha=0.4)

    for i in range(Nxgrid - 1):
        for j in range(Nygrid - 1):
            if not np.isnan(grid[i, j]):
                ax.text(xbins_grid[i], ybins_grid[j], f"{1000 * grid[i, j]:+.0f}",
                        color=label_color, ha="center",
                        va="center", alpha=0.5, fontsize=9)

    ax.text(0.01, 0.01, r"X$_\mathrm{align}$", ha='left', va='bottom',
            fontsize=9, color=label_color, alpha=0.5,
            zorder=10, transform=ax.transAxes)
    ax.text(0.01, 0.97, r"Y$_\mathrm{align}$", ha='left', va='top',
            rotation=90, fontsize=9, color=label_color,
            alpha=0.5, zorder=10, transform=ax.transAxes)

    ax.set_xlim((xbins[0], xbins[1]))
    ax.set_ylim((ybins[0], ybins[1]))


def plot_gaia_zp(filt, gaia_zp_data, gaia_zp_dist, ax=plt, filt_color="#666666",
                 label_color="#000000"):
    ax.set_xlim(-0.05, 0.05)
    ax.set_ylim(-0.3, 1.5)

    if gaia_zp_dist is not None:
        density = stats.gaussian_kde(gaia_zp_dist[filt])
        x = np.arange(-0.1, 0.1, .0001)
        y = density(x)
        y = y / np.max(y)
        ax.fill_between(x, y, color=filt_color, alpha=0.2, zorder=0)

    for x in np.arange(-0.05, 0.05, 0.01):
        ax.plot([x, x], [0, 0.1], color="#666666", alpha=0.2)
    for x in np.arange(-0.11, 0.1, 0.005):
        ax.plot([x, x], [0, 0.05], color="#666666", alpha=0.2)

    ax.plot([0, 0], [0, 1.5], color=filt_color, ls="--", alpha=0.1)

    if filt == "GAIA3":
        gaia_zp = gaia_zp_data["SPLUS_R"]
        ax.text(0.5, 0.9, "gaia scale ZP", ha="center", va="center",
                fontsize=18, color=filt_color, transform=ax.transAxes)

    else:
        gaia_zp = gaia_zp_data[filt]

    ax.scatter(gaia_zp, [0.06], s=150, marker="^", color=filt_color,
               alpha=0.4, linewidths=0)

    ax.plot([-0.1, 0.1], [0, 0], color=filt_color, alpha=0.2)

    ax.text(-0.03, 0.1, -0.03, va="bottom", ha="center", fontsize=9,
            color="#666666", alpha=0.5)
    ax.text(0.03, 0.1, 0.03, va="bottom", ha="center", fontsize=9,
            color="#666666", alpha=0.5)

    ax.fill_between([-0.1, 0.1], [-0.3, -0.3], [0.0, 0.0],
                    color=filt_color, alpha=0.1, zorder=0)
    ax.text(0.5, 0.075, f"{gaia_zp:.3f}", ha="center", va="center",
            fontsize=15, color=filt_color, transform=ax.transAxes, alpha=0.8)

def plot_final_zp(filt, zp_data, final_zp_dist, ax, filters_colors,
                  label_color="#000000"):
    # Get color
    filt_color = filters_colors[filt]

    ax.set_xlim(18, 25)
    ax.set_ylim(-0.5, 1.5)

    if final_zp_dist is not None:
        density = stats.gaussian_kde(final_zp_dist[filt])
        x = np.arange(18, 25, .01)
        y = density(x)
        y = y / np.max(y)
        ax.fill_between(x, y, color=filt_color, alpha=0.3, zorder=0)

    for x in np.arange(18, 25):
        ax.plot([x, x], [0, 0.1], color="#666666", alpha=0.2)
    for x in np.arange(18.5, 25.5, 1):
        ax.plot([x, x], [0, 0.05], color="#666666", alpha=0.2)

    ax.scatter(zp_data[filt], [0.06], s=150, marker="^", color=filt_color,
               alpha=0.5, linewidths=0)
    ax.plot([18, 25], [0, 0], color=filt_color, alpha=0.35)

    ax.text(19, 0.1, 19, va="bottom", ha="center", fontsize=9, color="#666666",
            alpha=0.5)
    ax.text(24, 0.1, 24, va="bottom", ha="center", fontsize=9, color="#666666",
            alpha=0.5)

    ax.fill_between([18, 25], [-0.5, -0.5], [0.0, 0.0], color=filt_color,
                    alpha=0.1, zorder=0)
    ax.text(0.5, 0.9, f"{filt}", ha="center", va="center", fontsize=16,
            color=label_color, transform=ax.transAxes)
    ax.text(0.5, 0.125, f"{zp_data[filt]:.3f}", ha="center", va="center",
            fontsize=20, color=label_color,  transform=ax.transAxes)

def plot_models(mod_data, cat_data, isocs, ax, label_color):

    ax.scatter(np.log10(mod_data["Teff"]), mod_data["logg"], color="#005500",
               alpha=0.05, s=30, zorder=10)
    ax.scatter(np.log10(cat_data["Teff"]), cat_data["logg"], color=label_color,
               alpha=0.05, s=5, zorder=11)

    ax.plot([], [], color=label_color, alpha=0.5, zorder=10,
            label="MIST isoc. (1e8, 1e9, 1e10 yr)")
    ax.scatter([], [], color="#005500", alpha=1, s=30, zorder=10,
               label="Models: Coelho (2014)")
    ax.scatter([], [], color=label_color, alpha=1, s=30, zorder=10,
               label="Fitted models")
    ax.legend(loc='upper left', bbox_to_anchor=(0.1, 0.98),
              labelcolor=label_color, frameon=False, fontsize=11)

    ax.set_xlim(4.5, 3.4 - 0.1)
    ax.set_ylim(6.5, -0.5)
    # ax.set_xscale("log")
    for isoc in isocs:
        f_isoc = isoc[" EEP"] < 1400
        logteff = isoc["log_Teff"]
        logg = isoc["log_g"]
        ax.plot(logteff[f_isoc], logg[f_isoc], color=label_color,
                alpha=0.3, lw=0.5, zorder=-5)

    for x in np.arange(3.5, 4.5, 0.25):
        ax.plot([x, x], [6.5, 6.3], color=label_color, alpha=0.2, zorder=-1)
        ax.plot([x, x], [-0.5, 6.5], color=label_color, alpha=0.05, zorder=-3)

    for x in np.arange(3.4, 4.5, 0.05):
        ax.plot([x, x], [6.5, 6.4], color=label_color, alpha=0.1, zorder=-2)

    for y in np.arange(0, 7, 1):
        ax.plot([4.5, 4.47], [y, y], color=label_color, alpha=0.2, zorder=-1)
        ax.plot([3.4, 4.5], [y, y], color=label_color, alpha=0.05, zorder=-3)

    for y in np.arange(-0.5, 7, 0.25):
        ax.plot([4.5, 4.485], [y, y], color=label_color, alpha=0.1, zorder=-2)

    for y in [1, 3, 5]:
        ax.text(4.45, y, y, fontsize=14, ha='left', va='center',
                color=label_color, alpha=0.5, zorder=1)

    for x in [3.75, 4.0, 4.25]:
        ax.text(x, 6.2, x, fontsize=14, ha='center', va='bottom',
                color=label_color, alpha=0.5, zorder=1)

    ax.text(0.9, 0.03, r"$\log T_{\mathrm{eff}}$", ha='right', va='bottom',
            fontsize=14, color=label_color, alpha=0.8,
            zorder=0, transform=ax.transAxes)
    ax.text(0.03, 0.95, r"$\log g$", ha='left', va='top', rotation=90,
            fontsize=14, color=label_color, alpha=0.8,
            zorder=0, transform=ax.transAxes)

def plot_stlocus(ref_data, cat_data, ax, mag1, mag2, mag3, mag4, xlim, ylim,
                 label_color, cat_color):
    if ref_data is not None:
        xref = ref_data[mag1] - ref_data[mag2]
        yref = ref_data[mag3] - ref_data[mag4]

    xcat = cat_data[mag1] - cat_data[mag2]
    ycat = cat_data[mag3] - cat_data[mag4]

    filters_splus = ['SPLUS_U', 'SPLUS_F378', 'SPLUS_F395', 'SPLUS_F410',
                     'SPLUS_F430', 'SPLUS_G', 'SPLUS_F515', 'SPLUS_R',
                     'SPLUS_F660', 'SPLUS_I', 'SPLUS_F861', 'SPLUS_Z']

    fcat = (cat_data["SPLUS_U"] >= 14)
    for filt in filters_splus:
        fcat = fcat & (cat_data[filt] >= 14)
        fcat = fcat & (cat_data[filt] <= 18)

    if ref_data is not None:
        ax.scatter(xref, yref, color=label_color, s=1, marker='.',
                   alpha=0.3, zorder=-1)
    ax.scatter(xcat[fcat], ycat[fcat], color=cat_color, s=12, marker='o',
               alpha=0.8, zorder=1)

    ax.text(0.5, 0.97, f"{mag1} " + r"$-$" + f" {mag2}", fontsize=14,
            color=label_color, horizontalalignment='center',
            verticalalignment='top', transform=ax.transAxes)
    ax.text(0.97, 0.5, f"{mag3} " + r"$-$" + f" {mag4}", fontsize=14,
            color=label_color, horizontalalignment='right',
            verticalalignment='center', rotation=90, transform=ax.transAxes)

    for x in (1. / 3, 2. / 3):
        ax.plot([x, x], [0, 1], color=label_color, alpha=0.1, lw=0.5, zorder=-1,
                transform=ax.transAxes)
        ax.plot([0, 1], [x, x], color=label_color, alpha=0.1, lw=0.5, zorder=-1,
                transform=ax.transAxes)

    for x in (1. / 6, 3. / 6, 5. / 6):
        ax.plot([x, x], [0, 1], color=label_color, alpha=0.05, lw=0.5, zorder=-1,
                transform=ax.transAxes)
        ax.plot([0, 1], [x, x], color=label_color, alpha=0.05, lw=0.5, zorder=-1,
                transform=ax.transAxes)

    xdelta = xlim[1] - xlim[0]
    ydelta = ylim[1] - ylim[0]

    ax.text(1. / 3, 0.03, f"{xlim[0] + xdelta / 3:.2f}", fontsize=16,
            color=label_color, alpha=0.5,
            ha='center', va='bottom', transform=ax.transAxes)
    ax.text(2. / 3, 0.03, f"{xlim[0] + 2 * xdelta / 3:.2f}", fontsize=16,
            color=label_color, alpha=0.5,
            ha='center', va='bottom', transform=ax.transAxes)

    ax.text(0.03, 1. / 3, f"{ylim[0] + ydelta / 3:.2f}", fontsize=16,
            color=label_color, alpha=0.5,
            ha='left', va='center', rotation=90, transform=ax.transAxes)
    ax.text(0.03, 2. / 3, f"{ylim[0] + 2 * ydelta / 3:.2f}", fontsize=16,
            color=label_color, alpha=0.5,
            ha='left', va='center', rotation=90, transform=ax.transAxes)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

################################################################################
################################################################################
###### Make the plots
################################################################################
################################################################################
################################################################################

px = 1/plt.rcParams['figure.dpi']

fig, axs = plt.subplot_mosaic(mosaic,
                              layout='constrained',
                              figsize = (2*3360*px, 2*1440*px),
                              facecolor=color0,
                              per_subplot_kw={"00": {"projection": ccrs.Robinson()}})

for label, ax in axs.items():
    ax.set_facecolor(color1)
    ax.set_yticks([])
    ax.set_xticks([])

#ax = axs['00']
#ax.text(0.96, 0.5, "Obs. dates", color = "#7e02d4", va = "center",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

#ax = axs['70']
#ax.fill_between([0.94,1], [0, 0], [1, 1], color = color0,
#                transform = ax.transAxes)
#ax.text(0.96, 0.5, "External ref.", color = "#b4008c", va = "center",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

#ax = axs['30']
#ax.fill_between([0.94,1], [0, 0], [1, 1], color = color0,
#                transform = ax.transAxes)
#ax.text(0.96, 0.5, "External", va = "center", color = "#b4008c",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

#ax = axs['70']
#ax.fill_between([0.94,1], [0, 0], [1, 1], color = color0,
#                transform = ax.transAxes)
#ax.text(0.96, 0.5, "Gaia Scale", va = "center", color = "#4ff500",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

#ax = axs['80']
#ax.fill_between([0.94,1], [2./3, 2./3], [1, 1], color = color0,
#                transform = ax.transAxes)
#ax.text(0.96, 5./6, "Final ZP", va = "center", color = "#b4008c",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

#ax = axs['80']
#ax.fill_between([0.94,1], [1./3, 1./3], [2./3, 2./3], color = color0,
#                transform = ax.transAxes)

#ax = axs['80']
#ax.fill_between([0.94,1], [0, 0], [1./3, 1./3], color = color0,
#                transform = ax.transAxes)
#ax.text(0.96, 1./6, "Synthetic Models", va = "center", color = "#00AA00",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

#ax = axs['93']
#ax.fill_between([0.91,1], [0, 0], [1, 1], color = color0, alpha = 0.3,
#                transform = ax.transAxes)
#ax.plot([0.91,0.91], [0, 1], color = color0, lw = 0.5, transform = ax.transAxes)
#ax.text(0.94, 0.5, "Stellar Locus checks", color = "#bb17b5", va = "center",
#        fontsize = 16, rotation = 90, transform = ax.transAxes, alpha = 0.8)

############################################
# Plot splus logo and Data release
newax = fig.add_axes([0.16,0.89,0.05,0.1], anchor = "NE", zorder=1)
newax.set_facecolor(color0)
imgplot = newax.imshow(logo)
newax.patch.set_alpha(0)
newax.set_yticks([])
newax.set_xticks([])
newax.axis('off')

#ax = axs['00']
#ax.text(0.5, 0.4, "field", fontsize = 14, color = "#666666", horizontalalignment='center', verticalalignment='center', transform = ax.transAxes)
#plot_DR(field = field,
#        ax = ax,
#        label_color = color2,
#        conf = conf, former_DRs = DRs)
#ax.set_facecolor(color0)

ax = axs['03']

#ax.set_facecolor(color0)

if field in list(splus_footprint["NAME"]):
    field_name_color = color2
elif field.replace("_", "-") in list(splus_footprint["NAME"]):
    field_name_color = color2
elif field.replace("-", "_") in list(splus_footprint["NAME"]):
    field_name_color = color2
else:
    field_name_color = "#ffa500"

ax.plot([0.35, 0.65], [0.6, 0.6], color = color2, transform = ax.transAxes)
ax.text(0.50, 0.55, "Calibration", fontsize = 24, color = field_name_color, ha='center',
        va='top', transform = ax.transAxes)

ax.text(0.10, 0.25, field, fontsize = 32, color = field_name_color, ha='left',
        va='top', transform = ax.transAxes)


ax.text(0.95, 0.22, conf["data_release_name"], fontsize = 22,
        color = field_name_color, ha='right',
        va='bottom', transform = ax.transAxes)

ax.text(0.95, 0.18, conf["calibration_name"], fontsize = 18,
        color = field_name_color, ha='right', alpha = 0.8,
        va='top', transform = ax.transAxes)

############################################
# Plot sky projection

ax = axs['00']

ax.set_facecolor("#666666")
ax.patch.set_alpha(0.15)
#plot_sky(field_ra = field_RA, field_dec = field_DEC,
#         splus_footprint = splus_footprint, ax = ax, color_label = color2,
#         point_color=field_name_color)

ax.text(0.00, 0.72, "RA", fontsize = 11, color = "#666666", ha='left',
        va='bottom', transform = ax.transAxes)

ax.text(0.30, 0.72, field_RAhms[:2] + r"$^{h}$" + field_RAhms[2:],
        ha = 'right', fontsize = 11, color = field_name_color, va='bottom',
        transform = ax.transAxes, alpha = 0.8)
ax.text(0.32, 0.72, f"({field_RA:.2f}"+r"$^\degree$"+")", ha = 'left',
        fontsize = 8, color = "#666666", va='bottom', transform = ax.transAxes)

ax.text(0.00, 0.65, "DEC", fontsize = 11, color = "#666666", ha='left',
        va='bottom', transform = ax.transAxes)
ax.text(0.30, 0.65, field_DECdms[:3] + r"$^\degree$" + field_DECdms[3:],
        ha='right', fontsize = 11, color = field_name_color, va='bottom',
        transform = ax.transAxes, alpha = 0.8)
ax.text(0.32, 0.65, f"({field_DEC:+.2f}"+r"$^\degree$"+")", fontsize = 8,
        color = "#666666", ha='left', va='bottom', transform = ax.transAxes)


############################################
# Plot filters

filters_to_plot = filters_splus
if "GALEX_NUV" in conf["external_sed_fit"]:
    filters_to_plot = ["GALEX_NUV"] + filters_to_plot

ax = axs["05"]
ax.set_facecolor(color0)

plot_filters(filters_to_plot,
             filters_colors,
             ax = ax,
             path_to_filters = path_to_filters,
             zorder = 1, alpha = 1, legend = False,
             label_color = color2)


ax = axs["0I"]

plot_filters(filters_gaia,
             filters_colors,
             ax = ax,
             path_to_filters = path_to_filters,
             zorder = 1, alpha = 1, legend = True,
             label_color = color2,
             lambda_eff = ut._lambda_eff,
             alambda_av = ut._Alambda_Av)

############################################
# Plot XY
ax = axs["10"]
ax.set_facecolor(color0)

plot_detections(detections = detections, ax = ax, label_color = color2,
                ref_xmatch = gaia_xmatch, xmatch_color = "#AA5533",
                xpsp_xmatch = gaiaxpsp_xmatch, xpsp_color = "#08c902")

if x0y0l_data is not None:
    plot_xy_grid(x0y0l_data   = x0y0l_data,
                ax = ax,
                conf = conf,
                line_color = "#888888")

############################################
# Calib steps

#ax = axs['50']
#plot_calib_steps(ax = ax,
#                 filters_ref  = filters_ref,
#                 filters_splus  = filters_splus,
#                 filters_gaia  = filters_gaia,
#                 conf = conf,
#                 label_color = color2,
#                 filters_colors = filters_colors,
#                 bg_color = color0)

#####################################
#### Plot Observation dates
ax = axs['09']

# noinspection PyBroadException
try:
    plot_obs_date(hdrs_info_df = hdrs_info_df,
                  obs_database = obs_database,
                  obs_database_finaldate = obs_database_finaldate,
                  ax = ax,
                  filters = filters_splus,
                  label_color = color2,
                  bg_color = color0,
                  filters_colors = filters_colors)
except:
    print("Unable to make obs_date plot")

#####################################
#### Plot Configuration
ax = axs['13']
ax.set_facecolor(color0)
ax.fill_between([0,1], [0,0], [0.9,0.9], color = color1,
                transform = ax.transAxes, zorder = -1000)

plot_config(conf = conf, ax = ax, label_color = color2)

#####################################
#### Plot Filters info table
ax = axs['14']
ax.set_facecolor(color0)
plot_splus_filter_info_2(ax = ax,
                         filters_splus = filters_splus,
                         hdrs_info_df = hdrs_info_df,
                         filt_info_cols = filt_info_cols_2,
                         label_color = color2,
                         filters_colors = filters_colors)

#####################################
#### Plot EBV
ax = axs['40']
plot_ebv_dist(ebv_data = ebv_data, ax = ax, conf = conf, label_color = color2)

ax = axs['70']
plot_Alambda_dist(ebv_data = ebv_data, ax = ax, filters_splus = filters_splus,
                  alambda_av = ut._Alambda_Av, filters_colors = filters_colors,
                  label_color = color2)


#####################################
#### Plot zp-fitting xpsp

ax_line = ['33', '34', '35', '36', '37', '38', '39', '3A', '3B', '3C', '3D', '3E'] # 5

mag_low_list = conf["gaiaxpsp_zp_fitting_mag_low"]
mag_up_list = conf["gaiaxpsp_zp_fitting_mag_up"]

print(zp_xpsp)
for filt, mag_low, mag_up in zip(filters_xpsp, mag_low_list, mag_up_list):
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]
    plot_zp_fitting(filt, zp_xpsp_data, zp_xpsp, ax = ax,
                    mag_low = mag_low, mag_up = mag_up, label_color = color2,
                    filters_colors=filters_colors, xpsp=True)

for filt in filters_splus:
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]
    ax.text(0.5, 0.95, filt, va = "top", ha = "center", color = color2,
            fontsize = 16, alpha = 0.8, transform = ax.transAxes)

#####################################
#### Plot zp-fitting external

ax_line = ['33', '54', '55', '56', '57', '58', '59', '5A', '5B', '5C', '5D', '5E'] # 5

mag_low_list = conf["external_zp_fitting_mag_low"]
mag_up_list = conf["external_zp_fitting_mag_up"]

for filt, mag_low, mag_up in zip(filters_splus_ext, mag_low_list, mag_up_list):
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]

    if filt != "SPLUS_U":
        zoom = True
    else:
        zoom = False

    plot_zp_fitting(filt, zp_ext_data, zp_ext, ax = ax,
                    mag_low = mag_low, mag_up = mag_up, label_color = color2,
                    filters_colors=filters_colors, zoom = zoom)

for filt in filters_splus:
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]
    ax.text(0.5, 0.95, filt, va = "top", ha = "center", color = color2,
            fontsize = 16, alpha = 0.8, transform = ax.transAxes)


#####################################
#### Plot GALEX

if 'GALEX_NUV' in filters_ref:
    ax = axs["53"]

    filt = 'GALEX_NUV'

    plot_zp_fitting(filt, zp_ext_data, ax = ax, mag_low = 14, mag_up = 21,
                    label_color = color2, filters_colors=filters_colors,
                    zoom = True, xlim = [15, 22])
    ax.text(0.5, 0.95, filt, va = "top", ha = "center", color = color2,
            fontsize = 16, alpha = 0.8, transform = ax.transAxes)

else:
    ax = axs["53"]
    ax.set_facecolor(color0)

#####################################
#### Plot zp-fitting external fit

ax_line = ['33', '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D', '6E'] # 5

mag_low_list = conf["gaiaxpsp_zp_fitting_mag_low"]
mag_up_list = conf["gaiaxpsp_zp_fitting_mag_up"]

for filt, mag_low, mag_up in zip(filters_xpsp, mag_low_list, mag_up_list):
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]

    plot_zp_fitting(filt, zp_ext_data, ax = ax,
                    mag_low = mag_low, mag_up = mag_up, label_color = color2,
                    filters_colors=filters_colors, zoom = True)

for filt in filters_splus:
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]
    ax.text(0.5, 0.95, filt, va = "top", ha = "center", color = color2,
            fontsize = 16, alpha = 0.8, transform = ax.transAxes)

#####################################
#### Plot zp-fitting gaia-scale

ax_line = ['1I', '1I', '7K', '3I', '3I', '7J', '5I', '5I', '5K', '7K', '8I', '8I'] # 7

mag_low_list = conf["gaiascale_zp_fitting_mag_low"]
mag_up_list = conf["gaiascale_zp_fitting_mag_up"]

for filt, mag_low, mag_up in zip(filters_gaia, mag_low_list, mag_up_list):
    i = filters_gaia_order[filt]
    ax = axs[ax_line[i]]
    plot_zp_fitting(filt, zp_gsc_data, zp_gsc, ax = ax, mag_low = mag_low,
                    mag_up = mag_up, label_color = color2,
                    filters_colors=filters_colors, zoom = True)
    ax.text(0.5, 0.95, filt, va = "top", ha = "center", color = color2,
            fontsize = 16, alpha = 0.8, transform = ax.transAxes)

#####################################
#### xy-check
ax_line = ['73', '74', '75', '76', '77', '78', '79', '7A', '7B', '7C', '7D', '7E'] # 5

for filt in filters_splus:
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]
    plot_xycheck(xychecks[filt], filt, ax = ax, filters_colors = filters_colors,
                 label_color = color2, bg_color = color0, clim = [-0.2, 0.2])

#####################################
#### Plot gaia zp dist

ax = axs['7I']
#ax.fill_between([0.0,1], [0, 0], [1, 1], color = filters_colors["GAIA3_BP"],
#                alpha = 0.1, transform = ax.transAxes)
plot_gaia_zp("GAIA3_BP", zp_gsc, gaia_zp_dist = gaia_zp_dist, ax = ax,
             label_color = color2, filt_color = filters_colors["GAIA3_BP"])

ax = axs['7J']
#ax.fill_between([0.0,1], [0, 0], [1, 1], color = filters_colors["GAIA3_G"],
#                alpha = 0.1, transform = ax.transAxes)
plot_gaia_zp("GAIA3_G", zp_gsc, gaia_zp_dist = gaia_zp_dist, ax = ax,
             label_color = color2, filt_color = filters_colors["GAIA3_G"])

ax = axs['7K']
#ax.fill_between([0.0,1], [0, 0], [1, 1], color = filters_colors["GAIA3_RP"],
#                alpha = 0.1, transform = ax.transAxes)
plot_gaia_zp("GAIA3_RP", zp_gsc, gaia_zp_dist = gaia_zp_dist, ax = ax,
             label_color = color2, filt_color = filters_colors["GAIA3_RP"])

ax = axs['8I']
#ax.set_facecolor("#080808")
#ax.set_facecolor(color0)

plot_gaia_zp("GAIA3", zp_gsc_mean, gaia_zp_dist = gaia_zp_dist, ax = ax,
             label_color = color2, filt_color = "#888888")

#####################################
#### Plot final zp

ax_line = ['83', '84', '85', '86', '87', '88', '89', '8A', '8B', '8C', '8D', '8E'] # 8

for filt in filters_splus:
    i = filters_splus_order[filt]
    ax = axs[ax_line[i]]
    plot_final_zp(filt, zp_final, final_zp_dist = final_zp_dist, ax = ax,
                  label_color = color2, filters_colors = filters_colors)

############################################
# Plot synthetic models
ax = axs["50"]

plot_models(mod_data = models,
            cat_data = catalog,
            ax = ax,
            isocs = isocs,
            label_color = color2)

############################################
# Plot stellar locus
ax = axs["0F"]
ax.set_facecolor(color0)

plot_stlocus(ref_data = stlocus_reference,
             cat_data = catalog,
             ax = ax,
             mag1 = "SPLUS_F378",
             mag2 = "SPLUS_F430",
             mag3 = "SPLUS_U",
             mag4 = "SPLUS_G",
             xlim = [0.1, 1.6],
             ylim = [0.5, 2.6],
             label_color = color2,
             cat_color = "#C300BC")

ax = axs["3F"]
ax.set_facecolor(color0)

plot_stlocus(ref_data = stlocus_reference,
             cat_data = catalog,
             ax = ax,
             mag1 = "SPLUS_G",
             mag2 = "SPLUS_R",
             mag3 = "SPLUS_F395",
             mag4 = "SPLUS_F515",
             xlim = [0, 1.2],
             ylim = [0.2, 2.3],
             label_color = color2,
             cat_color = "#3E22FA")

#ax = axs["6F"]
#ax.set_facecolor(color0)

#plot_stlocus(ref_data = stlocus_reference,
#             cat_data = catalog,
#             ax = ax,
#             mag1 = "SPLUS_G",
#             mag2 = "SPLUS_R",
#             mag3 = "SPLUS_F515",
#             mag4 = "SPLUS_F861",
#             xlim = [-0.1, 1.1],
#             ylim = [-0.2, 1.3],
#             label_color = color2,
#             cat_color = "#17FF00")

ax = axs["6F"]
plot_stlocus(ref_data = stlocus_reference,
             cat_data = catalog,
             ax = ax,
             mag1 = "SPLUS_G",
             mag2 = "SPLUS_I",
             mag3 = "SPLUS_F410",
             mag4 = "SPLUS_F660",
             xlim = [-0.1, 1.4],
             ylim = [0, 2.1],
             label_color = color2,
             cat_color = "#17FF00")

#ax = axs["6F"]
#plot_stlocus(ref_data = stlocus_reference,
#             cat_data = catalog,
#             ax = ax,
#             mag1 = "SPLUS_R",
#             mag2 = "SPLUS_Z",
#             mag3 = "SPLUS_F430",
#             mag4 = "SPLUS_F861",
#             xlim = [-0.2, 0.7],
#             ylim = [0, 2.1],
#             label_color = color2,
#             cat_color = "#A30000")

############################################
# Finish and save

plt.tight_layout(pad=0.0, w_pad=0.0, h_pad=0.0)

save_plot_file = os.path.join(field_path, f"Calibration_{suffix}",
                              f"{field}_{suffix}_mosaic.png")
plt.savefig(save_plot_file)
