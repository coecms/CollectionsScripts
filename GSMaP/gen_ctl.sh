#PBS -N JRA55
#PBS -q normal
#PBS -l walltime=02:00:00
#PBS -l mem=1GB

module load grads/2.0.2
cd /g/data1/ua8/Download/JRA55
#for yr in `seq 1958 2015`
#do
   #for f in `ls /g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_mdl/${yr}/anl_mdl.*.reg_tl319.* `
   for f in `ls /g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_surf/anl_surf.001_pres*.reg_tl319.*18 `
   do
      ./grib2ctl.pl $f  ${f}.idx > ${f}.ctl
      gribmap -e -i ${f}.ctl
   done
#done
