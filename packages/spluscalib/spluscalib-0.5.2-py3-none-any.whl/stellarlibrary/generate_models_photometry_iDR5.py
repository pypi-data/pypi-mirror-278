#====================================================================================================================#

from models import Coelho_2014              as coelho14
#from models import Castelli_Kurucz_2003     as ck03
#from models import NGSL                     as ngsl

#====================================================================================================================#

# ~~~~~~~~ Filters ~~~~~~~~ #

SDSS        = ['SDSS_U',     'SDSS_G',     'SDSS_R',     'SDSS_I',      'SDSS_Z']
PANSTARRS   = ['PS_G',       'PS_R',       'PS_I',       'PS_Z']
DES         = ['DES_G',      'DES_R',      'DES_I',      'DES_Z']
GAIA        = ['GAIA_G',     'GAIA_BP',    'GAIA_RP']
GAIA3       = ['GAIA3_G',    'GAIA3_BP',   'GAIA3_RP']
GALEX       = ['GALEX_FUV',  'GALEX_NUV']
SM          = ['SM_U',       'SM_V',       'SM_G',       'SM_R',        'SM_I',     'SM_Z']
SPLUS       = ['SPLUS_U',    'SPLUS_F378', 'SPLUS_F395', 'SPLUS_F410', 'SPLUS_F430', 'SPLUS_G',
               'SPLUS_F515', 'SPLUS_R',    'SPLUS_F660', 'SPLUS_I',    'SPLUS_F861', 'SPLUS_Z']

# ~~~~~~~~ Extinctions ~~~~~~~~ #

#ebvs = [0]
ebvs = [-0.1, -0.075, -0.05, -0.025, 0.00, 0.025, 0.05, 0.075, 0.1]
#ebvs = [0,      0.025,  0.05,   0.075,  0.1,    0.125,  0.15,   0.175,
#        0.2,    0.225,  0.25,   0.275,  0.3,    0.325,  0.35,   0.375,
#        0.4,    0.45,   0.5,    0.6,    0.8,    1]
#ebvs = [-0.2, -0.15, -0.1, -0.05,
#        0,
#        0.05,  0.1, 0.15,  0.2]

# ~~~~~~~~ Prior ~~~~~~~~ #

reference = ("./resources/SSPP_notnans.cat",   # Path
             ("FEH_ADOP", "LOGG_ADOP", "TEFF_ADOP"),                # Names of the columns (in order)
             'ascii')                                               # Format

#          Parameter  N      Limits
bins      = {'FeH':  (7,  -3.0,   +0.5),
             'logg': (4,  -1.0,   +6.0),
             'Teff': (0, +2500, +30000)}

#====================================================================================================================#

# Creates an instance of the model class
model = coelho14(ebvs)

# Loads the files (wavelenghts/fluxes) into the object
model.load(path = "./resources/data/s_coelho14_sed/")

# For every filter (passed in the arguments) fills the table with the magnitudes
model.fill("./resources/filters/", SPLUS, SDSS, PANSTARRS, DES, SM, GALEX, GAIA, GAIA3)

# Creates a new column with the prior probabilities of each model (for now, calculated based on SSPP)
model.add_prior(reference = reference, regbins = True, bins = bins, bw = 3.0)

# Removes SEDs with prior probability equal to zero (they won't ever be used)
model.remove(col = "prior", value = 0, error = 1E-8)

# Saves the model catalog (in a .cat file)
model.save(path = "coelho14_bw30_iDR5_2.cat", fmt = "ascii", form = [0, 5, 8])

#====================================================================================================================#
