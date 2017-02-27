#!/bin/bash -l
#PBS -N merge
#PBS -q normal
#PBS -l walltime=10:00:00
#PBS -l mem=2GB
module load grads 
indir=/g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_mdl
#indir=/g/data1/ua8/Download/JRA55/lnk_mdl
cd /g/data1/ua8/Download/JRA55/
#for yr in `seq 1961 2015`
for yr in 1958
do
for mn in `seq --format="%02.f" 1 12`
do
for var in 011_tmp 051_spfh 007_hgt 033_ugrd 034_vgrd; 
do
#./grib2ctl.pl ${indir}/${yr}/anl_mdl.${var}.reg_tl319.${yr}${mn}%d2 ${indir}/${yr}/anl_mdl_${var}_${yr}${mn}.idx > ${indir}/${yr}/anl_mdl_${var}_${yr}${mn}.ctl
#gribmap -e -i ${indir}/${yr}/anl_mdl_${var}_${yr}${mn}.ctl
#./grib2ctl.pl ${indir}/${yr}/anl_mdl.${var}.reg_tl319.${yr}${mn}%d2 ${indir}/${yr}/anl_mdl_${var}_${yr}${mn}.idx > ${indir}/${yr}/anl_mdl_${var}_${yr}${mn}.ctl
#gribmap -e -i ${indir}/${yr}/anl_mdl_${var}_${yr}${mn}.ctl
done
done
done
