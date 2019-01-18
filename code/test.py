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

report = open("report.txt", "w+", 1)

homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'

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


def navigationalQuery():
    '''Extract calendar entries from calendar database'''
    file = open("maps\com.google.android.apps.maps\\files\saved_directions.data.cs",errors="ignore")
    x = file.read()
    print(x)



def main():
    navigationalQuery()

if __name__ == '__main__':
    main()
