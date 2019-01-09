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


def whatsAppQuery():
    '''Extract SMS messages from SMS Database'''
    print(dt(), "Querying WhatsApp Databases")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  WhatsApp Data\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    db = ("evidence/Databases/WhatsApp/msgstore.db")

    if os.path.isfile(db):
        connect = sqlite3.connect(db)
        print(dt(), "Connection made to WhatsApp Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT key_remote_jid, key_from_me,data,timestamp  from messages where data IS NOT NULL")
        messages = cur.fetchall()
        print("The following messages have been sent/received via WhatsApp", file=report)
        for row in messages:
            if row[1] == 1:
                sent = row[0]
                num = sent[0:12]
                print("\t\tMessage sent to", num, file=report)
            else:
                sent = row[0]
                num = sent[0:12]
                print("\t\tMessage received from", num, file=report)
            print("\t\tMessage:", row[2], file=report)
            print("\t\tDate/Time:", row[3], "\n", file=report)

        cur.execute("SELECT key_remote_jid,key_from_me,media_url,timestamp  from messages WHERE key_remote_jid != \"status@broadcast\" AND media_url IS NOT NULL")
        media = cur.fetchall()
        print(dt(), "The following media has been sent/received via WhatsApp:", file=report)
        for row in media:
            if row[1] == 1:
                sent = row[0]
                num = sent[0:12]
                print("\t\tMedia sent to:" ,num, file=report)
            else:
                sent = row[0]
                num = sent[0:12]
                print("\t\tMedia received from", row[0], file=report)
            print("\t\tMedia URL:", row[2], file=report)
            date = str(row[3])
            nDate = date[:-3]

            conv = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(nDate)))
            print("\t\tDate:", conv, file=report)
            print("\t\tDate/Time:", nDate, "\n", file=report)

    else:
        print(dt(), "[ERROR] WhatsApp Database not found", file=report)


def main():
    whatsAppQuery()


if __name__ == '__main__':
    main()
