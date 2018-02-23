#!/usr/bin/env python
"""
Copyright 2017 ARC Centre of Excellence for Climate Systems Science

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

 This script is used to download, checksum and update the TRMM dataset on
   NCI server raijin
 dataset is in /g/data1/ua8/CMEMS_SeaLevel
 scripts and checksums files are currently in /g/data1/ua8/Download/CMEMS_SeaLevel
 Last change:
      2017-05-24

 Usage:
 Inputs are:
   y - year to check/download/update the only one required
   c - to indicate that year is current, 
       this will call the download_dir function first,
       to check if there are new files to download 
   f - this forces local chksum to be re-calculated even if local file exists
 The script will look for the local and remote checksum files:
     trmm_<local/remote>_cksum_<year>.txt
 If the local file does not exists calls calculate_cksum() to create one
 If the remote cksum file does not exist calls retrieve_cksum() to create one
 The remote checksum are retrieved directly from the cksum field in 
   the filename.xml available online.
 The checksums are compared for each files and if they are not matching 
   the local file is deleted and download it again using the requests module
 The requests module also handle the website cookies by opening a session
   at the start of the script
 
 Uses the following modules:
 import FTP to download files via ftp
 import subprocess to run cksum as a shell command
 import argparse to manage inputs 
 import haslib to calculate md5sum
 should work with both python 2 and 3

"""

from __future__ import print_function

import os, sys
import argparse
import subprocess
import hashlib
from ftplib import FTP


