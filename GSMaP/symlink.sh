#!/bin/bash -l
#PBS -N merge
#PBS -q normal
#PBS -l walltime=10:00:00
#PBS -l mem=2GB
indir=/g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_mdl
cd /g/data1/ua8/Download/JRA55/lnk_mdl
#for yr in `seq 1961 2015`
for yr in `seq 1958 1960`
#for yr in 1958
do
mkdir $yr
for mn in `seq --format="%02.f" 1 12`
#for mn in `seq --format="%02.f" 1 1`
do
for var in 011_tmp 051_spfh 007_hgt 033_ugrd 034_vgrd; 
do
   for dd in 01 11 21;do
       ln -s ${indir}/${yr}/anl_mdl.${var}.reg_tl319.${yr}${mn}${dd}00_*  ${yr}/anl_mdl.${var}.reg_tl319.${yr}${mn}${dd}
   done
done
done
done
