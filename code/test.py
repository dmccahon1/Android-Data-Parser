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

report = open("report.txt", "w+", 1)

homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)


def fileFoundGen():
    '''Creates file signature section within report including file types searched, file
    types found and duplicate file information - how many, file old + new name'''

    # TODO: Add list of applications installed on device?  Ugly output, extract required information?

    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  File Signature Searching\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)

    print("{} file types have been searched for: ".format(len(fileSig)), file=report)
    for key, value in fileSig.items():
        print("\t\t"+key, file=report)

    totalFiles = 0

    print("\n{} file types have successfully been found:".format(len(fileFound)), file=report)
    for key, value in fileFound.items():
        print("\t\t"+key, file=report)
        for found in value:
            totalFiles += 1

    print("\n{} Files have successfully been found:".format(totalFiles), file=report)

    for key, value in fileFound.items():
        print("\t\t {} ".format(len(value))+key+" files have been found", file=report)
        for file, path in value.items():
            print("\t\t\t\t {} : {}".format(file, path), file=report)

def main():
    fileFoundGen()


if __name__ == '__main__':
    main()
