#!/usr/bin/env python
"""
Copyright 2018 ARC Centre of Excellence for Climate Systems Science

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
   y - run to check/download/update the only one required
   c - to indicate that run is current, 
       this will call the download_dir function first,
       to check if there are new files to download 
   f - this forces local chksum to be re-calculated even if local file exists
 The script will look for the local and remote checksum files:
     gpcp_<local/remote>_cksum_<run>.txt
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
 import subprocess to run cksum as a shell command
 import argparse to manage inputs 
 should work with both python 2 and 3

"""

from __future__ import print_function

import os, sys
import argparse
import subprocess
import requests
from bs4 import BeautifulSoup
import re


def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='''Retrieve checksum value for the GPCP netcdf 
             files directly from GPCP http server using xml.etree to read the corresponding field. 
             Usage: python gpcp-download-check.py -r <run>  ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-e','--ensemble', help='run to process', required=True)
    parser.add_argument('-f','--frequency', help='current run, download always first', required=True)
    parser.add_argument('-r','--realm', help='force local cheksum calculation even if file is present', required=True)
    return vars(parser.parse_args())


def retrieve_xml(hdf_list,fremote):
    ''' extract from the online xml files the checksums and save them to a file
        input: hdf_list a list of all the HDF files in the "run" directory '''
    global http_url, session
    dremote={}
    # from each filename derived the complete url for the corresponding XML file online
    # access Checksum from xml field CheckSumValue and save to file
    for fhdf in hdf_list:
        fyr,fday = get_tstamp(fhdf)
    return dremote
        

def calculate_cksum(hdf_list,flocal):
    ''' calculate cksum for local files for run '''
    dlocal={}
    for fhdf in hdf_list: 
        p = subprocess.Popen("cksum "+fhdf, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        dlocal[fhdf] = output.split(" ")[0]
        flocal.write(output) 
    return dlocal
    

def read_sums(fopen,kind):
    ''' read checksum values for checksum files from respective runly files '''
    dresult={}
    for l in fopen.readlines():
        bits = l.replace("\n","").split(" ")
        if kind=='local': dresult[bits[2]] = bits[0]
        if kind=='remote': dresult[bits[0]] = bits[1]
    return dresult


def compare_sums(dlocal,dremote):
    '''Compare remote and local checksums if they're different re-download file '''
    for fname in sorted(dlocal.keys()):
        if fname not in dremote.keys():
            print('there is no remote cksum for file ', fname) 
        elif dlocal[fname] != dremote[fname]:
            print('problem with ' , fname)
            print( dlocal[fname], dremote[fname])
            update_file(fname)
        else:
            pass
    return


def update_file(fname):
    ''' Delete file and download it from scratch '''
    global run, http_url, data_dir
    local_file="/".join([data_dir,run,fname])
    os.remove(local_file)
    print("/".join([http_url,run,fname]))
    download_file("/".join([http_url,run,fname]),local_file)
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
    ''' download entire run directory '''
    global session, http_url, run, subset
    r = session.get(http_url)
    soup = BeautifulSoup(r.content,'html.parser')
    #for link in soup.find_all('a'):
    for link in soup.find_all('a',string=re.compile('^.*b40.*%s.*$' % run)):
        subdir=link.get('href')
        name=link.string
        root='https://www.earthsystemgrid.org/'
        print(root+subdir," , ", name)
        r2 = session.get(root+subdir)
        soup2 = BeautifulSoup(r2.content,'html.parser')
        print('Page start')
        print(soup2)
        print('Page end')
        #for sub in soup2.find_all('a',string=re.compile('^.*%s.*$' % subset)):
        for sub in soup2.find_all('a'):
            href=sub.get('href')
            print(href)
            #local_name="/".join([data_dir,subdir[:4],href])
            #print("/".join([http_url,subdir,href]))
            #if not os.path.exists(local_name):
            #    print(local_name, 'new')
            #    download_file("/".join([http_url,subdir,href]), local_name)
    #print('Download is complete')
    return


def open_session():
    ''' open a requests session to manage connection to webserver '''
    session = requests.session()
    p = session.post("https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.output.html")
    #cookies=requests.utils.dict_from_cookiejar(session.cookies)
    return session 


def main():
    global subset, run, http_url, data_dir, session
    # check python version
    if sys.version_info < ( 2, 7):
        print('This script needs a python version >= 2.7')
        sys.exit()
    # define http_url for GPCC http server and data_dir for local collection
    http_url="https://www.earthsystemgrid.org/dataset/ucar.cgd.ccsm4.output.html"
    data_dir='/g/data/ua8/CCSM/'
    run_dir='/g/data/ua8/Download/CCSM/'
    # read run as external argument and move to data directory
    inputs=parse_input()
    run=inputs["ensemble"]
    freq=inputs["frequency"]
    realm = inputs["realm"]
    if freq in ['mon', 'month']:
        sfreq = 'Monthly'
    elif freq in ['day', 'daily']:
        sfreq = 'Daily'
    else:
        print('Choose valid frequency')
        sys.exit()
    subset= " ".join([realm,'Post Processed Data,',sfreq]) 
    print(subset)
    try:
        os.chdir(data_dir + "/" + run)
    except:
        os.mkdir(data_dir + "/" + run)
    # open a request session and download cookies
    session = open_session()
    # download/update the selected run
    download_dir()
    # create list of local files for run
    #flist=sorted(os.listdir(data_dir + run))

    ## try to open the local checksum file for the run if it doesn't exist create one
    #local_file = run_dir + '/gpcp_local_cksum_' + run + '.txt'
    #if os.path.exists(local_file) and not force:
    #    flocal = open(local_file,'r')
    #    dlocal = read_sums(flocal,'local')
    #else:
    #    print('Local checksum file for run ',run, ' does not exist,\n calculating now')
    #    if force: os.remove(local_file)
    #    flocal = open(local_file,'w')
    #    dlocal = calculate_cksum(flist, flocal)
    #flocal.close()
    ## get remote checksums from file if exists, or retrieve them using xml
    ## and save to file
    #remote_file=run_dir + '/gpcp_remote_cksum_' + run + '.txt'
    #if os.path.exists(remote_file):
    #    fremote=open(remote_file,'r')
    #    dremote = read_sums(fremote,'remote')
    #else:
    #    print('Remote checksum file for run ', run, ' does not exist,\n retrieving now')
    #    fremote=open(remote_file,'w')
    #    dremote = retrieve_xml(flist,fremote)
    #fremote.close()
    ## compare local and remote checksum
    #compare_sums(dlocal,dremote)


if __name__ == "__main__":
    main()
