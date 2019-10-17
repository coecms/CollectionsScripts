#!/bin/bash -l

# assign input variables
dataset=$1
version=$2
version_dir=${2/./-}
nversion=${2/v/}
creator_id=$3
creator_email=$4
name=$5
surname=$6
license=$7
title=$8
doi=$9
center=CLEX
#center=ARCCSS
# create directory in ARCCSS_Data
data_dir=/g/data1/ua8/${center}_Data
cd $data_dir 
mkdir -p ${dataset}/${version_dir}
mkdir -p ${dataset}/tmp
# copy and adapt license and readme files
cp /home/581/pxp581/Collections_scripts/Publishing_templates/license-${license}-${center}.txt ${dataset}/license.txt
cp /home/581/pxp581/Collections_scripts/Publishing_templates/readme.txt ${dataset}/.
cp /home/581/pxp581/Collections_scripts/Publishing_templates/cf_template.sh ${dataset}/attributes_cf.sh
sed -i -e "s/<version>/${version}/" "${dataset}/license.txt"
sed -i -e "s/<version>/${version}/" "${dataset}/readme.txt"
sed -i -e "s/<version>/${version}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<nversion>/${nversion}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<version_dir>/${version_dir}/" "${dataset}/readme.txt"
sed -i -e "s/<dataset>/${dataset}/" "${dataset}/readme.txt"
sed -i -e "s/<dataset>/${dataset}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<title>/${title}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<name>/${name}/" "${dataset}/readme.txt"
sed -i -e "s/<surname>/${surname}/" "${dataset}/readme.txt"
sed -i -e "s/<title>/${title}/" "${dataset}/readme.txt"
sed -i -e "s/<title>/${title}/" "${dataset}/license.txt"
sed -i -e "s/<license>/${license}/" "${dataset}/license.txt"
sed -i -e "s/<name>/${name}/" "${dataset}/license.txt"
sed -i -e "s/<creator_email>/${creator_email}/" "${dataset}/license.txt"
sed -i -e "s/<surname>/${surname}/" "${dataset}/license.txt"
sed -i -e "s/<license>/${license}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<creator_email>/${creator_email}/" "${dataset}/readme.txt"
sed -i -e "s/<creator_email>/${creator_email}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<name>/${name}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<surname>/${surname}/" "${dataset}/attributes_cf.sh"
sed -i -e "s/<doi>/${doi}/" "${dataset}/attributes_cf.sh"
# set permissions
setfacl -R -m u:${creator_id}:rwX ${dataset}
setfacl -R -m d:u:${creator_id}:rwX ${dataset}
# so I can move files around
setfacl -R -m u:pxp581:rwX ${dataset}
setfacl -R -m d:u:pxp581:rwX ${dataset}
# so thredds can crawl the data
setfacl -R -m d:o::rX ${dataset}
setfacl -R -m o::rX ${dataset}



