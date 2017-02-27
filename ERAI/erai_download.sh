#!/bin/bash -l
# set up environment to run erai_download.py
module load python/2.7.3
export PYTHONPATH=/apps/python/2.7.3/lib:/apps/python/2.7.3/include:/apps/python/2.7.3/bin:/home/581/pxp581/ecmwf-api-client-python
export PATH=$PATH:/home/581/pxp581/ecmwf-api-client-python

# check which is last year and month downloaded
cd /g/data1/ub4/erai/grib/oper_an_sfc/fullres/
filelist=($(ls ei_oper_an_sfc_075x075_90N0E90S35925E_201* | sort ))
lastfile=${filelist[${#filelist[@]}-1]}
echo "last downloaded file is ${lastfile}"
date=$(echo $lastfile | cut -d'_' -f 7)
yr=${date[@]:0:4}
mn=${date[@]:4:2}
# define year and month for next download
# 10#$mn  force decimal (base 10)
nextmn=$((10#$mn + 1))
# if next month is 13 then change nextmn to 01 and yr to next year
if [ ${nextmn} = "13" ]; then
    $nextmn = "01"
    $yr = $((yr + 1))
fi
mn=$(printf "%02d" $nextmn)
echo "next month to download is ${yr} ${mn}"
# finally run the erai_download.py script for each of the 6 streams
cd /g/data1/ua8/Download/ERAI
python erai_download.py -t oper_an_ml -y $yr -m $mn  > tmp_log_an_ml_${yr}.txt &
python erai_download.py -t oper_an_pl -y $yr -m $mn  > tmp_log_an_pl_${yr}.txt &
python erai_download.py -t oper_an_pt -y $yr -m $mn  > tmp_log_an_pt_${yr}.txt &
python erai_download.py -t oper_an_sfc -y $yr -m $mn > tmp_log_an_sfc_${yr}.txt &
python erai_download.py -t oper_fc_sfc -y $yr -m $mn > tmp_log_fc_sfc_${yr}.txt &
            
# wait at least 25 min and then check if files are empty
# if they're not empty than download also oper_an_pv and after further wait concatanate tmp log to proper log
#sleep 1m 
#echo $( ls ei_oper_an_ml_075x075_90N0E90S35925E_${yr}${mn}01_*)
sleep 25m 
if [ -s $( ls ei_oper_an_ml_075x075_90N0E90S35925E_${yr}${mn}01_*) ]; 
then 
    python erai_download.py -t oper_an_pv -y $yr -m $mn  > tmp_log_an_pv_${yr}.txt &
    sleep 5h 
    #echo 'file is empty'
    #sleep 5m 
    logs=($(ls tmp_log_*.txt | sort ))
    for file in ${logs[@]}; do
        echo $file
        #cat $file >>  ${file[@:5]}
        echo ${file[@:5]}
    done
fi




