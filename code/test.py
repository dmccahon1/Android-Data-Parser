# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import shutil

report = open("report.txt", "w+")
dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M")

# Dictionaries
fileFound = {}
filePath = {}
fileRename = {}


def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''

report.write("this is via write\n")
print("this is via print", file=report)


def main():
    fileSigAnalysis("test")
    print(fileRename)


if __name__ == '__main__':
    main()
