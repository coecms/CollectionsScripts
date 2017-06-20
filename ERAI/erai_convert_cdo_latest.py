# This script converts ERA-Interim model level data grib files to netcdf
#from subprocess import call
# it now loops through years as well

import os, re, sys, stat, commands, shutil, time
import glob
import argparse
import pickle     # to load dictionaries saved in external files

def load_dict():
    ''' define variables in each type & dictionaries to map ECMWF-CMIP5 & global attributes '''
    global level_dict, param162_dict, param128_dict
# list variables for each type
    pv_vars = ["PT", "U", "V", "Q", "PRES", "Z", "O3"] 
    pt_vars = ["PV", "U", "V", "PRES"] 
    ml_vars = ["T", "U", "V", "Q", "D", "W", "VO", "O3", "CC", "CIWC", "CLWC", "Z"]
    pl_vars = ["T", "U", "V", "R", "Q", "W", "PV", "O3", "CC", "CIWC", "CLWC", "Z"]
    ansfc_vars = ["10U", "10V", "2D", "2T", "CI", "MSL", "SKT", "SP", "SSTK", "TCWV","TCW","TCC","HCC","LCC","MCC",
                 "VIMA", "VIEMF", "VINMF", "VIEWVF", "VINWVF", "VITCWV", "VINKEF", "VINHF", "VINGF", "VINTEF"] 
    fcsfc_vars = ["RO", "STRD", "TP", "LSP", "CP", "E", "MN2T", "MX2T", "SLHF", "SSRD","SF","10U", "10V", "2D", "2T","SP", "CAPE", "TSRC", "TTRC"]
    land_vars = ["STL1","STL2","STL3","STL4","SWVL1","SWVL2","SWVL3","SWVL4","SKT","RSN","SD","TSN","ASN"]
# dict = 'type' : ['level description','filename level str',type vars list]
    level_dict = {"oper_an_ml" : ["analysis on model","an-ml",ml_vars], "oper_an_pv" : ["analysis on potential vorticity","an-pv", pv_vars], "oper_an_pt" : ["analysis on potential temperature","an-pt", pt_vars], "oper_an_sfc" : ["analysis on surface","an-sfc",ansfc_vars], "oper_fc_sfc" : ["forecast on surface","fc-sfc",fcsfc_vars], "oper_an_pl" : ["analysis on pressure","an-pl",pl_vars], "land" : ["land experiment version 2", "land", land_vars]}

# this import the param_dict dictionary 'ecmwf var' : ['ecmwf param Id','long name','cmip name'] 
    unpicklefile = open('/g/data1/ua8/Convert/ERAI/table128_ecmwf_pickle', 'r')
    param128_dict = pickle.load(unpicklefile)
    unpicklefile.close()
    unpicklefile = open('/g/data1/ua8/Convert/ERAI/table162_ecmwf_pickle', 'r')
    param162_dict = pickle.load(unpicklefile)
    unpicklefile.close()

def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='Convert ERA Interim grib files to 1 variable monthly netcdf files')
    parser.add_argument('-t','--type', help='ERAI type in the form stream_type_level', required=True)
    parser.add_argument('-y','--year', help='Year', nargs="*", required=True)
    parser.add_argument('-m','--month', type=str, nargs="*", help='Month, default all months', required=False)
    parser.add_argument('-v','--variable', type=str, nargs="*", help='ERA Interim variable, default all for the selected type', required=False)
    parser.add_argument('-l','--low', action='store_true', default='store_false', 
                        help='low resolution (1.5X1.5) option, default is False', 
                        required=False)
    parser.add_argument('-q','--queue', action='store_true',  
                        help='execute jobs instead of submit to queue option, default is False', 
                        required=False)
    return vars(parser.parse_args())


def submit_job(var,meta):
    global rundir, queue, param128_dict, param162_dict, level_dict