def parse_input():
    ''' Parse input arguments '''
    parser = argparse.ArgumentParser(description='''Retrieve files and checksum values for the CMEMS SeaLevel nc.gz 
             files from CMEMS ftp server using FTP module. 
             Usage: python aviso-download.py -y <year> [-c/--current] ''', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-y','--year', type=int, help='year to process', required=True)
    parser.add_argument('-c','--current', help='current year, download always first',
                        action='store_true', required=False)
    return vars(parser.parse_args())


def retrieve_md5(filelist,fremote):
    ''' calculate md5sum for remote files via ftp 
        param: filename: filename 
        :returns: md5 checksum for file '''
    global session, syr
    dremote={}
    session.cwd(syr)
    for f in filelist:
        fgz = f+".gz"
        m = hashlib.md5()
        session.retrbinary('RETR %s' % fgz, m.update)
        dremote[fgz] = m.hexdigest()
        fremote.write(fgz + " " + dremote[fgz])
    session.cwd("../")
    return  dremote


def read_sums(fopen,kind):
    ''' read checksum values for checksum files from respective yearly files '''
    dresult={}
    for l in fopen.readlines():
        bits = l.replace("\n","").split(" ")
        if kind=='local': dresult[bits[1]] = bits[0]
        if kind=='remote': dresult[bits[0]] = bits[1]
    return dresult


def compare_sums(dlocal,dremote, down_set):
    '''Compare remote and local checksums if they're different re-download file '''
    for fname in sorted(dlocal.keys()):
        if fname not in dremote.keys():
            print('there is no remote cksum for file ', fname) 
        elif dlocal[fname] != dremote[fname]:
            print('problem with ' , fname)
            print( dlocal[fname], dremote[fname])
            local_file = "/".join([data_dir,syr,fname])
            update_file(fname,local_file)
            down_set.add(fname)
        else:
            pass
    return down_set

def calculate_cksum(inlist,flocal):
    ''' calculate cksum for local files for year '''
    for f in inlist:
        p = subprocess.Popen("md5sum "+f, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        flocal.write(output)
    return 


def unzip_file(fname):
    ''' unzip download file '''
    p = subprocess.Popen("gunzip "+fname, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print(output)
    print(err)
    return


def update_file(fname,lfile):
    ''' Delete file and download it from scratch '''
    global syr, session, data_dir
    os.remove(lfile.replace(".gz",""))
    download_file(fname,lfile)
    return


def download_file(fname,lfile):
    ''' download file using FTP '''
    global session
    print(lfile)
    with open(lfile, 'wb') as f:
        try:
            print("Trying to download file... " + fname)
            session.retrbinary("RETR " + fname, f.write)
        except Exception, e:
            print(fname + " could not be downloaded:")
            print(e)
        finally:
            f.close()
    return 


def download_dir():
    ''' download entire year directory '''
    global session, syr, dremote, dlocal
    session.cwd(syr)
    down_set = set()
    file_list = []
    session.retrlines("LIST", file_list.append)
    for line in file_list:
        f = line.split(" ")[-1] 
        local_file = "/".join([data_dir,syr,f])
        if(os.path.exists(local_file)):
            if not dremote[f] == dlocal[f] :
                print("file exists to update", f)
                update_file(f,local_file)
                down_set.add(f)
        else:
            download_file(f,local_file)
            down_set.add(f)
    print('Download for year '+ syr + ' is complete')
    return down_set


def open_ftpsession(username,password):
    ''' open a requests session to manage connection to webserver '''
    global ftpHost, ftpDir
    session = FTP(ftpHost)
    session.login(username,password)
    session.cwd(ftpDir)
    return session 


def main():
    global yr, syr, ftpHost, ftpDir, data_dir, session, dremote, dlocal
    # check python version
    if sys.version_info < ( 2, 7):
        # python too old, kill the script
        sys.exit("This script requires Python 2.7 or newer!")
    # define ftp host and directory for SeaLevel CMEMS ftp server and data_dir for local collection
    ftpHost = 'ftp.sltac.cls.fr'
    ftpDir = 'Core/SEALEVEL_GLO_PHY_L4_REP_OBSERVATIONS_008_047/dataset-duacs-rep-global-merged-allsat-phy-l4-v3/'
    data_dir = '/g/data/ua8/CMEMS_SeaLevel/v3-0/'
    run_dir = '/g/data/ua8/Download/CMEMS_SeaLevel/'
    # read year as external argument and move to data directory
    inputs = parse_input()
    yr = inputs["year"]
    syr = str(yr)
    current = inputs["current"]
    try:
        os.chdir(data_dir + syr)
    except:
        os.mkdir(data_dir + syr)
    # open a request session and download cookies
    f = open(run_dir+credentials-file,"r")
    lines = f.readlines()
    uname = lines[0].replace("\n","")
    passw = lines[1].replace("\n","")
    session = open_ftpsession(uname,passw)
    # create list of local netcdf.gz files for year
    file_list=sorted(os.listdir(data_dir + syr))

    # try to open the local checksum file for the year if it doesn't exist create one
    local_file = run_dir + 'local_cksum_' + syr + '.txt'
    if os.path.exists(local_file):
        flocal = open(local_file,'r')
        dlocal = read_sums(flocal,'local')
        flocal.close()
    else:
        print('Local checksum file for year ',syr, ' does not exist,\n new year')
    # get remote checksums from file if exists
    # and save to file
    remote_file=run_dir + 'remote_cksum_' + syr + '.txt'
    if os.path.exists(remote_file):
        fremote=open(remote_file,'r')
        dremote = read_sums(fremote,'remote')
    else:
        print('Remote checksum file for year ', syr, ' does not exist,\n retrieving now')
        fremote=open(remote_file,'w')
        dremote = retrieve_md5(file_list,fremote)
    fremote.close()
    # compare local and remote checksum
    # if current flag is True, download/update the all year first:
    down_set=set()
    if current:
        down_set = download_dir()
    else:
        down_set = compare_sums(dlocal,dremote,down_set)
    if len(down_set) >= 1:
        if os.path.exists(local_file):
            os.remove(local_file)
        flocal = open(local_file,'w')
        if dlocal:
            for k in dlocal.keys():
                flocal.write(dlocal[k] + " " + k + "\n")
        calculate_cksum(down_set, flocal)
        for f in down_set:
            unzip_file(f)
        flocal.close()
     

    


if __name__ == "__main__":
    main()
