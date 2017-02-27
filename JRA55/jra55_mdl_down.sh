cd /g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_mdl/$1
wget -O Authentication.log --save-cookies auth.rda_ucar_edu --post-data="email=paola.petrelli@utas.edu.au&passwd=FM27g2010&action=login"  https://rda.ucar.edu/cgi-bin/login
for mn in `seq --format="%02.f" 1 12`;
do
  for sday in 01 11 21;
  do
     eday=$((sday+9))
     if [ "$eday" == "30" ] && [[ "01 03 05 07 08 10 12" =~ $mn ]]; then
        eday=31
     fi
     if [ "$eday" == "30" ] && [ "$mn" = "02" ]; then
        eday=28
     fi
##watch out for irregular years and Feb  1960 64 68 72 76 80 84 88 92 96 2000 04 08 12 16

wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_mdl/$1/anl_mdl.007_hgt.reg_tl319.${1}${mn}${sday}00_${1}${mn}${eday}18
wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_mdl/$1/anl_mdl.011_tmp.reg_tl319.${1}${mn}${sday}00_${1}${mn}${eday}18
wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_mdl/$1/anl_mdl.033_ugrd.reg_tl319.${1}${mn}${sday}00_${1}${mn}${eday}18
wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_mdl/$1/anl_mdl.034_vgrd.reg_tl319.${1}${mn}${sday}00_${1}${mn}${eday}18
wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_mdl/$1/anl_mdl.051_spfh.reg_tl319.${1}${mn}${sday}00_${1}${mn}${eday}18

  done
done
