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


def dateConversation(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''

    date = str(timestamp)
    nDate = date[:-3]
    conv = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(nDate)))
    return(conv)
def whatsAppQuery():
    '''Extract SMS messages from SMS Database'''
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("reports/WhatsApp")

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("reports/WhatsApp"):
            raise
    print(dt(), "Querying WhatsApp Databases")
    message = open("reports/WhatsApp/messages.txt", "w+", 1)

    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=message)
    print("                  WhatsApp Message Data\n", file=message)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=message)
    db = ("evidence/Databases/WhatsApp/msgstore.db")

    if os.path.isfile(db):
        connect = sqlite3.connect(db)
        print("\n"+dt(), "Connection made to WhatsApp Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT key_remote_jid, key_from_me,data,timestamp  from messages where data IS NOT NULL")
        messages = cur.fetchall()
        print(dt(), "Extracting WhatsApp Messages, See /reports/WhatsApp/messages.txt for more info", file=report)
        for row in messages:
            if row[1] == 1:
                sent = row[0]
                num = sent[0:12]
                print("Message sent to", num, file=message)
            else:
                sent = row[0]
                num = sent[0:12]
                print("Message received from", num, file=message)
            print("Message:", row[2], file=message)
            print("Date/Time:", dateConversation(row[3]), "\n", file=message)

        message.close()
        files = open("reports/WhatsApp/WhatsAppdownloads.txt", "w+", 1)
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=files)
        print("                  WhatsApp Media Transfer Data\n", file=files)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=files)
        cur.execute("SELECT key_remote_jid,key_from_me,media_url,timestamp, media_mime_type  from messages WHERE key_remote_jid != \"status@broadcast\" AND media_url IS NOT NULL")
        media = cur.fetchall()
        print(dt(), "Extracting WhatsApp Media/File Transfer Data, see /report/WhatsApp/downloads.txt for detailed information:", file=report)
        for row in media:
            if row[1] == 1:
                sent = row[0]
                num = sent[0:12]
                print("Media sent to:", num, file=files)
            else:
                sent = row[0]
                num = sent[0:12]
                print("Media received from", row[0], file=files)
            print("Media URL:", row[2], file=files)
            print("Date:", dateConversation(row[3]), file=files)
            print("File Type:", row[4], "\n", file=files)
        files.close()

        calls = open("reports/WhatsApp/calls.txt", "w+", 1)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        print("                  WhatsApp Call Logs\n", file=calls)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)

        cur.execute("select key_remote_jid, key_from_me, messages.timestamp, call_logs.video_call, call_logs.duration from messages JOIN call_logs ON message_row_id == messages._id")
        callLogs = cur.fetchall()
        print(dt(), "Extracting WhatsApp Call Logs, see /report/WhatsApp/callLogs.txt for detailed information:", file=report)
        for row in callLogs:
            contact = row[0]
            if row[1] == 1:
                print("User Called", contact[0:12], file=calls)
            else:
                print("Call Received From", contact[0:12], file=calls)
            if row[3] == 1:
                print("Video Call: Yes", file=calls)
            else:
                print("Video Call: No", file=calls)
            print("Date:", dateConversation(row[2]), file=calls)
            if row[4] != 0:
                print("Duration:", row[4],"Seconds \n", file=calls)
            else:
                print("Call Missed\n", file=calls)
        calls.close()

    else:
        print(dt(), "[ERROR] WhatsApp Database not found", file=report)



def main():
    whatsAppQuery()

if __name__ == '__main__':
    main()
