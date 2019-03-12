# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import subprocess
import os
import datetime
import sqlite3
import glob
import json
import time
import re
import pprint
import codecs
import shutil

report = open("report.txt", "w+", 1)

homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'
fileFound = {}
dupCount = {}

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)


def dateConversion(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''

    date = str(timestamp)
    nDate = date[:-3]
    conv = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(nDate)))
    return(conv)

def chromeDateTimeConv(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    format = epoch_start + delta
    return format.strftime("%d/%m/%y %H:%M:%S")


def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''

    fileSig = {"PNG": ".png",
                "JPG": ".jpg",
                "DB": ".db",
                "MP3": ".mp3",
                "MP4": ".mp4",
                "GIF": 	".gif",
                "MOV": ".mov",
                "flv": ".flv",
                "avi": ".avi",
                "WMV": ".wmv",
                "WAV": ".wav",
                "wma": ".wma",
                "FLV": ".flv",
                "XML": ".xml",
                "APK": ".apk",
                "TIFF": ".tif"}

    print(dt(), "Analysing File Signatures")
    for root, directories, files in os.walk(folder):   # For folders/files in rawdump
        for file in files:
            for key, value in fileSig.items():
                if file.endswith(value):  # Iterate over File types & Signatures
                    print(file)
                    path = os.path.join(root, file)
                    if key not in fileFound:
                        fileFound[key] = {}
                    fileFound[key][file] = path
    pprint.pprint(fileFound)


def evidenceGathering():
    '''Moves evidence to an evidence folder for each found filetype'''
    print(dt(), "Gathering Evidence")
    for key, value in fileFound.items():
        for item in value:
            evidence = "evidence/"+key
            for file, path in value.items():
                try:  # Make directory if doesnt exist, error raised if it does exist
                    os.makedirs(evidence)
                except OSError:
                    if not os.path.isdir(evidence):
                        raise
                try:  # Copy file to evidence folder
                    shutil.move(path, evidence)
                except shutil.Error as err:
                    pass  # Duplicate file found, ignore
                except FileNotFoundError as fileNotFound:
                    pass


def fileFoundGen():
    '''Creates file signature section within report including file types searched, file
    types found'''

    # TODO: Add list of applications installed on device?  Ugly output, extract required information?
    print(dt(), "Generating Files Acquired Report Section",)
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("reports")

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("reports"):
            raise
    files = open("reports/filesFound.txt", "w+", 1)
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=files)
    print("                  File Signature Searching\n", file=files)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=files)

    totalFiles = 0
    for key, value in fileFound.items():
        for found in value:
            totalFiles += 1

    print("\n"+dt(), "{} Matched File Types have been found, see /reports/filesFound.txt for details".format(totalFiles), file=report)

    for key, value in fileFound.items():
        print("{} ".format(len(value))+key+" files have been found", file=files)
        for file, path in value.items():
            print("\t\t %s : %s" % (file, path), file=files)

    files.close()


def main():
    fileSigAnalysis("rawdump")
    fileFoundGen()
    evidenceGathering()

if __name__ == '__main__':
    main()
