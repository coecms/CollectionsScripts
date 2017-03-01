#!/bin/bash -l
module load cdo
cd /g/data1/ua8/Download/GSMaP/raw/reanalysis_gauge/daily/00Z-23Z
#define months as 3 letters code to define time axis
mnt=("jan" "feb" "mar" "apr" "may" "jun" "jul" "aug" "sep" "oct" "nov" "dec")
dirs=($(ls -d *))
echo ${#dirs[@]}
for d in ${dirs[@]}; do
    cd $d 
    yr=${d:0:4}
    mn=$((10#${d:4}-1))
    cp /g/data1/ua8/Download/GSMaP/template.ctl gsmap_${d}.ctl
    sed -ie "s/jan2002/${mnt[$mn]}${yr}/" "gsmap_${d}.ctl" 
    cdo -f nc4 import_binary gsmap_${d}.ctl gsmap_${d}.nc
    cd ..
done

