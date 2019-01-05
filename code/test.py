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

report = open("report.txt", "w+", 1)

homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)


def skypeQuery():
    '''Extract contacts and messages from skype Database'''
    db = glob.glob("evidence/Databases/Skype/*live*.db")
    for file in db:
        if os.path.isfile(file):
            connect = sqlite3.connect(file)
            print(dt(), "Connection made to WhatsApp Database", file=report)
            cur = connect.cursor()
            cur.execute("SELECT nsp_data from localaddressbookcontacts")
            contacts = cur.fetchall()
            print(dt(),"Skype has the Following Contacts:", file=report)
            for row in contacts:
                for line in row:
                    data = json.loads(line)
                    for key, value in data.items():
                        target = ["firstName", "middleName", "lastName", "phones"]
                        if key in target:
                            print("\t",key,":", value,file=report)
                    print("\n",file=report)

            cur.execute("SELECT nsp_data from messagesv12")
            messages = cur.fetchall()
            print(dt(), "The following messages have been found:", file=report)
            for row in messages:
                for line in row:
                    msg = json.loads(line)
                    if msg["conversationId"] == msg["creator"]:
                        print("\tMessage received from", msg["conversationId"],file=report)
                    else:
                        print("\tMessage sent to", msg["conversationId"], file=report)
                    for key,value in msg.items():
                        target=["createdTime","content","messagetype"]
                        if key in target:
                            print("\t"+key,":",value, file=report)
                print("\n",file=report)

        else:
            print(dt(),"[ERROR] Skype Database not found",file=report)



def main():
    skypeQuery()


if __name__ == '__main__':
    main()
