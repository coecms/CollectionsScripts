# To download operative analysis on pressure levels (full resolution) ERA Interim data from the ECMWF data server
# Download all the files for a year or selected months
# Timestep is 6hrs
# Resolution is 0.75X0.75 degree, area is global
# to change them change the relative fields
# Use: change year and adjust mntlist if necessary
#      python ei_oper_an_pl_full.py
# depends on ecmwfapi.py that can be downloaded from the ECMWF website
# https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
# contact: paolap@utas.edu.au
# last updated 16/01/2014
#!/usr/bin/python
import sys
import argparse
from ecmwfapi import ECMWFDataServer

def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='Download CAMS realtime data')
    parser.add_argument('-y','--year', help='Year', required=True)
    parser.add_argument('-m','--month', type=str, help='Month', required=True)
    parser.add_argument('-d','--day', type=int, help='Day to start from, default 01', required=False)
    parser.add_argument('-e','--end', type=int, help='Day to stop, default is last day of the month', required=False)
    parser.add_argument('-v','--variable', type=str, help='YOTC phys_fc_pl variable', required=True)
    return vars(parser.parse_args())

args = parse_input()
startday = args["day"]
if startday is None: startday=01
yr = args["year"]
mnt = args["month"]
if yr=="2008" and mnt in ["01","02","03","04"] or yr=="2010" and mnt not in ["01","02","03","04"]:
   print "No data for " + yr + " " + mnt
   sys.exit()
varname = args["variable"]
endday = args["end"]
if endday is None:
   if mnt in  ["01", "03", "05", "07", "08", "10", "12"]:
       endday= 31
   if mnt in  ["04", "06", "09", "11"]:
       endday= 30
   if mnt=="02":

# find parameter corresponding to selected variable
var = {"D":"155.128", "PV":"60.128",
       "Q":"133.128", "R":"157.128", "T":"130.128",
         "VO":"138.128", "Z":"129.128"}
varparam =  [var[name] for name in var if name == varname]
if  varparam == []:
    print "Couldn't find variable  " + varname
    sys.exit()
yr = "2016"
mntlist = ["05"]
#mntlist = ["01", "02", "03"]
#mntlist = ["04", "05", "06"]
#mntlist = ["07", "08", "09"]
#mntlist = ["09", "10", "11", "12"]
#mntlist = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

startday = ["01", "06", "11", "16", "21", "26"]
#startday = ["01", "06"]
#startday = ["11","16","21","26"]

for mnt in mntlist:
   print yr, mnt
   if mnt in  ["01", "03", "05", "07", "08", "10", "12"]:
        endday=["05", "10", "15", "20", "25", "31"]
        #endday=["05", "10"]
#        endday=["15", "20", "25", "31"]
   if mnt in  ["04", "06", "09", "11"]:
        endday=["05", "10", "15", "20", "25", "30"]
#        endday=["15", "20", "25", "30"]
   if mnt=="02":
        endday=["05", "10", "15", "20", "25", "28"]
#        endday=["20", "25", "28"]
   if mnt=="02" and yr in ["1980", "1984", "1988", "1992", "1996", "2000", "2004", "2008", "2012", "2016", "2020"]:
        endday=["05", "10", "15", "20", "25", "29"]
#        endday=["20", "25", "29"]

   for index in range(len(startday)): 
       datestr = yr + mnt + startday[index] + "/to/" + yr + mnt + endday[index] 
       targetstr = "ei_oper_an_pl_075x075_90N0E90S35925E_" + yr + mnt + startday[index] + "_" + yr + mnt + endday[index]
       print datestr, targetstr
       try:
         server = ECMWFDataServer()
         server.retrieve({
             'dataset' : "cams_nrealtime",
             'date'    : datestr,
             'time'    : "00/06/12/18",
             'grid'    : "0.75/0.75",
             'step'    : "0",
             'levtype' : "pl",
             'type'    : "an",
             'expver'  : "0001"
             'class'   : "mc",
             'param'   : "138.128",
             'levelist' : "1/2/3/5/7/10/20/30/50/70/100/150/200/250/300/400/500/700/850/925/1000",
              'area'    : "90/-180/-90/179.25",
              'target'  : targetstr
             })
       except RuntimeError:
             print "Runtime error"

