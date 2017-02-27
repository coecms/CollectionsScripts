#!/usr/bin/python
from ftplib import FTP
import os, time
import zipfile
from os.path import join, exists 
import subprocess, hashlib
from datetime import datetime
from time import gmtime

class DataGetter:
    def __init__(self):
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.ftpHost = "eclipse.ncdc.noaa.gov"
        self.ftp = FTP(self.ftpHost)
        self.ftp.login()

    def processDataset(self, datasetName, localDir):
        self.localDir = localDir
        self.yearList = []
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.remoteDir = "/pub/OI-daily-v2/NetCDF/"
        print "Processing dataset..." + datasetName
        os.chdir(self.localDir + datasetName + "/raw")   # go to dataset dir
        #print os.getcwd()
        self.ftp.cwd(self.remoteDir) # got to ftp dataset dir 
        #print "ftp ", self.ftp.pwd()
        self.ftp.retrlines("LIST", self.yearList.append)
        for year in self.yearList:
             print year[-4:]
             if year[-4:-3]=="2":
                 fileList = self.doDirectory(year,datasetName,True)
                 baseDir = os.getcwd()
                 for f in fileList:
                     self.handleFile(baseDir, f)
                 self.ftp.cwd("../../")  # get out of ftp year dir
                 #print "ftp ", self.ftp.pwd()
                 os.chdir("../")     #get out of local year dir
                 #print os.getcwd()
        os.chdir("../../")   # get out of local dataset dir
        #print os.getcwd()
        self.ftp.cwd("../")  # get out of ftp dataset dir 
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
 
    def doDirectory(self, dirLine, datasetName, makedir):
        if(dirLine[0] == 'd'):
            dirName = dirLine[(dirLine.rindex(" ") + 1):]
            if makedir:
               if(not os.path.exists(dirName)):
                  os.mkdir(dirName)
               #print os.path.exists(dirName), dirName
               os.chdir(dirName)  # go to "year"/"month" dir
               #print os.getcwd()
            self.ftp.cwd(dirName+"/"+datasetName)
            #print "ftp ", self.ftp.pwd()
            lineList = []
            self.ftp.retrlines("LIST", lineList.append)
            return lineList 

    def handleFile(self, baseDir, fileLine):
        if fileLine[0]== '-'  :
            try:    
                line = fileLine[(fileLine.rindex(" ") + 1):]
                filename = line.split(" ")[-1]
                if filename[-5:]=="nc.gz":
                   #self.fileList.append(filename)
                   self.doFile(baseDir, filename)    
            except ValueError:
                pass

    def doFile(self, baseDir, filename):
        curDir = os.getcwd()
# if files exists already compare to one online to check if need updating
        if(os.path.exists(filename)):
            if self.check_mdt(filename):
               print "file exists to update", filename
               if(self.downloadFile(filename, True)):
                    self.updatedFiles.append(os.path.abspath(filename))
        else:
            if(self.downloadFile(filename, False)):
                self.newFiles.append(os.path.abspath(filename))


    def check_md5sum(self, filename):
        ''' Execute md5sum on file on raijin and return True,if same as ftp file '''
        m = hashlib.md5()
        self.ftp.retrbinary('RETR %s' % filename, m.update)
        ftp_md5 =  m.hexdigest()
        # use this is working on raijin
        #local_md5 = subprocess.check_output(["md5sum", filename]).split()[0]
        # use this is working on downloader 
        local_md5 = subprocess.Popen(['md5sum', filename], stdout=subprocess.PIPE).communicate()[0]
        print local_md5, ftp_md5, filename
        return local_md5 == ftp_md5


    def check_mdt(self,filename):
        result = self.ftp.sendcmd("MDTM " + filename)
        remoteLastModDate = datetime(*(time.strptime(result[4:], "%Y%m%d%H%M%S")[0:6]))
        localModTime = gmtime(os.path.getmtime(filename))
        if (os.stat(filename).st_size == 0):
           return  True 
        return localModTime < remoteLastModDate.timetuple() 


    def downloadFile(self, filename, isUpdate):
        newFile = None
        
        #print filename
        newFile = open(filename, "wb")
        try:
            try:
                print "Trying to download file... " + filename
                self.ftp.retrbinary("RETR %s" % filename, newFile.write)
                os.popen("chmod g+rxX " + filename).readline() 
                os.popen("chgrp rr7 " + filename).readline() 
                return True
            except Exception, e:
                self.errorFiles.append(filename + " could not be downloaded:")
                print e
                return False 
        finally:
            newFile.close()


    def close(self):
        self.ftp.quit()

if __name__ == "__main__":
        getter = DataGetter()
        getter.processDataset("AVHRR", "/g/data1/ua8/NOAA_OISST/")
        getter.close()
