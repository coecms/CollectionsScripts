for yr in `seq 1958 1959`
do
./grib2ctl.pl /g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_surf/anl_surf.001_pres.reg_tl319.${yr}%m2%d2%h2_${yr}%m2%d2%h2 anl_surf_ps_${yr}.idx >/g/data1/ua8/Download/JRA55/raw/Hist/Daily/anl_surf/anl_surf_ps_${yr}.ctl
gribmap -i raw/Hist/Daily/anl_surf/anl_surf_ps_${yr}.ctl
done
