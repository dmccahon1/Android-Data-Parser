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


def skypeMessageQuery():
    '''Extract contacts and messages from skype Database'''
    print(dt(),"Extracting Messages from Skype Database")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  Skype Data\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    db = glob.glob("evidence/Databases/Skype/*live*.db")
    for file in db:
        if os.path.isfile(file):
            connect = sqlite3.connect(file)
            cur = connect.cursor()
            cur.execute("SELECT nsp_data from messagesv12")
            messages = cur.fetchall()
            print(dt(), "The following messages have been found:", file=report)
            for row in messages:
                for line in row:
                    msg = json.loads(line)
                    time = datetime.datetime.strptime(msg["_serverMessages"][0]["originalarrivaltime"][:-8], "%Y-%m-%dT%H:%M")
                    if msg["messagetype"] == "RichText":
                        if msg["conversationId"] == msg["creator"]:
                            print("\t\tMessage received from", msg["conversationId"], file=report)
                        else:
                            print("\t\tMessage sent to", msg["conversationId"], file=report)

                        URL = re.compile('<a href=\"(.*?)\">').search(msg["content"])
                        if URL is not None:
                            print("\t\tContent:", URL.group(1), file=report)
                        else:
                            print("\t\tContent:",msg["content"], file=report)
                        print("\t\tTime:", time.strftime("%d/%m/%Y %H:%M"),"\n", file=report)

                    elif msg["messagetype"] == "Event/Call":
                        print("\t\tCall Created between user and", msg["conversationId"], file=report)
                        dur=re.compile('<duration>(.*?)</duration>').search(msg["content"])
                        if dur is not None:
                            print("\t\tCall Ended, Duration:", dur.group(1), file=report)
                        else:
                            print("\t\tCall Started", file=report)
                        print("\t\tTime:", time.strftime("%d/%m/%Y %H:%M"),"\n", file=report)

                    elif msg["messagetype"] == "RichText/UriObject":
                        if msg["conversationId"] == msg["creator"]:
                            print("\t\tFile received from", msg["conversationId"], file=report)
                        else:
                            print("\t\tFile sent to", msg["conversationId"], file=report)

                        fileName=re.compile('<OriginalName v=\"(.*?)\">').search(msg["content"])
                        if fileName is not None:
                            print("\t\tFilename:",fileName.group(1), file=report)
                        else:
                            print("\t\tFile Not Found", file=report)

                        fileType=re.compile('meta type=\"(.*?)\"').search(msg["content"])
                        if fileType is not None:
                            print("\t\tFiletype:",fileType.group(1), file=report)
                        else:
                            print("\t\tFiletype Not Found", file=report)
                        print("\t\tTime:", time.strftime("%d/%m/%Y %H:%M"),"\n", file=report)
        else:
            print(dt(), "[ERROR] Skype Database not found", file=report)

def main():
    skypeMessageQuery()


if __name__ == '__main__':
    main()
