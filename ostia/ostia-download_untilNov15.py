#!/usr/bin/python
from ftplib import FTP
import os
from os.path import join, exists 
import subprocess, hashlib

class DataGetter:
    def __init__(self):
        user = open("/g/data1/ua8/ostia/.ostia")
        details=user.readlines()
        user.close()
        uname=details[0]
        pword=details[1]
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.ftpHost = "data.ncof.co.uk"
        self.ftp = FTP(self.ftpHost)
        self.ftp.login(uname,pword)

    def processDataset(self, datasetName, localDir):
        self.localDir = localDir
        self.yearList = []
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.remoteDir = "/Core/SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/"
        print "Processing dataset..." + datasetName
        os.chdir(self.localDir + datasetName)
        print os.getcwd()
        self.ftp.cwd(self.remoteDir + datasetName) 
        #self.ftp.cwd(datasetName)
        print "ftp ", self.ftp.pwd()
        self.ftp.retrlines("LIST", self.yearList.append)
        for year in self.yearList:
             print year[-4:]
             varList = self.doDirectory(year)
             if varList and year[-4:]=="2015":
                 for var in varList:
                     fileList = self.doDirectory(var)
                     baseDir = os.getcwd()
                     for f in fileList:
                         self.handleFile(baseDir, f)
                     os.chdir("../")
                     print os.getcwd()
                     self.ftp.cwd("../")
                     print "ftp ", self.ftp.pwd()
                 os.chdir("../")
                 print os.getcwd()
                 self.ftp.cwd("../")
                 print "ftp ", self.ftp.pwd()
             else:
                 print "I AM IN ELSE!!!"
                 fileList = []
                 fileList = self.ftp.retrlines("LIST", fileList.append)
                 baseDir = os.getcwd()
                 for f in fileList:
                     self.handleFile(baseDir, f)
                 os.chdir("../")
                 print os.getcwd()
                 self.ftp.cwd("../")
                 print "ftp ", self.ftp.pwd()
        os.chdir("../")
        print os.getcwd()
        self.ftp.cwd("../")
        print "ftp ", self.ftp.pwd()
               

              
         
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
 
    def doDirectory(self, dirLine):
        if(dirLine[0] == 'd'):
            dirName = dirLine[(dirLine.rindex(" ") + 1):]
            #create the LOCAL dataset directory if one 
            #doesn't exist already
            if(not os.path.exists(dirName)):
                os.mkdir(dirName)
            print os.path.exists(dirName), dirName
            os.chdir(dirName)
            print os.getcwd()
            #print dirName
            self.ftp.cwd(dirName)
            print "ftp ", self.ftp.pwd()
            lineList = []
            self.ftp.retrlines("LIST", lineList.append)
            #print self.ftp.dir()
            #print lineList
            return lineList 

    def handleFile(self, baseDir, fileLine):
        if fileLine[0]== '-'  :
            try:    
                line = fileLine[(fileLine.rindex(" ") + 1):]
                filename = line.split(" ")[-1]
                #if filename[0:4] == "2014":
                if baseDir[-4:] == "/sst":
                #self.fileList.append(filename)
                   self.doFile(baseDir, filename)    
                #self.doFile(baseDir, filename)    
                ##pass
            except ValueError:
                pass

    def doFile(self, baseDir, filename):
        curDir = os.getcwd()
        if(os.path.exists(filename)):
            if not self.check_md5sum(filename):
               print "file exists 2 update", filename
               #if(self.downloadFile(filename, True)):
               #     self.updatedFiles.append(os.path.abspath(filename))
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

    
    def downloadFile(self, filename, isUpdate):
        newFile = None
        #newFile = open(filename, "wb")
        
        if(isUpdate):
            newFile = open(filename + ".1", "wb")
        else:
            newFile = open(filename, "wb")
        try:
            try:
                print "Trying to download file... " + filename
                self.ftp.retrbinary("RETR " + filename, newFile.write)
                os.popen("chmod g+rxX " + filename).readline() 
                os.popen("chgrp ua8 " + filename).readline() 
                if(isUpdate):
                    lines = os.popen("mv " + filename + ".1 " + filename).readlines() 
                    if(len(lines) != 0):
                        print lines
                        self.errorFiles.append(filename + " counld not move file")
                        return False
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
        #getter.processDataset("SST_GLO_SST_L4_REP_OBSERVATIONS_010_011", "/g/data1/ua8/ostia/Core1/")
        getter.processDataset("METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2", "/g/data1/ua8/ostia/Core/SST_GLO_SST_L4_NRT_OBSERVATIONS_010_001/")
        #getter.processDataset("SST_GLO_SST_L4_NRT_OBSERVATIONS_010_005", "/g/data1/ua8/ostia/Core/")
        getter.close()
