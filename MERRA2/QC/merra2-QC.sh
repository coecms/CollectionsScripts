#!/bin/bash -l
# simple bash script that checks that MERRA2 files are not missing, corrupted or incomplete
# Paola Petrelli paolap@utas.edu.au
# 2017/02/21
#
# uses stat -c '%s' filename to retrieve filesize and check if it's below a threshold whose value depends on the specific MERRA2 product

ROOT_DIR="/g/data1/rr7/MERRA2/raw/"
cd $ROOT_DIR
# dataset products
prod_list=("M2I6NPANA.5.12.4" "M2T1NXFLX.5.12.4" "M2T1NXINT.5.12.4" "M2T1NXRAD.5.12.4" "M2T1NXSLV.5.12.4")
# file minimum size  from for each dataset product
prod_minsize=(520000000 380000000 1280000000 210000000 400000000)
# goldsmr# server number to download from for each dataset product
prod_num=(5 4 4 4 4) 
for i in ${!prod_list[@]}; do
   cd ${prod_list[$i]} 
   pwd
   years=$(ls )
   for yr in $years; do
       cd $yr
       for month in `seq --format="%02.f" 1 12`; do
           if [ -d $month ] && [ ! "$(find $month -type d -empty)" ]; then
               cd $month
               if [ "${month}" = '12' ]; then
                  nextmn=01
                  nyr=$(( $yr + 1 ))
               else
                  nextmn=$((10#$month + 1))
                  nyr=$yr
               fi   
               lastdate=$( date -d "yesterday ${nyr}-${nextmn}-01" +%Y-%m-%d)
               ndays=${lastdate[@]: -2:2}
               files=($( ls ./*.nc4 ))
               if ! [ "${#files[@]}" = "${ndays}" ]; then
                  echo 'Some files missing for ' $yr-$month 
               fi   
               for f in ${files}; do
                   size=$(stat -c "%s" ${f})
                   if [ $size -lt ${prod_minsize[$i]} ]; then
                       echo "problem with file ${f}"
                       wget --load-cookies ~/.urs_cookies --save-cookies ~/.urs_cookies --keep-session-cookies \
                       -nH -np -nd -O ${f} \
                       https://goldsmr${prod_num[$i]}.gesdisc.eosdis.nasa.gov/data/MERRA2/${prod_list[$i]}/${yr}/${month}/${f} 
                       chgrp rr7 ${f}
                   fi
               done
               cd ../
           fi
       done
       cd ../
   done
   cd ../
done
