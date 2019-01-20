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

def chromeDateTimeConv(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    format = epoch_start + delta
    return format.strftime("%d/%m/%y %H:%M:%S")


def skypeQuery():
    '''Extract contacts and messages from skype Database'''
    print(dt(), "Querying Skype Databases")
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("reports/Skype")

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("reports/Skype"):
            raise
    contact = open("reports/Skype/contacts.txt", "w+", 1)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=contact)
    print("                  Skype Contacts\n", file=contact)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=contact)
    db = glob.glob("evidence/Databases/Skype/*live*.db")
    for file in db:
        if os.path.isfile(file):
            connect = sqlite3.connect(file)
            print("\n"+dt(), "Connection made to Skype Database", file=report)
            cur = connect.cursor()
            cur.execute("SELECT nsp_data from localaddressbookcontacts")
            contacts = cur.fetchall()
            conCount = 0
            for row in contacts:
                for line in row:
                    data = json.loads(line)
                    for key, value in data.items():
                        target = ["firstName", "middleName", "lastName"]
                        if key in target:
                            print("", key, ":", value, file=contact)
                        if key == "phones":
                            for item in value:
                                for x, y in item.items():
                                    if x == "number":
                                        print(" Number:", y, file=contact)
                    conCount += 1
                    print("\n", file=contact)
            print(dt(), "%d Skype Contacts Found, see /reports/skype/contacts.txt for detailed information" % (conCount), file=report)
            contact.close()
        else:
            print(dt(), "[ERROR] Skype Database not found", file=report)


def skypeMessageQuery():
    '''Extract contacts and messages from skype Database'''
    mssg = open("reports/Skype/messages.txt", "w+", 1)

    print(dt(), "Extracting Messages from Skype Database")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=mssg)
    print("                  Skype Message Data\n", file=mssg)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=mssg)
    db = glob.glob("evidence/Databases/Skype/*live*.db")
    for file in db:
        if os.path.isfile(file):
            connect = sqlite3.connect(file)
            cur = connect.cursor()
            cur.execute("SELECT nsp_data from messagesv12")
            messages = cur.fetchall()
            mssgCount = 0
            for row in messages:
                for line in row:
                    msg = json.loads(line)
                    time = datetime.datetime.strptime(msg["_serverMessages"][0]["originalarrivaltime"][:-8], "%Y-%m-%dT%H:%M")
                    if msg["messagetype"] == "RichText":
                        if msg["conversationId"] == msg["creator"]:
                            print("Message received from", msg["conversationId"], file=mssg)
                        else:
                            print("Message sent to", msg["conversationId"], file=mssg)

                        URL = re.compile('<a href=\"(.*?)\">').search(msg["content"])
                        if URL is not None:
                            print("Content:", URL.group(1), file=mssg)
                        else:
                            print("Content:", msg["content"], file=mssg)
                        print("Time:", time.strftime("%d/%m/%Y %H:%M"), "\n", file=mssg)

                    elif msg["messagetype"] == "Event/Call":
                        print("Call between user and", msg["conversationId"], file=mssg)
                        dur = re.compile('<duration>(.*?)</duration>').search(msg["content"])
                        if dur is not None:
                            print("Call Ended", file=mssg)
                            print("Duration:", dur.group(1), file=mssg)
                        else:
                            print("Call Started", file=mssg)
                        print("Time:", time.strftime("%d/%m/%Y %H:%M"), "\n", file=mssg)

                    elif msg["messagetype"] == "RichText/UriObject":
                        if msg["conversationId"] == msg["creator"]:
                            print("File received from", msg["conversationId"], file=mssg)
                        else:
                            print("File sent to", msg["conversationId"], file=mssg)

                        fileName = re.compile('<OriginalName v=\"(.*?)\">').search(msg["content"])
                        if fileName is not None:
                            print("Filename:", fileName.group(1), file=mssg)
                        else:
                            print("File Not Found", file=mssg)

                        fileType = re.compile('meta type=\"(.*?)\"').search(msg["content"])
                        if fileType is not None:
                            print("Filetype:", fileType.group(1), file=mssg)
                        else:
                            print("Filetype Not Found", file=report)
                        print("Time:", time.strftime("%d/%m/%Y %H:%M"), "\n", file=mssg)
                    mssgCount += 1
            print(dt(), "%d Skype Messages Found, see /reports/skype/messages.txt for detailed information" % (mssgCount), file=report)
            mssg.close()
        else:
            print(dt(), "[ERROR] Skype Database not found", file=mssg)


def main():
    skypeQuery()
    skypeMessageQuery()

if __name__ == '__main__':
    main()
