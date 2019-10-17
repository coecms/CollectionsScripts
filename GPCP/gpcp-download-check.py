#!/usr/bin/env python
"""
Copyright 2019 ARC Centre of Excellence for Climate Systems Science

author: Paola Petrelli <paola.petrelli@utas.edu.au>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

 This script is used to download, checksum and update the OISST dataset on
   NCI server raijin
 dataset is in /g/data1/ua8/GPCP
 scripts and checksums files are currently in /g/data1/ua8/Download/GPCP
 Last change:
      2018-01-30

 Usage:
 Inputs are:
   y - year to check/download/update the only one required
   c - to indicate that year is current, 
       this will call the download_dir function first,
       to check if there are new files to download 
   t - timestep mon or day, default day is true
   f - this forces local chksum to be re-calculated even if local file exists
 The script will look for the local and remote checksum files:
     gpcp_<local/remote>_cksum_<year>.txt
 If the local file does not exists calls calculate_cksum() to create one
 If the remote cksum file does not exist calls retrieve_cksum() to create one
 The remote checksum are retrieved directly from the cksum field in 
   the filename.xml available online.
 The checksums are compared for each files and if they are not matching 
   the local file is deleted and download it again using the requests module
 The requests module also handle the website cookies by opening a session
   at the start of the script
 
 Uses the following modules:
 import requests to download files and html via http
 import beautifulsoup4 to parse html
 import xml.etree.cElementTree to read a single xml field
 import time and calendar to convert timestamp in filename
        to day number from 1-366 for each year
 import subprocess to run cksum as a shell command
 import argparse to manage inputs 
 should work with both python 2 and 3

"""

from __future__ import print_function

#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET
import os, sys
import time, calendar
import argparse
import subprocess
import requests
from bs4 import BeautifulSoup
import re


def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='''Retrieve checksum value for the GPCP netcdf 
             files directly from GPCP http server using xml.etree to read the corresponding field. 
             Usage: python gpcp-download-check.py -y <year>  ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-y','--year', type=int, help='year to process', required=True)
    parser.add_argument('-c','--current', help='current year, download always first',
                        action='store_true', required=False)
    parser.add_argument('-t','--tstep', help='timestep either mon or day, day is default',
                        default='day', required=False)
    parser.add_argument('-f','--force', help='force local cheksum calculation even if file is present',
                        action='store_true', required=False)
    return vars(parser.parse_args())


def compare_sums(dlocal,dremote):
    '''Compare remote and local checksums if they're different re-download file '''
    for fname in sorted(dlocal.keys()):
        if fname not in dremote.keys():
            print('there is no remote cksum for file ', fname) 
        elif dlocal[fname] != dremote[fname]:
            print('problem with ' , fname)
            print( dlocal[fname], dremote[fname])
            fyr,fday = get_tstamp(fname)
            update_file(fyr,fday,fname)
        else:
            pass
    return


def update_file(fyr,fname):
    ''' Delete file and download it from scratch '''
    global syr, http_url, data_dir
    local_file="/".join([data_dir,syr,fname])
    os.remove(local_file)
    print("/".join([http_url,fyr,fname]))
    download_file("/".join([http_url,fyr,fname]),local_file)
    return


def download_file(url,fname):
    ''' download file using requests '''
    global session
    r = session.get(url)
    with open(fname, 'wb') as f:
        f.write(r.content)
    del r
    return 


def download_dir():
    ''' download entire year directory '''
    global session, http_url, syr
    r = session.get(http_url)
    soup = BeautifulSoup(r.content,'html.parser')
    for link in soup.find_all('a',string=re.compile('^%s/' % syr)):
        subdir=link.get('href')
        r2 = session.get("/".join([http_url,subdir]))
        soup2 = BeautifulSoup(r2.content,'html.parser')
        for sub in soup2.find_all('a',string=re.compile('^gpcp_.*\.nc$')):
            href=sub.get('href')
            local_name="/".join([data_dir,subdir[:4],href])
            print("/".join([http_url,subdir,href]))
            if not os.path.exists(local_name):
                print(local_name, 'new')
                download_file("/".join([http_url,subdir,href]), local_name)
    print('Download is complete')
    return


def open_session():
    ''' open a requests session to manage connection to webserver '''
    session = requests.session()
    p = session.post("https://www.ncei.noaa.gov/data/global-precipitation-climatology-project-gpcp-daily/access/")
    #cookies=requests.utils.dict_from_cookiejar(session.cookies)
    print(session)
    return session 


def main():
    global yr, syr, http_url, data_dir, session
    # read year as external argument and move to data directory
    inputs=parse_input()
    yr=inputs["year"]
    syr=str(yr)
    current=inputs["current"]
    tstep=inputs["tstep"]
    force=inputs["force"]
    # define http_url for GPCC http server and data_dir for local collection
    if tstep == 'day':
       http_url="https://www.ncei.noaa.gov/data/global-precipitation-climatology-project-gpcp-daily/access/"
       data_dir='/mnt/ua8/GPCP/day/v1-3/'
    else:
       http_url="https://www.ncei.noaa.gov/data/global-precipitation-climatology-project-gpcp-monthly/access/"
       data_dir='/mnt/ua8/GPCP/mon/v2-3/'
    run_dir='/mnt/ua8/Download/GPCP/'
    try:
        os.chdir(data_dir + "/" + syr)
    except:
        os.mkdir(data_dir + "/" + syr)
    # open a request session and download cookies
    session = open_session()
    # download/update the selected year
    download_dir()
    # create list of local files for year
    #flist=sorted(os.listdir(data_dir + syr))

    ## try to open the local checksum file for the year if it doesn't exist create one
    #local_file = run_dir + '/gpcp_local_cksum_' + syr + '.txt'
    #if os.path.exists(local_file) and not force:
    #    flocal = open(local_file,'r')
    #    dlocal = read_sums(flocal,'local')
    #else:
    #    print('Local checksum file for year ',syr, ' does not exist,\n calculating now')
    #    if force: os.remove(local_file)
    #    flocal = open(local_file,'w')
    #    dlocal = calculate_cksum(flist, flocal)
    #flocal.close()
    ## get remote checksums from file if exists, or retrieve them using xml
    ## and save to file
    #remote_file=run_dir + '/gpcp_remote_cksum_' + syr + '.txt'
    #if os.path.exists(remote_file):
    #    fremote=open(remote_file,'r')
    #    dremote = read_sums(fremote,'remote')
    #else:
    #    print('Remote checksum file for year ', syr, ' does not exist,\n retrieving now')
    #    fremote=open(remote_file,'w')
    #    dremote = retrieve_xml(flist,fremote)
    #fremote.close()
    ## compare local and remote checksum
    #compare_sums(dlocal,dremote)


if __name__ == "__main__":
    main()
