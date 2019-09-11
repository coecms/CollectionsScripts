cd /g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_surf
wget -O Authentication.log --save-cookies auth.rda_ucar_edu --post-data="email=&action=login"  https://rda.ucar.edu/cgi-bin/login
#for yr in `seq 1958 2013`;
#do
#wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_surf/$yr/anl_surf.001_pres.reg_tl319.${yr}010100_${yr}123118
#done
for yr in `seq 2014 2016`;
do
for mn in `seq --format="%02.f" 1 12`;
do
     eday=30
     if [[ "01 03 05 07 08 10 12" =~ $mn ]]; then
        eday=31
     fi
     if [ "$mn" = "02" ]; then
        eday=28
     fi
     if [ "$yr" == "2016" ] && [ "$mn" = "02" ]; then
        eday=28
     fi

wget -N --load-cookies auth.rda_ucar_edu http://rda.ucar.edu/data/ds628.0/anl_surf/$yr/anl_surf.001_pres.reg_tl319.${yr}${mn}0100_${yr}${mn}${eday}18
done
done