#   retrieve info necessary to write job to submit to queue
    param_dict={"128": param128_dict, "162": param162_dict}[meta[3]]
    param=param_dict[var][0]
    # if param=129.128 ie geopotential from oper_an_ml then we want to select only the current month
    if param=='129': param+=',month='+mn
    cmipvar = param_dict[var][2]
    lname = param_dict[var][1]
    level = level_dict[type][0]
    tmpgr = var + "_" + yr + "_" + mn + ".grib"
    tmpnc = var + "_" +  yr + "_" + mn + ".nc"
    if type in ["oper_an_pv","land"]:
       tmpgr = var + "_" +  yr  + ".grib"
       tmpnc = var + "_" +  yr  + ".nc"
    gdate_set = set() 
    for file in glob.glob(infiles):
        gdate_set.add(created_time(file))  
    gdate = ";".join(list(gdate_set))

    # define a template for the shell job to be submitted
    qsub_tmp_skel = '''#! /bin/bash -l
    module load netcdf/4.3.2
    module load cdo/1.6.4
    module load nco/4.3.8
    cd RUN_DIR 
    cdo -select,code=PARAM INFILES TMPGR       
    cdo -L -f nc4 -z zip_5 -setpartabp,/g/data1/ua8/Convert/ERAI/cdo_param_tableNTABLE -setreftime,1900-01-01,00:00:00 TMPGR TMPNC
    ncatted -h -O -a 'title',global,c,c,'ERA-Interim LNAME LEVEL (global GRID lat/lon grid) converted from original grib format' TMPNC                       
    ncatted -h -O -a 'institution',global,o,c,'ARCCSS ARC Centre of Excellence for Climate System Science www.climatescience.org.au' TMPNC
    ncatted -h -O -a 'source',global,c,c,'Original grib files obtained from http://apps.ecmwf.int/datasets/data/interim_full_daily/ on GDATE' TMPNC
    ncatted -h -O -a 'references',global,c,c,'Please acknowledge both ECMWF for original files and the ARCCSS for conversion to netcdf format' TMPNC
    ncks -O --md5_wrt_att -v VAR TMPNC -o OUTNC
    '''
    # write template to a shell file to execute
    qsub_skel = qsub_tmp_skel.replace("RUN_DIR",rundir)
    qsub_skel = qsub_skel.replace("INFILES",meta[1])
    qsub_skel = qsub_skel.replace("PARAM",param)
    qsub_skel = qsub_skel.replace("TMPGR",tmpgr)
    qsub_skel = qsub_skel.replace("TMPNC",tmpnc)
    qsub_skel = qsub_skel.replace("VAR",cmipvar)
    qsub_skel = qsub_skel.replace("LEVEL",level)
    qsub_skel = qsub_skel.replace("LNAME",lname)
    qsub_skel = qsub_skel.replace("GRID",meta[2])
    qsub_skel = qsub_skel.replace("GDATE",gdate)
    qsub_skel = qsub_skel.replace("OUTNC",meta[0])
    qsub_skel = qsub_skel.replace("NTABLE",meta[3])
    qsfname = "ERAI_" + var + yr + mn + ".sh"
    qsub = open(rundir + qsfname, 'w')
    qsub.write(qsub_skel)
    qsub.close()
    # change permissions for qsub file so it is executable
    os.chmod(rundir + qsfname,stat.S_IRWXU)
    #  submit it to raijin with qsub
    cmd = "qsub -P w35 -q normal -lother=gdata1 -l walltime=0:10:00,mem=10Gb,ncpus=1 " + rundir + qsfname

    # now we print the command.  When it's printing OK, we uncomment the
    # commands.getstatusoutput(cmd) line below it
    if queue:
       print cmd
       qsub_status = commands.getstatusoutput(cmd)
    else:
       print "qsfname = " + qsfname
       run_status = commands.getstatusoutput(rundir + qsfname)

def created_time( name):
    return time.strftime("%d/%m/%Y", time.gmtime(os.path.getctime(name)))


def define_dirs(type,resol):
    ''' define input and running directory '''
    indir = "/g/data1/ub4/erai/grib/" + type +  "/" + resol + "/"
    #print "  indir = " + indir
