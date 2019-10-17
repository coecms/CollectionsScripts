#!/bin/bash -l
# this is partially filled template to make the files compliant with CF1.6 and ACDD1.3 metadata conventions.
module load nco
cd /g/data1/ua8/ARCCSS_Data/<dataset>/tmp/
# correct variable attributes
# if attribute exist already use o,c instead of c,c to overwrite rather than create
# if attribute is not a character change type i.e. float use c,f, 
# available types are: float (f), double (d), long (l), short (s)
#                      char (c), byte (b)
#ncatted -h -O -a standard_name,<varname>,c,c,"<standard-name>" $1
#ncatted -h -O -a long_name,<varname>,c,c,"<long-name>" $1
#ncatted -h -O -a units,<varname>,c,c,"<units>" $1
#ncatted -h -O -a cell_methods,<varname>,c,c,"<axis>: <method>" $1
# delete extra attribute
# ncatted -h -O -a <att-name>,<var-name>,d,, $1
# ncatted -h -O -a <att-name>,global,d,, $1 
ncatted -h -O -a Conventions,global,o,c,"CF-1.6, ACDD-1.3" $1
ncatted -h -O -a title,global,o,c,"<title> <version>" $1
ncatted -h -O -a summary,global,c,c,"" $1
ncatted -h -O -a source,global,c,c,"" $1
ncatted -h -O -a license,global,c,c,"http://creativecommons.org/licenses/<license>/4.0/" $1
ncatted -h -O -a id,global,c,c,"http://dx.doi.org/<doi>" $1
ncatted -h -O -a product_version,global,c,c,"<nversion>" $1
ncatted -h -a contact,global,c,c,"<creator_email>" $1
ncatted -h -O -a institution,global,c,c,"" $1
ncatted -h -O -a organisation,global,c,c,"ARC Centre of Excellence for Climate System Science" $1
ncatted -h -O -a references,global,c,c,"<surname>, <name>, <year>: <title> <version> . NCI National Research Data Collection , doi:<doi> <publication>" $1
# keywords is a list of words separated by commas: Climate, Precipitation
ncatted -h -O -a keywords,global,c,c,"<keywords>" $1
ncatted -h -O -a date_created,global,c,c,"<date-created>" $1
ncatted -h -O -a creator_name,global,c,c,"<name> <surname>" $1
ncatted -h -O -a creator_email,global,c,c,"<creator_email>" $1
ncatted -h -O -a publisher_name,global,c,c,"ARCCSS data manager" $1
ncatted -h -O -a publisher_email,global,c,c,"paola.petrelli@utas.edu.au" $1
# time coverage format is YYYY-MM-DD optional hh:ss
ncatted -h -O -a time_coverage_start,global,c,c,"<from-date>" $1
ncatted -h -O -a time_coverage_end,global,c,c,"<to-date>" $1
ncatted -h -O -a geospatial_lat_min,global,c,d,<minlat> $1
ncatted -h -O -a geospatial_lat_max,global,c,d,<maxlat> $1
ncatted -h -O -a geospatial_lon_min,global,c,d,<minlon> $1
ncatted -h -O -a geospatial_lon_max,global,c,d,<maxlon> $1
