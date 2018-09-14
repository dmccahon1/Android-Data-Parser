# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import time

report = open("abc123.txt", "w+", 1)
dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

platPath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = platPath+'/adb'
abe = platPath+'/abe.jar'
unzip = platPath+'/7za.exe'

fileSig = {"PNG": "89504E47",
            "JPEG": "FFD8FFE0",
            "AVI": "52484646",
            "DB": "53514C69746520666F726D6174203300",
            "MP3": "494433",
            "MOV": "6D6F6F76",
            "TIFF": "49492A",
            "GIF": 	"47494638"}
fileFound = {}
filePath = {}

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    return(dt)


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files'''

    subprocess.call(["java", "-jar", abe, "unpack", "android_backup/backup.ab", "android_backup/backup.tar"])


def main():
    adbExtract()


if __name__ == '__main__':
    main()
