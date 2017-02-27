#!/usr/bin/env python
"""

"""
import cdms2
import datetime
import os
import sys
#from ccam import Lookup

#Requires module cct /g/data/r87/public/apps
#from jra.standard_names import CF_VARIABLE_NAMES,CF_STANDARD_NAMES,CF_LONG_NAMES,CF_UNITS,CCAM_MEASUREMENT_METHOD

cdms2.setNetcdfShuffleFlag(1)
cdms2.setNetcdfDeflateFlag(1)

"""
GLOBALS:

   Variables: Mapping of JRA55 variable names to CMIP5 standard names

   History: History string added to metadata

   Reference: JRA55 reference used in metadata

   Units: Sets time axis to standard/common units.

"""
class Lookup(dict):

    """
    a dictionary which can lookup value by key, or keys by value
    """
    def __init__(self, items=[]):
        """
            items can be a list of pair_lists or a dictionary
        """
        dict.__init__(self, items)

    def ccam2ipcc(self, value):
        """
            find the key(s) as a list given a value
        """
        results = [item[0] for item in self.items() if item[1] == value]
        if results:
            return results[0]
        else:
            return None

    def ipcc2ccam(self, key):
        """
            find the value given a key
        """
        if self.has_key(key):
            return self[key]
        else:
            return None

CF_VARIABLE_NAMES = Lookup({

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

CF_STANDARD_NAMES = Lookup({
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

CF_LONG_NAMES = Lookup({
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

CF_UNITS = Lookup({
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



VARIABLES = {
             'DEPR2m': 'dptas',
             'POTsfc': '',
             'PRESsfc': 'ps',
             'PRMSLmsl': 'psl',
             'RH2m': 'hurs',
             'SPFH2m': 'huss',
             'TMP2m' : 'tas',
             'UGRD10m': 'uas',
             'VGRD10m': 'vas'
    }

REFERENCE = "Kobayashi, S., Y. Ota, Y. Harada, A. Ebita, M. Moriya, H. Onoda, K. Onogi, H. Kamahori, C. Kobayashi, H. Endo, K. Miyaoka, and K. Takahashi , 2015: The JRA-55 Reanalysis: General Specifications and Basic Characteristics. J. Meteor. Soc. Japan, 93, 5-48, doi:10.2151/jmsj.2015-001."

HISTORY = "JRA55 downloaded Nov 2015, converted by %(user)s on %(date)s using %(script)s : version %(version)s"

UNITS = "days since 1900-01-01"


def setupOutputFile(outFile,attrs):
    """
    Open output yearly netcdf file and copy across the attributes
    fom the input file and add extra history.
    """
    otf = cdms2.open(outFile,'w')
    print 'Writing to output file:',outFile

    history = HISTORY % {'user': os.environ['USER'],
                         'date': datetime.date.today(),
                         'script': sys.argv[0],
                         'version': 1 }

    if "history" not in attrs:
        setattr(otf,'history',history)
    else:
        setattr(otf,'history',attrs['history']+"\n %s" % (history))

    for key in attrs:
        setattr(otf,key,attrs[key])

    return  otf

def main(ifile):

    #Open file
    fin = cdms2.open(ifile)
   
    #Loop through variables and write out
    for variable in fin.listvariables():
        print("Processing variable %s\n" % variable)
        tvar = fin(variable)

        time_axis = tvar.getTime()
        t = time_axis.asComponentTime()
        cal = time_axis.getCalendar()
 
        ### set the common days since that you want ###
        tvar.getTime().toRelativeTime(UNITS,cal)
        
        #Convert standard names
        tvar.id = CF_VARIABLE_NAMES.ccam2ipcc(variable)
        tvar.long_name = CF_LONG_NAMES[tvar.id]
        tvar.standard_name = CF_STANDARD_NAMES[tvar.id]
        print("I AM HERE AFTER calling cf standard names")
        tvar.units = CF_UNITS[tvar.id]
        print("I AM HERE AFTER calling cf standard names")

        #Setup level axis
        if 'p125' in ifile:
            lev = tvar.getLevel()
            lev.id = 'plev'
            lev.standard_name = 'air_pressure'
            lev.long_name = "pressure"
            lev.units = "Pa"
            lev.positive = "down"
            #Convert from hPa to Pa
            lev[:] = lev[:]*100
        elif 'mdl' in ifile:
            lev = tvar.getLevel()
            lev.id = 'hybl_lev'
            #lev.standard_name = 'air_pressure'
            lev.long_name = "hybrid model level"
            lev.units = "level"
            lev.axis = "Z"
        print("I AM HERE AFTER set up levels axes")

        lat = tvar.getLatitude()
        lat.id = 'lat'
        lat.long_name = 'latitude'
        lat.standard_name = 'latitude'
        lon = tvar.getLongitude()
        lon.id = 'lon'
        lon.long_name = 'longitude'
        lon.standard_name = 'longitude'
        print("I AM HERE AFTER lat/lon")

        #Get date from time axis
        #date_range = t[0]-t[-1]
        date_range = "%s%02d%02d%02d-%s%02d%02d%02d" % (t[0].year,t[0].month,t[0].day,t[0].hour,
                                                  t[-1].year,t[-1].month,t[-1].day,t[-1].hour)

        #Write to file
        if 'surf125' in ifile:
            ofile = '%s_A6hr_JRA55_%s.nc' % (tvar.id,date_range)
        elif '_surf_' in ifile:
            ofile = '%s_6hrLev_JRA55_reg-tl319%s.nc' % (tvar.id,date_range)
        elif 'p125' in ifile:
            ofile = '%s_6hrPlev_JRA55_%s.nc' % (tvar.id,date_range)
        elif 'mdl' in ifile:
            ofile = '%s_6hrLev_JRA55_reg-tl319_%s.nc' % (tvar.id,date_range)
        else:
            print("ERROR: Cannot determine ouput file structure")
            sys.exit(1)

        print ofile

        #TODO: Check file exists?
        fout = setupOutputFile(ofile,{'reference':REFERENCE})
        fout.write(tvar)
        fout.close()

    fin.close()


if __name__ == "__main__":

    ifile = sys.argv[1]
    main(ifile)
