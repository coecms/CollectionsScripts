#!/bin/bash -l
# download recursively and checking timestamp Polar_NCEP sst rtg_high_res dataset in /g/data1/ua8/NCEP_Polar/sst/rtg_high_res
# input year to download

cd /g/data1/ua8/NCEP_Polar/sst/rtg_high_res/


# download files, use cookies to keep session alive
#
# -r recursive
# -c continue if file download was interrupted
# -A nc4 download only files with nc4 suffix
# -nH no host-prefixed directories 
# -np  no parent directories
# -nd no directories
# -N check timestamp to decide if downloading or not NB removed because file headers don't have time-stamp
# using only -c options, but this could create issues if files here are smaller but corrupted!!

wget -r -c -nH -np -nd  -e robots=off \
ftp://polar.ncep.noaa.gov/pub/history/sst/rtg_high_res/
