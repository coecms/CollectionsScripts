#!/bin/bash -l
cd /From_downloader/ERAI/
wget -p -l 1 -O ecmwf_erai_page.html http://apps.ecmwf.int/datasets/data/interim-full-daily/levtype=sfc/
grep 'class="daterange_max"' ecmwf_erai_page.html
