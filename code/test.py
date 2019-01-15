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


def callQuery():
    '''Extract calendar entries from calendar database'''
    contactDB = ("evidence/Databases/ContactCall/Contacts2.db")
    callDB = ("evidence/Databases/ContactCall/calls.db")
    calls = open("reports/call.txt", "w+", 1)

    print(dt(), "Querying Call Databases")
    if os.path.isfile(callDB):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        print("                  Call Log Data\n", file=calls)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        connect = sqlite3.connect(callDB)
        print("\n"+dt(), "Connection made to Call Database", file=report)

        # Calendar Account Information
        cur = connect.cursor()
        cur.execute("select number, date, name, duration  from calls")
        callLog = cur.fetchall()
        print(dt(), "Call Log Information extracted, see /report/calls.txt for detailed information", file=report)
        for row in callLog:
            print("Contact Name:", row[2], file=calls)
            print("Caller Number", row[0], file=calls)
            print("Call Duration:", row[3], "Seconds", file=calls)
            print("Call Date:", dateConversion(row[1]), "\n", file=calls)

    elif os.path.isfile(contactDB):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        print("                  Call Log Data\n", file=calls)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        connect = sqlite3.connect(contactDB)
        print("\n"+dt(), "Connection made to Call Database", file=report)

        # Calendar Account Information
        cur = connect.cursor()
        cur.execute("SELECT number, date,duration,name  FROM calls;")
        callLog = cur.fetchall()
        print(dt(), "Call Log Information extracted, see /report/calls.txt for detailed information", file=report)
        for row in callLog:
            print("Caller Name:", row[3], file=calls)
            print("Caller Number:", row[0], file=calls)
            print("Call Duration", row[2], file=calls)
            print("Call Date:", dateConversion(row[1]), "\n", file=calls)
    else:
        print("[ERROR] Call Log Database not found", file=report)
        print("[ERROR] Call Log Database not found")
    calls.close()



def main():
    callQuery()

if __name__ == '__main__':
    main()
