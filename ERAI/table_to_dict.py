# This script read an ECMWF parameterId table (standard is 128 table)
# and produced a python dictionary assigning Id to variable short names
# paolap@utas.edu.au
# 29th May 2014

import pickle
#ntable="162"
ntable="128"
# create empty dictionary
param_dict={}
#open table text file
#ftable = open('ecmwf_128table.txt','r')
ftable = open('ecmwf_'+ntable+'table.txt','r')
#now create the cdo table
cdotable = open('cdo_param_table'+ntable, 'w')
#read file & close
lines = ftable.readlines()
ftable.close()
# extract var short name and id from each line and add to dictionary
for line in lines:
    varid,var,longname,cmip,standard,methods = line.split(":")[0:6]
    print varid
    param_dict.update({var : [varid,longname,cmip]})
    lname,units = longname.split("[")
    units = units.replace("]","")
    if units in ["0-1","0,1","kg kg**-1","m**3 m**-3"]: units = "1"
    cdotable.write("&parameter\n")
    cdotable.write("param = " + varid + "." + ntable + "\n")
    cdotable.write("out_name =" + cmip + "\n")
    cdotable.write("long_name = \"" + lname + "\"\n")
    if standard:
       cdotable.write("standard_name = " + standard + "\n")
    if methods:
       axis_stats = methods.replace("-",":")
       cdotable.write("cell_methods = \"" + axis_stats + "\"\n")
    cdotable.write("units = \"" + units + "\"\n")
    cdotable.write("/\n")
# print dict
#print param_dict
pickle.dump( param_dict, open( "table"+ntable+"_ecmwf_pickle", "wb" ) )
cdotable.close()

