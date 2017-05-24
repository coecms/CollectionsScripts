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
        self.ftpHost = "disc2.nascom.nasa.gov"
        self.ftp = FTP(self.ftpHost)
        self.ftp.login()

    def processDataset(self, datasetName, localDir):
        self.localDir = localDir
        self.yearList = []
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.remoteDir = "/data/s4pa/TRMM_L3/"
        print "Processing dataset..." + datasetName
        os.chdir(self.localDir + datasetName)   # go to dataset dir
        #print os.getcwd()
        self.ftp.cwd(self.remoteDir + datasetName) 
        #print "ftp ", self.ftp.pwd()
        self.ftp.retrlines("LIST", self.yearList.append)
        for year in self.yearList:
             print year[-4:]
             dayList = self.doDirectory(year,True)
             #if dayList and year[-4:]=="2016":
             if dayList:
                 for day in dayList:
                     fileList = self.doDirectory(day,False)
                     baseDir = os.getcwd()
                     for f in fileList:
                         self.handleFile(baseDir, f)
                     self.ftp.cwd("../")  # get out of day dir
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
               #print os.path.exists(dirName), dirName
               os.chdir(dirName)  # go to "year" dir
               #print os.getcwd()
            self.ftp.cwd(dirName)
            #print "ftp ", self.ftp.pwd()
            lineList = []
            self.ftp.retrlines("LIST", lineList.append)
            return lineList 

    def handleFile(self, baseDir, fileLine):
        if fileLine[0]== '-'  :
            try:    
                line = fileLine[(fileLine.rindex(" ") + 1):]
                filename = line.split(" ")[-1]
                if filename[-5:]=="HDF.Z":
                   #self.fileList.append(filename)
                   self.doFile(baseDir, filename)    
            except ValueError:
                pass

    def doFile(self, baseDir, filename):
        curDir = os.getcwd()
        # for TRMM files need to compare to uncompressed filename
        if(os.path.exists(filename[:-2])):
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
        # for TRMM files need to compare to uncompressed filename
        localModTime = gmtime(os.path.getmtime(filename[:-2]))
        return localModTime < remoteLastModDate.timetuple() 


    def downloadFile(self, filename, isUpdate):
        newFile = None
        
        #print filename
        if(isUpdate):
            #newFile = open(filename + ".1", "wb")
            newFile = open(filename, "wb")
        else:
            newFile = open(filename, "wb")
        try:
            try:
                print "Trying to download file... " + filename
                self.ftp.retrbinary("RETR " + filename, newFile.write)
                os.popen("chmod g+rxX " + filename).readline() 
                os.popen("chgrp ua8 " + filename).readline() 
                #if(isUpdate):
                #    lines = os.popen("mv " + filename + ".1 " + filename).readlines() 
                #    if(len(lines) != 0):
                #        print lines
                #        self.errorFiles.append(filename + " counld not move file")
                #        return False
                return True
            except Exception, e:
                self.errorFiles.append(filename + " could not be downloaded:")
                print e
                return False 
        finally:
            newFile.close()
            try:
                os.popen("gunzip " + filename)
            except:
                print " could not unzip file", filename


    def close(self):
        self.ftp.quit()

if __name__ == "__main__":
        getter = DataGetter()
        getter.processDataset("TRMM_3B42", "/g/data1/ua8/NASA_TRMM/TRMM_L3/")
        getter.close()
