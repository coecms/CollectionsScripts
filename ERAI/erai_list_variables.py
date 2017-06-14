# This script converts ERA-Interim model level data grib files to netcdf
#from subprocess import call
# it now loops through years as well

import os, re, sys, stat, commands, shutil, time
import glob
import argparse
import pickle     # to load dictionaries saved in external files

def load_dict():
    ''' define variables in each type & dictionaries to map ECMWF-CMIP5 & global attributes '''
    global level_dict, param_dict, grib_ansfc_codes, grib_fcsfc_codes
# list variables for each type
    pv_vars = ["PT", "U", "V", "Q", "PRES", "Z", "O3"] 
    pt_vars = ["PV", "U", "V", "PRES"] 
    ml_vars = ["T", "U", "V", "Q", "D", "W", "VO", "O3", "CC", "CIWC", "CLWC"]
    pl_vars = ["T", "U", "V", "R", "Q", "W", "PV", "O3", "CC", "CIWC", "CLWC", "Z"]
    ansfc_vars = ["10U", "10V", "2D", "2T", "CI", "MSL", "SKT", "SP", "SSTK", "TCWV","TCW","TCC","HCC","LCC","MCC"]
    fcsfc_vars = ["RO", "STRD", "TP", "LSP", "CP", "E", "MN2T", "MX2T", "SLHF", "SSRD","SF","10U", "10V", "2D", "2T","SP", "CAPE", "TSRC", "TTRC"]
    grib_ansfc_codes = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 134, 136, 137, 139, 141, 148, 151, 164, 165, 166, 167, 168, 170, 173, 174, 183, 186, 187, 188, 198, 206, 234, 235, 236, 238]
    grib_fcsfc_codes = [20, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 49, 50, 57, 58, 59, 78, 79, 134, 136, 137, 139, 141, 142, 143, 144, 145, 146, 147, 148, 151, 159, 164, 165, 166, 167, 168, 169, 170, 175, 176, 177, 178, 179, 180, 181, 182, 183, 186, 187, 188, 189, 195, 196, 197, 198, 201, 202, 205, 206, 208, 209, 210, 211, 212, 228, 229, 230, 231, 232, 235, 236, 238, 239, 240, 243, 244, 245]
    land_vars = ["STL1","STL2","STL3","STL4","SWVL1","SWVL2","SWVL3","SWVL4","SKT","RSN","SD","TSN","ASN"]
# dict = 'type' : ['level description','filename level str',type vars list]
    level_dict = {"oper_an_ml" : ["analysis on model","an-ml",ml_vars], "oper_an_pv" : ["analysis on potential vorticity","an-pv", pv_vars], "oper_an_pt" : ["analysis on potential temperature","an-pt", pt_vars], "oper_an_sfc" : ["analysis on surface","an-sfc",ansfc_vars], "oper_fc_sfc" : ["forecast on surface","fc-sfc",fcsfc_vars], "oper_an_pl" : ["analysis on pressure","an-pl",pl_vars], "land" : ["land experiment version 2", "land", land_vars]}

# this import the param_dict dictionary 'ecmwf var' : ['ecmwf param Id','long name','cmip name'] 
    unpicklefile = open('/g/data1/ub4/Work/Scripts/table128_ecmwf_pickle', 'r')
    param_dict = pickle.load(unpicklefile)
    unpicklefile.close()

def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='Convert ERA Interim grib files to 1 variable monthly netcdf files')
    parser.add_argument('-t','--type', help='ERAI type in the form stream_type_level', required=True)
    parser.add_argument('-v','--variable', type=str, nargs="*", help='ERA Interim variable, default all for the selected type', required=False)
    parser.add_argument('-e','--exclude', action='store_true',
                        help='exclude all variable currently converted to netcdf, default is False',
                        required=False)
    return vars(parser.parse_args())


def create_file(file,message):
    ''' open new file or exit if exists already ''' 
    if os.path.exists(file):
       print message
       sys.exit()
    newfile = open(file,"w")
    return newfile



# Main program starts here
#global level_dict, param_dict
# load dictionaries describing types and variables
load_dict()
# call argument parser
args = parse_input() 
type = args["type"]
# ei_land files can go 1 year instead of 1 months
variables = args["variable"]
if variables is None:  variables = level_dict[type][2]
exclude=args["exclude"]
frq="_6hrs"
if type in ["oper_fc_sfc"]: frq="_3hrs"
# define directories for input files and running code
# create a list of variables file
outfile = type + "_variables.txt"
if exclude: outfile = type + "_grib_variables.txt"
errmsg = "A list for " + type + " exists already"
outlist = create_file(outfile,errmsg)

if exclude: 
   keys= param_dict.keys()
   if type=="oper_an_sfc":
      allvar=set( [x for x in keys if int(param_dict[x][0]) in grib_ansfc_codes ])
   elif type=="oper_fc_sfc":
      allvar=set( [x for x in keys if int(param_dict[x][0]) in grib_fcsfc_codes ])
   #allvar=set(param_dict.keys())
   variables=list(allvar-set(variables))
   print variables

for var in variables:
     
    param=param_dict[var][0]
    cmipvar = param_dict[var][2]
    dummy = param_dict[var][1]
    lname,units = dummy.split("[")   
    units = units.replace("[","")
    units = units.replace("]","")
    level = level_dict[type][0]
    outlist.writelines(",".join([var,cmipvar,param,lname,units]) + "\n")
# create a job file to run cdo & nco commands and submit job to queue


# close nc files list when processed all months and variables 
outlist.close()
    
