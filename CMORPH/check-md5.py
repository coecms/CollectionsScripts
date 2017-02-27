#!/usr/bin/python
from ftplib import FTP
import os, time
from os.path import join, exists 
import subprocess, hashlib
from datetime import datetime
from time import gmtime

class DataGetter:
    def __init__(self):
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.ftpHost = "ftp.cpc.ncep.noaa.gov"
        self.ftp = FTP(self.ftpHost)
        self.ftp.login()

    def processDataset(self, datasetName, localDir):
        self.localDir = localDir
        self.yearList = []
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.remoteDir = "/precip/CMORPH_V1.0/RAW/"
        print "Processing dataset..." + datasetName
        os.chdir(self.localDir + datasetName)   # go to dataset dir
        #print os.getcwd()
        self.ftp.cwd(self.remoteDir + datasetName) 
        #print "ftp ", self.ftp.pwd()
        self.ftp.retrlines("LIST", self.yearList.append)
        for year in self.yearList:
             print year[-4:]
             mnList = self.doDirectory(year,True)
             if mnList and year[-4:]=='1998':
                 locmd5=self.read_localmd5()
                 baseDir = os.getcwd()
                 for f in mnList:
                     self.handleFile(baseDir, f, locmd5)
                 self.ftp.cwd("../")      # get out of year dir
                 os.chdir("../")     #get out of year dir
             else:
                 fileList = []
                 fileList = self.ftp.retrlines("LIST", fileList.append)
                 baseDir = os.getcwd()
                 for f in fileList:
                     self.handleFile(baseDir, f)
                 os.chdir("../")  # get out of year dir to skip or containing only files
                 #print os.getcwd()
                 self.ftp.cwd("../")
                 #print "ftp ", self.ftp.pwd()
        os.chdir("../")   # get out of dataset dir
        #print os.getcwd()
        self.ftp.cwd("../")
        #print "ftp ", self.ftp.pwd()
               

              
         
        print "======================================================="
        print "Summary for " + datasetName
        print "======================================================="
        print "These files were updated: "
        for f in self.updatedFiles:
            print f
        print "======================================================="
        print "These are new files: "
        for f in self.newFiles:
            print f
        print "======================================================="
        print "These files and problems: " 
        for f in self.errorFiles:
            print f
 
    def doDirectory(self, dirLine, makedir):
        if(dirLine[0] == 'd'):
            dirName = dirLine[(dirLine.rindex(" ") + 1):]
            if makedir:
               if(not os.path.exists(dirName)):
                  os.mkdir(dirName)
               print os.path.exists(dirName), dirName
               os.chdir(dirName)  # go to "year" dir
            self.ftp.cwd(dirName)
            #print "ftp ", self.ftp.pwd()
            lineList = []
            self.ftp.retrlines("LIST", lineList.append)
            return lineList 

    def handleFile(self, baseDir, fileLine, locmd5):
        if fileLine[0]== '-'  :
            try:    
                line = fileLine[(fileLine.rindex(" ") + 1):]
                filename = line.split(" ")[-1]
                if filename[-4:]==".tar":
                   self.doFile(baseDir, filename, locmd5)    
            except ValueError:
                pass

    def doFile(self, baseDir, filename, locmd5):
        curDir = os.getcwd()
        if(os.path.exists(filename)):
            local_md5 = locmd5[filename]
            if not self.check_md5sum(filename, local_md5):
               print "file exists to update", filename
        else:
            print "file exists to download", filename


    def check_md5sum(self, filename, local_md5):
        ''' Execute md5sum on file on raijin and return True,if same as ftp file '''
        m = hashlib.md5()
        self.ftp.retrbinary('RETR %s' % filename, m.update)
        ftp_md5 =  m.hexdigest()
        print local_md5, ftp_md5, filename
        return local_md5 == ftp_md5


    def read_localmd5(self):
        '''Read local md5sum from file and load as dictionary'''
        locmd5={}
        fmd5=open('original_md5sum.txt','r')
        #lines=fmd5.readlines
        for line in fmd5.readlines():
            md5,name=line.split("  ")
            name=name.replace("\n","") 
            locmd5[name]=md5
        return locmd5

    def close(self):
        self.ftp.quit()

if __name__ == "__main__":
        getter = DataGetter()
        getter.processDataset("8km-30min", "/g/data1/ua8/CMORPH/CMORPH_V1.0/raw/")
        getter.close()
