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


def calendarQuery():
    '''Extract calendar entries from calendar database'''
    db = ("evidence/Databases/Calendar/calendar.db")
    print(dt(), "Querying Calendar Databases")
    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        print("                  Calendar Data\n", file=report)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        connect = sqlite3.connect(db)
        print(dt(), "Connection made to Calendar Database", file=report)

        # Calendar Account Information
        cur = connect.cursor()
        cur.execute("SELECT account_name FROM Calendars;")
        accounts = cur.fetchall()

        print(dt(), "Calendar Contains the Following Accounts:", file=report)
        for row in accounts:
            print("\t\t", row[0], file=report)

        # Event Information
        cur.execute("SELECT title,allDay,EventsRawTimes.dtstart2445,EventsRawTimes.dtend2445,eventLocation FROM Events JOIN EventsRawTimes on Events._id == EventsRawTimes.event_id ORDER BY dtstart2445;")
        events = cur.fetchall()
        print("\n"+dt(), "Calendar Contains the Following Events:", file=report)
        for row in events:
            # Date / Time Decoding
            # Works on P20
            try:
                sDT = datetime.datetime.strptime(row[2], "%Y%m%dT%H%M%S")
                sDT = sDT.strftime("%d-%m-%Y %H:%M")

                eDT = datetime.datetime.strptime(row[3], "%Y%m%dT%H%M%S")
                eDT = eDT.strftime("%d-%m-%Y %H:%M")

            except:
                # Except error, some phones format with Z on end
                sDT = datetime.datetime.strptime(row[2], "%Y%m%dT%H%M%SZ")
                sDT = sDT.strftime("%d-%m-%Y %H:%M")

                eDT = datetime.datetime.strptime(row[3], "%Y%m%dT%H%M%SZ")
                eDT = eDT.strftime("%d-%m-%Y %H:%M")


            if (row[1] == 1):
                print("\t\t", row[0], sDT, "All Day Event", "@", row[4], file=report)
            else:
                print("\t\t", row[0], sDT, "-", eDT, " @ ", row[4], file=report)

    else:
        print("[ERROR] Calendar Database not found")

def main():
    calendarQuery()


if __name__ == '__main__':
    main()
