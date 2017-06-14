#!/usr/bin/python
#from ftplib import FTP
import pysftp
import os
from os.path import join, exists 
import subprocess, hashlib

class DataGetter:
    def __init__(self):
        user = open("/g/data1/ua8/Download/GLEAM/.gleam")
        details=user.readlines()
        user.close()
        uname=details[0].replace('\n','')
        pword=details[1].replace('\n','')
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.ftpHost = "hydras.ugent.be"
        self.ftpPort = 2225
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys.load('/g/data1/ua8/Download/GLEAM/.gleam_hostkeys') 
        self.ftp = pysftp.Connection(host=self.ftpHost,
                                     port=self.ftpPort,
                                     username=uname,
                                     password=pword,
                                     cnopts=cnopts)
                                     #password=pword)


    def processDataset(self, datasetName, localDir):
        self.localDir = localDir
        self.yearList = []
        self.updatedFiles = []
        self.newFiles = []
        self.errorFiles = []
        self.remoteDir = "data/"
        print "Processing dataset..." + datasetName
        os.chdir(self.localDir)
        print os.getcwd()
        print self.ftp.pwd
        self.ftp.cwd(self.remoteDir + datasetName) 
        print "ftp ", self.ftp.pwd
        yearList=self.ftp.listdir()
        for year in yearList:
            fileList = self.doDirectory(year)
            baseDir = os.getcwd()
            for f in fileList:
                self.handleFile(baseDir, f, year)
            os.chdir("../")
            print os.getcwd()
            self.ftp.cwd("../")
            print "ftp ", self.ftp.pwd
        os.chdir("../")
        print os.getcwd()
        self.ftp.cwd("../../")
        print "ftp ", self.ftp.pwd
               

              
         
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
 
    def doDirectory(self, dirName):
        #create the LOCAL dataset directory if one 
        #doesn't exist already
        if(not os.path.exists(dirName)):
            os.mkdir(dirName)
        print os.path.exists(dirName), dirName
        os.chdir(dirName)
        print os.getcwd()
        #print dirName
        self.ftp.cwd(dirName)
        print "ftp ", self.ftp.pwd
        fileList = self.ftp.listdir()
        return fileList 

    def handleFile(self, baseDir, filename, year):
        if filename[-3:]== '.nc' :
            try:    
                self.doFile(baseDir, filename)    
            except ValueError:
                pass

    def doFile(self, baseDir, filename):
        curDir = os.getcwd()
        if(os.path.exists(filename)):
            if not self.check_md5sum(filename):
               print "file exists 2 update", filename
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
        local_md5=local_md5.split(" ")[0]
        return local_md5 == ftp_md5

    
    def downloadFile(self, filename, isUpdate):
        #newFile = None
        #newFile = open(filename, "wb")
        
        #if(isUpdate):
        #    newFile = open(filename + ".1", "wb")
        #else:
        #    newFile = open(filename, "wb")
        try:
            try:
                print "Trying to download file... " + filename
                self.ftp.get(filename, preserve_mtime=True)
                os.popen("chmod g+rX " + filename).readline() 
                os.popen("chgrp wd9 " + filename).readline() 
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
            #newFile.close()
            pass


    def close(self):
        self.ftp.close()

if __name__ == "__main__":
        getter = DataGetter()
        #getter.processDataset("v3.1c", "/g/data1/wd9/BenchMarking/GLEAM_v3-1/v3-1c/")
        getter.processDataset("v3.1a", "/g/data1/wd9/BenchMarking/GLEAM_v3-1/v3-1a/")
        getter.processDataset("v3.1b", "/g/data1/wd9/BenchMarking/GLEAM_v3-1/v3-1b/")
        getter.close()
# data/v3.1c/2011/E_2011_GLEAM_v3.1c.nc
