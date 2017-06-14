# To download ERA Interim data from the ECMWF data server
# Download all the files for a year or selected months
# Timestep is 6hrs
# Resolution is 0.75X0.75 degree, area is global
# to change them change the relative fields
# Use: change year and adjust mntlist if necessary
#      python erai_download_full.py
# depends on ecmwfapi.py that can be downloaded from the ECMWF website
# https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
# Author: Paola Petrelli for ARC Centre of Excellence for Climate System Science
# contact: paolap@utas.edu.au
# last updated 03/11/2016
#!/usr/bin/python

from __future__ import print_function
from ecmwfapi import ECMWFDataServer
import argparse
from calendar import monthrange
import pickle     # to load dictionaries saved in external files


def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description=r'''   Download ERA Interim grib files from ECMWF MARS server using ecmwfapi.py.
    Output file format changes depending on selected stream, can download more than one month
    at one time but only one year. If month is not specified will default to entire year. User can 
    choose a start-end file number for model and pressure level streams, where a month is split in 
    6 files. ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t','--type', help='ERAI type in the form stream_type_level', required=True)
    parser.add_argument('-y','--year', help='Year', type=str, required=True)
    parser.add_argument('-m','--month', type=str, nargs="*", help='Month, default all months', required=False)
    parser.add_argument('-s','--start', type=int, 
                        help='start from file, default first file, works only for pressure and model levels that have 6 files',
                        default=1, choices=range(1,7), required=False)
    parser.add_argument('-e','--end', type=int,
                        help='end with file, default last file, works only for pressure and model levels that have 6 files',
                        choices=range(1,7), required=False)
    return vars(parser.parse_args())


def define_dates(type,yr,mn,start,end):
    ''' return a date range for each file depending on selected type '''
    if type in ['oper_an_ml','oper_an_pl']:
        startday = ["01", "06", "11", "16", "21", "26"]
        endday=["05", "10", "15", "20", "25", str(monthrange(int(yr),int(mn))[1])]
        if start: 
            startday=startday[start-1:]
            endday=endday[start-1:]
        if end: 
            ind=end + len(startday)-6
            startday=startday[:ind]
            endday=endday[:ind]
    else:
        startday=['01']
        endday=[str(monthrange(int(yr),int(mn))[1])]
    return startday,endday


def define_args(type):
    ''' Return parameters and levels lists and step, time depending on stream type'''
    # this import the stream_dict dictionary <stream> : ['time','step','params','levels']
    unpicklefile = open('/g/data1/ua8/Download/ERAI/ecmwf_stream_pickle', 'r')
    stream_dict = pickle.load(unpicklefile)
    unpicklefile.close()
    time=stream_dict[type]['time']
    step=stream_dict[type]['step']
    params=stream_dict[type]['params']
    levels=stream_dict[type]['levels']
    return time,step,params,levels


def main():
    # parse input arguments
    args=parse_input()
    type = args["type"]
    type_split = type.split("_")
    # assign time, step, param and levelist values for server request based on stream
    time,step,params,levels =  define_args(type)
    # if surface stream than use 'levtype' keyword instead of 'levelist'
    #if '_sfc' in type:
    #    level_key='levtype'
    #else:
    #    level_key='levelist'
# we should'n t need the distinction, they both are in the dictionary
    #print(level_key,levels)
    print(time,step)
    print(params)
    # assign year and list of months
    yr = args['year']
    mntlist = args["month"]
    if mntlist is None:  mntlist = ["01","02","03","04","05","06","07","08","09","10","11","12"]
    # oper_an_pv data is always from Jan to latest available month
    if len(mntlist) > 1 and type in ['oper_an_pv','oper_an_ml_sfc']:
         startmn=mntlist[0]
         mntlist=[mntlist[-1]]
    # assign arguments start and end to subset pressure and model stream file list if available
    start = args["start"]
    end = args["end"]
    # build MARS requests for each month and submit it using ecmwfapi.py
    for mn in mntlist:
        print( yr, mn)
        if type not in ['oper_an_pv','oper_an_ml_sfc']:
            startmn=mn
        startday,endday = define_dates(type,yr,mn,start,end) 
        # for each output file build filename and submit request
        for ind in range(len(startday)): 
            datestr = yr + startmn + startday[ind] + "/to/" + yr + mn + endday[ind] 
            targetstr = "ei_"+type+"_075x075_90N0E90S35925E_" + yr + startmn + startday[ind] + "_" + yr + mn + endday[ind]
            print(datestr,targetstr)
            try:
                server = ECMWFDataServer()
                server.retrieve({
                    'dataset'  : "interim",
                    'date'     : datestr,
                    'time'     : time,
                    'grid'     : "0.75/0.75",
                    'step'     : step,
                    'levtype'  : type_split[2],
                    'type'     : type_split[1],
                    'class'    : "ei",
                    'param'    : params,
                    'levelist'  : levels,
                    'area'     : "90/-180/-90/179.25",
                    'target'   : targetstr
                })
            except RuntimeError:
                print("Runtime error")


if __name__ == "__main__":
    main()
