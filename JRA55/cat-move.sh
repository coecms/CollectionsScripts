#PBS -N catJRA 
#PBS -q normal
#PBS -l walltime=04:00:00
#PBS -l mem=32GB

module load cdo 
cd /g/data1/ua8/Download/JRA55/conv_mdl
var=ta
for yr in `seq 1958 1964`; do
  for mn in `seq --format="%02.f" 1 12`; do
     td=31
     if [[ "04 06 09 11" =~ $mn ]]; then
        td=30
     fi
     if [ "$mn" = "02" ]; then
        td=28
     fi
     if [ "$mn" = "02" ] && [[ "1960 1964 1968 1972 1976 1980 1984 1988 1992 1996 2000 2004 2008 2012 2016 2020" =~ $yr ]]; then
        td=29
     fi
     #echo ${var}_6hrLev_JRA55_reg-tl319_${yr}${mn}0100-${yr}${mn}${td}18.nc

      cdo cat ${var}_6hrLev_JRA55_reg-tl319_${yr}${mn}*.nc cat_${var}_6hrLev_JRA55_reg-tl319_${yr}${mn}0100-${yr}${mn}${td}18.nc
      mv  cat_${var}_6hrLev_JRA55_reg-tl319_${yr}${mn}0100-${yr}${mn}${td}18.nc ../conv_mdl3/.
   done
done
