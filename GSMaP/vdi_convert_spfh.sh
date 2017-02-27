#PBS -N JRA55
#PBS -q normal 
#PBS -l walltime=10:00:00
#PBS -l mem=16GB

module load netcdf
module use /g/data1/r87/public/modulefiles
module load python/2.7.5 python-cdat-lite cct
#export PYTHONPATH=/home/599/tae599/src/cct/pythonlib/

cd /g/data/ua8/Yotc_Down/JRA55

for yr in 1958 ; do

for f in raw/Hist/Daily/anl_mdl/$yr/anl_mdl_spfh.ctl
  do  
    python ctl2nc.py $f
done
done
