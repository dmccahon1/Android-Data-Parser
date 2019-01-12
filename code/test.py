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


def chromeDateTimeConv(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    format = epoch_start + delta
    return format.strftime("%d/%m/%y %H:%M:%S")


def contactQuery():
    '''Extract SMS messages from SMS Database'''
    db = ("evidence/Databases/ContactCall/contacts2.db")
    print(dt(), "Querying Contact Databases")

    con = open("reports/contacts.txt", "w+", 1)

    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=con)
        print("                 Contact Information\n", file=con)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=con)
        connect = sqlite3.connect(db)
        print("\n"+dt()+" Connection made to Contact Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT account_id, display_name,number,times_contacted, email_ori, address_ori, note_ori   from hwsearch_contacts WHERE account_id == \"|3|\"")
        contact = cur.fetchall()
        print(dt()+" Extracting Contacts, See /reports/contacts.txt for detailed information:", file=report)
        for row in contact:
            data = {"Name": row[1],
                    "Number:": row[2],
                    "No. Times Contacts:": row[3],
                    "Email:": row[4],
                    "Address:": row[5],
                    "Notes:": row[6]}

            for col,data in data.items():
                if isinstance(data,str):
                    print(col, data.replace("|",""), file=con)
                else:
                    print(col, "None", file=con)
            print("\n", file=con)
        con.close()

    else:
        print("[ERROR] Contact Database Could Not Be Found", file=report)



def main():
    contactQuery()

if __name__ == '__main__':
    main()
