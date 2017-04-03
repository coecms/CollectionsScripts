#!/bin/bash -l
# download recursively and checking timestamp MERRA2 products in /g/data1/rr7/MERRA2/raw
# input year to download

year=$1
cd /g/data1/rr7/MERRA2/raw/

# list product directories to download/update
dirList=$( ls ./ )
for dir in $dirList; do
    mkdir -p ${dir}/${year}
    cd ${dir}/${year}
# assign right goldsrm# server number depending on dataset product to download
    if [[ "$dir" =~ ^(M2I6NPANA.5.12.4)$ ]]; then
        num=5
    elif [[ "$dir" =~ ^(M2I3NPASM.5.12.4)$ ]]; then
        num=5
    else
        num=4
    fi
    for month in `seq --format="%02.f" 1 12`;
    do
        mkdir -p ${month}
        cd ${month}
        pwd
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
        -r -c -nH -np -nd -A nc4 \
        https://goldsmr${num}.gesdisc.eosdis.nasa.gov/data/MERRA2/${dir}/${year}/${month}/ 
        cd ../
    done
    cd ../../
chgrp -R rr7 ${dir}/${year} 
done
