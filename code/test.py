# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import subprocess
import os
import datetime
import sqlite3

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
    db = ("evidence/Databases/WhatsApp/msgstore.db")

    if os.path.isfile(db):
        connect = sqlite3.connect(db)
        print(dt(), "Connection made to WhatsApp Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT key_remote_jid, key_from_me,data,timestamp  from messages where data IS NOT NULL")
        messages = cur.fetchall()
        print("The following messages have been sent/received via WhatsApp", file=report)
        for row in messages:
            contact = row[0]
            type = row[1]
            message = row[2]
            date = row[3]

            if type == 1:
                print("\tMessage sent to", contact, file=report)
            else:
                print("\tMessage received from", contact, file=report)
            print("\tMessage:",message, file=report)
            print("\tDate/Time:", date,"\n", file=report)

        cur.execute("SELECT key_remote_jid,key_from_me,media_url,timestamp  from messages WHERE key_remote_jid != \"status@broadcast\" AND media_url IS NOT NULL")
        media = cur.fetchall()
        print(dt(),"The following media has been sent/received via WhatsApp:", file=report)
        for row in media:
            contact = row[0]
            type = row[1]
            url = row[2]
            timestamp = row[3]

            if type == 1:
                print("\tMedia sent to", contact, file=report)
            else:
                print("\tMedia received from", contact, file=report)
            print("\tMedia URL:", url, file=report)
            print("\tDate/Time:", date, "\n",file=report)

    else:
        print(dt(),"[ERROR] SMS Database not found",file=report)



def main():
    whatsAppQuery()


if __name__ == '__main__':
    main()
