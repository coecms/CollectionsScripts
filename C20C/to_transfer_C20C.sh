#!/bin/bash
# This script irun rsync command to transfer/update C20C collection from CORI server at NERSC
# take as argument subdir to transfer
# currently available subdirs are:
# C20C: last update 04 Feb finished
# LBNL:             04 Feb  *
# MIROC:            04 Feb finished 
# rsync error: some files/attrs were not transferred (see previous errors) (code 23) at main.c(1505) [generator=3.0.6]
# I think these are some files for which i didn't have permissions
# UCT-CSAG          04 Feb finished
# ETH               04 Feb * 
# HAPPI             04 Feb finished 
# MOHC              04 Feb finished 
# NOAA-ESRLandCIRES 04 Feb finished
# New subdirs from last update:
# CCCma  828Gb      04Feb finished
# NCC               04 Feb * 
# ClimateAnalytics  05 Feb finished 
# MPI-M            04 Feb finished 

#switchproj ua8
rsync  -rvL --append-verify paolap@cori.nersc.gov://project/projectdirs/m1517/C20C/$1/ /g/data1/ua8/C20C/$1
