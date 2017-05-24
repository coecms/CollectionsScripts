#!/bin/bash -l
# download recursively and checking timestamp TRMM_3B42 dataset in /g/data1/ua8/NASA_TRMM/TRMM_L3/TRMM_3B42/
# input year to download

year=$1
cd /g/data1/ua8/NASA_TRMM/TRMM_L3/TRMM_3B42/

mkdir -p ${year}
nextyr=$(( ${year}+1 ))
mkdir -p ${nextyr}
cd ${year}
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

wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies \
    -r -c -nH -np -nd -A HDF \
    https://disc2.nascom.nasa.gov/data/s4pa/TRMM_L3/TRMM_3B42/${year}/ 
cd ..
chgrp -R ua8 ${year} 
tomove=$(ls "${year}/3B42.${nextyr}"*)
mv ${tomove} ${nextyr}/. 
rm ${year}/robots.txt
