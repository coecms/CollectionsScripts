# To download operative surface analysis (full resolution) ERA Interim data from the ECMWF data server
# Timestep is 6hrs
# Resolution is 0.75X0.75 degree, area is global
# to change them change the relative fields
# Use: change date in date and target fields
#      python ei_oper_an_sfc_full.py
# depends on ecmwfapi.py that can be downloaded from the ECMWF website
# https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
# contact: paolap@utas.edu.au
# last updated 16/01/2014
#!/usr/bin/python
from ecmwfapi import ECMWFDataServer

yr = "2016"
mntlist = ["05"]
startday = ["01"]

for mnt in mntlist:
   print yr, mnt
   if mnt in  ["01", "03", "05", "07", "08", "10", "12"]:
        endday=["31"]
   if mnt in  ["04", "06", "09", "11"]:
        endday=["30"]
   if mnt=="02":
        endday=["28"]
   if mnt=="02" and yr in ["1980", "1984", "1988", "1992", "1996", "2000", "2004", "2008", "2012", "2016", "2020"]:
        endday=["29"]

   for index in range(len(startday)):
       datestr = yr + mnt + startday[index] + "/to/" + yr + mnt + endday[index]
       targetstr = "ei_oper_an_sfc_075x075_90N0E90S35925E_" + yr + mnt + startday[index] + "_" + yr + mnt + endday[index]
       print datestr, targetstr
       try:
         server = ECMWFDataServer()
         server.retrieve({
          'stream' : "oper",
          'dataset' : "cams_nrealtime",
          'date'    :  datestr,
          'time'    : "00/06/12/18",
          'grid'    : "0.75/0.75",
          'step'    : "0",
          'levtype' : "sfc",
          'type'    : "an",
          'class'   : "mc",
          'expver'  : "0001",
          'param'   : "6.218/13.218/16.218/27.218/30.218/34.128/45.218/47.218/52.210/53.210/125.210/126.210/127.210/128.210/129.128/137.128/151.128/164.128/165.128/166.128/167.128/168.128/172.128/174.128/186.128/187.128/188.128/206.210",
          'area'    : "90/-180/-90/179.25",
          'target'  : targetstr
             })
       except RuntimeError:
             print "Runtime error"
