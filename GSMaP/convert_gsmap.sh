#PBS -N JRA55
#PBS -q normal 
#PBS -l walltime=10:00:00
#PBS -l mem=6GB

module load netcdf
module use /g/data1/r87/public/modulefiles
module load python/2.7.5 python-cdat-lite cct
#export PYTHONPATH=/home/599/tae599/src/cct/pythonlib/

cd /g/data/ua8/Download/GSMaP

for yr in 200003 ; do

for f in raw/reanalysis_gauge/daily/00Z-23Z/$yr/gsmap_rnl_gauge.ctl
#for f in raw/reanalysis_gauge/daily/00Z-23Z/$yr/gsmap_rnl_gauge*.ctl
  do  
    python ctl2nc.py $f
done
done