#    if type in ["oper_an_ml", "oper_an_pl"] and resol=="fullres" : 
#       indir += (yr + "/") 
    if not os.path.exists(indir): 
       print "  Error: there's no directory " + indir
       sys.exit()
    rundir = "/g/data1/ua8/Convert/ERAI/Run/" + type + "/"
    #rundir = "/g/data1/ub4/Work/Scripts/Work/" 
    #print "  rundir = " + rundir
    return indir, rundir


def create_file(dir,file,message):
    ''' open new file or exit if exists already ''' 
    if os.path.exists(dir+file):
       print message
       sys.exit()
    newfile = open(dir+file,"w")
    return newfile


def build_dates(yr,mn,type):
    ''' Build the from date to date string to use in nc filename '''
    if mn in  ["01", "03", "05", "07", "08", "10", "12"]:
       endday="31"
    if mn in  ["04", "06", "09", "11"]:
       endday="30"
    if mn=="02":
       endday= "28"
    if mn=="02" and yr in ["1980", "1984", "1988", "1992", "1996", "2000", "2004", "2008", "2012", "2016", "2020"]:
       endday="29"
    datestr = yr + mn +  "01_" + yr + mn + endday
    if type in ["oper_an_pv","land"]:
       datestr = yr + "0101_" + yr + "1231"
    return datestr
    

# Main program starts here
#global level_dict, param_dict
# load dictionaries describing types and variables
load_dict()
# call argument parser
args = parse_input() 
type = args["type"]
years = args["year"]
months = args["month"]
if months is None:  months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
# ei_land files can go 1 year instead of 1 months
if type in ["land"]: months = ["01"]
variables = args["variable"]
if variables is None:  variables = level_dict[type][2]
resol = "fullres"  # this is default
grid = "0.75X0.75" # this is default
if args["low"] is True: 
   resol = "lowres"
   grid = "1.5X1.5"
queue = args["queue"]
print "queue = "
print queue
frq="_6hrs"
if type in ["oper_fc_sfc"]: frq="_3hrs"
# work out which ECMWF table to use, default 128
# define directories for input files and running code
indir, rundir = define_dirs(type,resol)
os.chdir(rundir)
# create a list of netcdf output files
ncfiles = "nc_files.txt"
errmsg = "A list for netcdf files " + ncfiles + " exists already in " + rundir
nclist = create_file(rundir,ncfiles,errmsg)

# loop through months and variables 
for yr in years:
  if type in ["oper_an_ml", "oper_an_pl"] and resol=="fullres" :
     indir += (yr + "/")
  if not os.path.exists(indir):
     print "  Error: there's no directory " + indir
     sys.exit()

  for mn in months:
      t_range = yr + mn + "[0-9][0-9]" 
      if type in ["oper_an_pv","land"] : 
         t_range = yr + "[0-1][0-9][0-9][0-9]" 
      infiles= indir + "ei_" + type + "_*_" + t_range + "*" 
      datestr = build_dates(yr,mn,type)
      for var in variables:
          if type=="oper_an_sfc" and var in ["VIMA", "VIEMF", "VINMF", "VIEWVF", "VINWVF", "VITCWV",
                                             "VINGF", "VINKEF", "VINHF", "VINTEF"]:
              cmipvar = param162_dict[var][2]
              ntable="162"
          else:
              cmipvar = param128_dict[var][2]
              ntable="128"
          # write netcdf name in cmip5 style
          ncout = cmipvar + frq + "_ERAI_historical_" + level_dict[type][1] + "_" +  datestr + ".nc"
          nclist.writelines(ncout + "\n")
# create a job file to run cdo & nco commands and submit job to queue
          meta = [ncout,infiles,grid,ntable]
          if type=="oper_an_ml" and var in ["Z"]:
              t_range = yr + "[0-1][0-9][0-9][0-9]" 
              infiles_sfc=infiles[:-17].replace(yr,'surface') + t_range + "*" 
              meta = [ncout,infiles_sfc,grid,ntable]
          submit_job(var,meta)


# close nc files list when processed all months and variables 
nclist.close()
    
