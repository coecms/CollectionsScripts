# To download operative surface analysis (full resolution) ERA Interim Land data from the ECMWF data server
# Timestep is 6hrs
# Resolution is 0.75X0.75 degree, area is global
# to change them change the relative fields
# Use: change date in date and target fields
#      python ei_oper_an_sfc_full.py
# depends on ecmwfapi.py that can be downloaded from the ECMWF website
# https://software.ecmwf.int/wiki/display/WEBAPI/Accessing+ECMWF+data+servers+in+batch
# contact: paolap@utas.edu.au
# last updated 09/10/2014
#!/usr/bin/python
from ecmwfapi import ECMWFDataServer

yr = "1979"
mntlist = ["09"]

#startday = ["01"]
#for mnt in mntlist:
#   print yr, mnt
#   if mnt in  ["01", "03", "05", "07", "08", "10", "12"]:
#        endday=["31"]
#   if mnt in  ["04", "06", "09", "11"]:
#        endday=["30"]
#   if mnt=="02":
#        endday=["28"]
#   if mnt=="02" and yr in ["1980", "1984", "1988", "1992", "1996", "2000", "2004", "2008", "2012"]:
#        endday=["29"]

datestr = yr + "0101/to/" + yr + "1231"
targetstr = "ei_land_075x075_90N0E90S35925E_" + yr +  "0101_" + yr + "1231"
#   for index in range(len(startday)):
#       datestr = yr + mnt + startday[index] + "/to/" + yr + mnt + endday[index]
#       targetstr = "ei_oper_an_sfc_075x075_90N0E90S35925E_" + yr + mnt + startday[index] + "_" + yr + mnt + endday[index]
print datestr, targetstr
try:
         server = ECMWFDataServer()
         server.retrieve({
          'stream' : "oper",
          'dataset' : "interim-land",
          'expver' : "2",
          'date'    :  datestr,
          'time'    : "00/06/12/18",
          'grid'    : "0.75/0.75",
          'levtype' : "sfc",
          'type'    : "an",
          'class'   : "ei",
          'param'   : "139.128/141.128/170.128/183.128/235.128/236.128/238.128/32.128/33.128/39.128/40.128/41.128/42.128",
          'area'    : "90/-180/-90/179.25",
          'target'  : targetstr
             })
except RuntimeError:
             print "Runtime error"
