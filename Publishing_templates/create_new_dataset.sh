#!/bin/bash -l

# assign input variables
dataset=$1
version=$2
version_dir=${2/./-}
creator_id=$3
creator_email=$4
# create directory in ARCCSS_Data
cd /g/data1/ua8/ARCCSS_Data
mkdir -p ${dataset}/${version_dir}
mkdir -p ${dataset}/tmp
# copy and adapt license and readme files
cp /home/581/pxp581/Publishing_templates/license.txt ${dataset}/.
cp /home/581/pxp581/Publishing_templates/readme.txt ${dataset}/.
sed -i -e "s/<version>/${version}/" "${dataset}/license.txt"
sed -i -e "s/<version>/${version}/" "${dataset}/readme.txt"
sed -i -e "s/<version_dir>/${version_dir}/" "${dataset}/readme.txt"
sed -i -e "s/<dataset>/${dataset}/" "${dataset}/readme.txt"
sed -i -e "s/<creator_email>/${creator_email}/" "${dataset}/readme.txt"
# set permissions
setfacl -R -m u:${creator_id}:rwX ${dataset}
setfacl -R -m d:u:${creator_id}:rwX ${dataset}
# so I can move files around
setfacl -R -m u:pxp581:rwX ${dataset}
setfacl -R -m d:u:pxp581:rwX ${dataset}
# so thredds can crawl the data
setfacl -R -m d:o::rX ${dataset}
setfacl -R -m o::rX ${dataset}



