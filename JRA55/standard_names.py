"""
SVN INFO: $Id: standard_names.py 311 2011-08-17 05:38:23Z david.kent@csiro.au $
          $HeadURL: https://projects.arcs.org.au/svn/cawcr/trunk/pythonlib/ccam/standard_names.py $

Author: Tim Erwin, erw001, Tim.Erwin@csiro.au
Description Utilities to convert ccam data to CF compliant files.
             File contains mapping between IPCC names and CCAM names
             Utility Lookup.Lookup allows reverse dictionary lookup
"""

__version__ = "$Revision: 311 $"

from ccam import Lookup

CF_VARIABLE_NAMES = Lookup.Lookup({

    #JRA55
    'tas'   : 'tmp2m',
    'dptas' : 'depr2m',
    'ps'    : 'pressfc',
    'psl'   : 'prmslmsl',
    'hurs'  : 'rh2m',
    'huss'  : 'spfh2m',
    'uas'   : 'ugrd10m',
    'vas'   : 'vgrd10m',
    'ptas'  : 'potsfc',

    #JRA55 3D
    'ta'    : 'tmpprs',
    'zg'   :  'hgtprs',
     
    #JRA55 anl_mdl 3D
    'ta'    : 'tmphbl',
    'zg'   :  'hgthbl',
    'ua'   :  'ugrdhbl',
    'va'   :  'vgrdhbl',
    'hus'   :  'spfhhbl',
    })

CF_STANDARD_NAMES = Lookup.Lookup({
    'hur'    : 'relative_humidity',
    'rsds'   : 'surface_downwelling_shortwave_flux_in_air',
    'pr'     : 'precipitation_flux',
    'tas'    : 'air_temperature',
    'ts'     : 'surface_temperature',
    'ta'     : 'air_temperature',
    'tasmax' : 'air_temperature',
    'tasmin' : 'air_temperature',
    'uas'    : 'eastward_wind',
    'ua'    : 'eastward_wind',
    'uasmax' : 'eastward_wind',
    'vas'    : 'northward_wind',
    'va'    : 'northward_wind',
    'vasmax' : 'northward_wind',
    'mrso' : 'soil_moisture_content',
    'evspsblpot' : 'water_potential_evaporation_flux',
    'orog' : 'surface_altitude',
    'sftlf' : 'land_area_fraction',
    'clt' : 'cloud_area_fraction',
    'vegFrac' : 'area_fraction',
    'mrsoz' : 'moisture_content_of_soil_layer',
    'mrsos' : 'moisture_content_of_soil_layer',
    'psl'   : 'air_pressure_at_sea_level',
    'hurs'  : 'relative_humidity',
    'huss'  : 'specific_humidity',
    'hus'  : 'specific_humidity',
    'dptas' : 'dew_point_depression',
    'ptas'  : 'potential_temperature',
    'ps'    : 'surface_air_pressure',
    'zg'    : 'geopotential_height',
   })

CF_LONG_NAMES = Lookup.Lookup({
    'hur'    : 'Relative humidity',
    'rsds'   : 'SW radiation incident at the surface',
    'pr'     : 'Total precipitation rate',
    'tas'    : 'Surface (2m) air temperature',
    'ts'     : 'Surface temperature',
    'ta'     : 'Air Temperature',
    'tasmax' : 'Daily maximum surface (2m) temperature',
    'tasmin' : 'Daily minimum surface (2m) temperature',
    'uas'    : 'Eastward near-surface wind',
    'ua'    : 'Eastward wind',
    'uasmax' : 'Daily maximum surface (10m) eastward wind',
    'vas'    : 'Northward near-surface wind',
    'va'    : 'Northward wind',
    'vasmax' : 'Daily maximum surface (10m) northward wind',
    'evspsblpot' : 'Potential Surface evaporation plus sublimation rate',
    'mrso' : 'Total Soil Moisture Content',
    'orog' : 'Surface Altitude',
    'sftlf' : 'Land area fraction',
    'clt' : 'Total Cloud Fraction',
    'vegFrac' : 'Vegetation Fraction',
    'mrsoz' : 'Moisture in lower layers of Soil Column',
    'mrsos' : 'Moisture in Upper0.1m of Soil Column',
    'psl'   : 'Sea Level Pressure',
    'ps'    : 'Surface Air Pressure',
    'hurs'  : 'Near-Surface Relative Humidity',
    'huss'  : 'Near-Surface Specific Humidity',
    'hus'  : 'Specific Humidity',
    'dptas' : 'Near-Surface Dew Point Depression',
    'ptas': 'Near-Surface Potential Temperature',
    'zg'  : 'Geopotential Height',
})

CF_UNITS = Lookup.Lookup({
    'hur'    : '',
    'rsds'   : '',
    'pr'     : '',
    'tas'    : 'K',
    'ta'     : 'K',
    'ts'     : '',
    'tasmax' : '',
    'tasmin' : '',
    'uas'    : 'm s-1',
    'ua'    : 'm s-1',
    'uasmax' : '',
    'vas'    : 'm s-1',
    'va'    : 'm s-1',
    'vasmax' : '',
    'mrso' : '',
    'evspsblpot' : '',
    'orog' : '',
    'sftlf' : '',
    'clt' : '1',
    'vegFrac' : '',
    'mrsoz' : '',
    'mrsos' : '',
    'psl'   : 'Pa',
    'huss'  : '1',
    'hus'  : '1',
    'dptas' : 'K',
    'hurs'  : '%',
    'ps'    : 'Pa',
    'ptas'  : 'K',
    'zg'    : 'm',
   })

CCAM_MEASUREMENT_METHOD = {
    'hur'    : 'time: mean (interval: 3 hr comment: sampled instantaneously)',
    'rsds'   : 'time: mean (interval: 6 hr comment: average)',
    'pr'     : 'time: sum (interval: 1 day)',
    'tas'    : 'time: mean (interval: 6 hr comment: average)',
    'ts'     : 'time: mean (interval: 6 hr comment: sampled instantaneously)',
    'tasmax' : 'time: maximum (interval: 1 day)',
    'tasmin' : 'time: minimum (interval: 1 day)',
    'uas'    : 'time: mean (interval: 3 hr comment: sampled instantaneously)',
    'uasmax' : 'time: maximum (interval: 1 day)',
    'vas'    : 'time: mean (interval: 3 hr comment: sampled instantaneously)',
    'vasmax' : 'time: maximum (interval: 1 day)',
    'evspsblpot' : 'time: mean (interval: 6 hr comment: average)',
    'orog' : '',
    'sftlf' : '',
    'clt' : 'time: mean (interval: 6 hr comment: sampled instantaneously)',
    'vegFrac' : '',
    'mrso' : 'time: mean (interval: 6 hr comment: sampled instantaneously) area: mean where land',
    'mrsoz' : 'time: mean (interval: 6 hr comment: sampled instantaneously) area: mean where land',
    'mrsos' : 'time: mean (interval: 6 hr comment: sampled instantaneously) area: mean where land',
    'psl'   : 'time: mean (interval: 6 hr comment: sampled instantaneously)',
}

