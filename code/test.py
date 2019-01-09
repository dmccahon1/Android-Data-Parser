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

report = open("report.txt", "w+", 1)

homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)


def chromeDateTimeConv(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    format = epoch_start + delta
    return format.strftime("%d/%m/%y %H:%M:%S")



def callQuery():
    '''Extract calendar entries from calendar database'''
    db = ("evidence/Databases/ContactCall/Contacts2.db")
    calls = open("reports/call.txt", "w+", 1)
    print(dt(), "Querying Calendar Databases")
    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        print("                  Calendar Data\n", file=calls)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        connect = sqlite3.connect(db)
        print("\n"+dt(), "Connection made to Calendar Database", file=report)

        # Calendar Account Information
        cur = connect.cursor()
        cur.execute("SELECT number, date,duration,name  FROM calls;")
        callLog = cur.fetchall()
        print(dt(), "Call Log Information extracted, see /report/calls.txt for detailed information", file=report)
        for row in callLog:
            number = row[0]
            date = row[1]
            duration = row[2]
            name = row[3]

            print("Caller Name:", name, file=calls)
            print("Caller Number:", number, file=calls)
            print("Call Duration", duration, file=calls)
            print("Call Date:", date, "\n", file=calls)

    else:
        print("[ERROR] Call Log Database not found", file=report)
        print("[ERROR] Call Log Database not found")
    calls.close()

def main():
    callQuery()


if __name__ == '__main__':
    main()
