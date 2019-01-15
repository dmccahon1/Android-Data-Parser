# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil
import sqlite3
import glob
import json
import time
import re
# Main Report / Summary Report
report = open("report.txt", "w+", 1)

# Platform Tools
homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'
abe = homePath+'/abe.jar'
unzip = homePath+'/7za.exe'
fileFound = {}


def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+": "
    return(dt)


print(dt()+"Script Started", file=report)


def clearFolders():
    '''Deletes androidbackup, rawdump and evidence folders'''
    print(dt(), "Deleting folders")
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)
    shutil.rmtree('reports', ignore_errors=True)

    print(dt(), "Folders Successfully Cleared", file=report)


def deviceInfo():
    '''Gets information about connected device
    Backup Size, Device Type, Android Version'''
    print(dt(), "Gathering Device Information")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  Device Information\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    serialNo = subprocess.check_output([adb, "shell", "getprop", "ro.serialno"]).decode()
    print("Serial Number: "+serialNo, file=report)
    devProduct = subprocess.check_output([adb, "shell", "getprop", "ro.product.device"]).decode()
    print("Product: "+devProduct, file=report)
    devModel = subprocess.check_output([adb, "shell", "getprop", "ro.product.model"]).decode()
    print("Model: "+devModel, file=report)
    androidVersion = subprocess.check_output([adb, "shell", "getprop", "ro.build.version.release"]).decode()
    print("Android Version: "+androidVersion, file=report)


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files to RawDump'''

    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("              Shared Storage Acquisition\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)

    print(dt(), "Pulling Shared Storage From Device", file=report)
    quiet = open(os.devnull, "w")
    print(dt(), "Extracting Data From Shared Storage")
    subprocess.call([adb, "pull", "sdcard/", "rawdump"], stdout=quiet)
    print(dt(), "Shared Storage Extraction Complete", file=report)
    totalFiles = 0
    for root, directories, files in os.walk("rawdump"):
        for file in files:
            totalFiles += 1

    print(dt()+" %d Files Have Been Found\n" % (totalFiles), file=report)


def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''

    fileSig = {"PNG": "89504E47",
                "JPEG": "FFD8FFE0",
                "JPG": "FFD8FFE1",
                "DB": "53514C69746520666F726D6174203300",
                "MP3": "494433",
                "MP4": "0000001866747970",
                "TIFF": "49492A",
                "GIF": 	"47494638",
                "Sound Recordings": "FFF94C80",
                "PDF": "25504446"}

    print(dt(), "Analysing File Signatures")
    for root, directories, files in os.walk(folder):   # For folders/files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Signatures
                path = os.path.join(root, file)
                sigLen = int(len(value)/2)  # Divide length of signature by 2 to read in bytes, i.e length 16 = 8bytes
                read = open(path, "rb").read(sigLen)  # Read for length of signature
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                stripBytes = hexBytes.replace(" ", "")  # Strip all spaces, required due to having to strip spaces in dict to calcuate bytes
                if stripBytes.startswith(value):   # If `````````file````````` sig is found, append to fileFound dict
                    if key not in fileFound:
                        fileFound[key] = {}
                    fileFound[key][file] = path


def evidenceGathering():
    '''Moves evidence to an evidence folder for each found filetype'''
    print(dt(), "Gathering Evidence")
    for key, value in fileFound.items():
        for item in value:
            evidence = "evidence/"+key
            for file, path in value.items():
                try:  # Make directory if doesnt exist, error raised if it does exist
                    os.makedirs(evidence)
                except OSError:
                    if not os.path.isdir(evidence):
                        raise
                try:  # Copy file to evidence folder
                    shutil.move(path, evidence)
                except shutil.Error as err:
                    pass


def fileFoundGen():
    '''Creates file signature section within report including file types searched, file
    types found'''

    # TODO: Add list of applications installed on device?  Ugly output, extract required information?
    print(dt(), "Generating Files Acquired Report Section",)
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("reports")

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("reports"):
            raise
    files = open("reports/filesFound.txt", "w+", 1)
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=files)
    print("                  File Signature Searching\n", file=files)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=files)

    totalFiles = 0
    for key, value in fileFound.items():
        for found in value:
            totalFiles += 1

    print("\n"+dt(), "{} Shared Storage Files have successfully been found, see /reports/filesFound.txt for details".format(totalFiles), file=report)

    for key, value in fileFound.items():
        print("{} ".format(len(value))+key+" files have been found", file=files)
        for file, path in value.items():
            print("\t\t %s : %s" % (file, path), file=files)

    files.close()


def databaseExtract():
    '''Extract databases from android device by copying databases to a locally accessible directory
    such as /sdcard.  Files are then ed to evidence directory.  Skype database requires rename
    due to filename containing : causing error on extraction.'''
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("             Application Database Acquisition\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    # Dictionary with path to databases, multiple entries added for support of multiple locations
    # Errors found are thrown within shell and do not distrupt script execution
    target = {"SMS": ["/data/user_de/0/com.android.providers.telephony/databases/mmssms.db",
    "/data/data/com.android.providers.telephony/databases/mmssms.db"],
    "ContactCall": ["/data/data/com.android.providers.contacts/databases/contacts2.db"],
    "Calendar": ["/data/data/com.android.providers.calendar/databases/calendar.db"],
    "WhatsApp": ["data/data/com.whatsapp/databases/msgstore.db"],
    "Chrome": ["/data/data/com.android.chrome/app_chrome/Default/History"],
    "Skype": ["/data/data/com.skype.raider/databases/*live*.db"],
    "Email": ["/data/data/com.android.email/databases/EmailProvider.db"]}

    # TODO: Fix for Samsung Device
    print(dt(), "Moving Databases to SDCARD")
    print(dt(), "Copying Target Databases to SDCARD", file=report)
    for key, value in target.items():
        for path in value:
            bPath = path.encode()  # Convert path to Bytes
            bType = key.encode()  # Convert type to Bytes
            procId = subprocess.Popen([adb, 'shell'], stdin=subprocess.PIPE)  # Open ADB Shell
            procId.communicate(b'su\nmkdir -p /sdcard/Databases/%s\ncp %s /sdcard/Databases/%s/ >> /dev/null \nexit\nexit' % (bType, bPath, bType))  # Make Directories, Copy file to temporary directory
    # rename skype databases to remove special character
    print("\n"+dt(), "Databases have been copied to sdcard/databases", file=report)
    print(dt(), "Removing Special Characters from Skype Database Name", file=report)

    procId = subprocess.Popen([adb, 'shell'], stdin=subprocess.PIPE)  # Open ADB Shell
    procId.communicate(b'su\ncd sdcard/databases/Skype/\nfor file in *; do mv "$file" `echo $file | tr \':\' \'-\'` ; done\nexit\nexit')  # Remove : from filename
    # FIXME: FIJAOIJHAOHOAP
    try:  # Create Directory for app dbs to go
        os.makedirs("evidence")
        print(dt()+"Database Evidence Folder Successfully Created", file=report)
    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("evidence"):
            raise
    print(dt(), "Pulling databases from /sdcard/databases/ to /evidence/databases", file=report)
    print(dt(), "Extracting Databases From Device")
    quiet = open(os.devnull, "w")
    subprocess.call([adb, "pull", "sdcard/Databases", "evidence"], stdout=quiet)  # Pull database files from sdcard

    totalFiles = 0

    for root, directories, files in os.walk("evidence/databases/"):
        for file in files:
            totalFiles += 1

    print(dt(), "%d Databases have been successfully extracted\n" % (totalFiles), file=report)


def dateConversion(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''

    date = str(timestamp)
    nDate = date[:-3]
    conv = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(nDate)))

    return(conv)


def accountQuery():
    '''Extract SMS messages from SMS Database'''
    db = ("evidence/Databases/ContactCall/contacts2.db")
    print(dt(), "Querying Account Databases")
    if os.path.isfile(db):

        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        print("                 Account Information\n", file=report)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        connect = sqlite3.connect(db)
        print(dt(), "Connection made to Account Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT account_name FROM Accounts")
        contact = cur.fetchall()
        print(dt()+"The following accounts have been found:", file=report)
        for row in contact:
            account = row[0]
            print("\t\t"+account, file=report)
    else:
        print("[ERROR] Contact Database Could Not Be Found", file=report)


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
                    "Email:": row[4],
                    "Address:": row[5],
                    "Notes:": row[6]}

            for col,data in data.items():
                if isinstance(data,str):
                    print(col, data.replace("|",""), file=con)
                else:
                    print(col, "None", file=con)
            print("No.Times Contacted:", row[3],file=con)
            print("\n", file=con)
        con.close()

    else:
        print("[ERROR] Contact Database Could Not Be Found", file=report)


def calendarQuery():
    '''Extract calendar entries from calendar database'''
    db = ("evidence/Databases/Calendar/calendar.db")
    calendar = open("reports/calendar.txt", "w+", 1)
    print(dt(), "Querying Calendar Databases")
    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calendar)
        print("                  Calendar Data\n", file=calendar)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calendar)
        connect = sqlite3.connect(db)
        print("\n"+dt(), "Connection made to Calendar Database", file=report)

        # Calendar Account Information
        cur = connect.cursor()
        cur.execute("SELECT account_name FROM Calendars;")
        accounts = cur.fetchall()
        print(dt(), "Calendar Account & Event Information extracted, see /report/calendar.txt for detailed information", file=report)
        print(dt(), "Calendar Contains the Following Accounts:", file=calendar)
        for row in accounts:
            print("\t\t", row[0], file=calendar)

        # Event Information
        cur.execute("SELECT title,allDay,dtstart,dtend,eventLocation FROM Events;")
        events = cur.fetchall()
        print("\n"+dt(), "Calendar Contains the Following Events:", file=calendar)
        for row in events:
            startDateTime = str(row[2])
            cutDate = startDateTime[:-3]
            startDate = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(cutDate)))

            endDateTime = str(row[3])
            cutSDate = endDateTime[:-3]
            endDate = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(cutSDate)))

            if (row[1] == 1):
                print("\t\t", row[0],"All Day Event", "@", row[4], file=calendar)
            else:
                print("\t\t", row[0], startDate, "-", endDate, " @ ", row[4], file=calendar)
    else:
        print("[ERROR] Calendar Database not found", file=report)
        print("[ERROR] Calendar Database not found")
    calendar.close()


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


def emailQuery():
    '''Extract Emails messages from Email Database'''
    email = open("reports/emails.txt", "w+", 1)
    db = ("evidence/Databases/Email/EmailProvider.db")
    print(dt(), "Querying Email Databases")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=email)
    print("                  Email\n", file=email)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=email)
    if os.path.isfile(db):
        connect = sqlite3.connect(db)
        print("\n"+dt(), "Connection made to Email Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT Message.displayName, timeStamp,subject, fromList, toList, ccList, bccList, snippet, Account.displayName FROM Message JOIN Account ON account._id == Message.accountKey")
        sms = cur.fetchall()
        print(dt(), "Extracting Email Data, see /reports/emails.txt for detailed information", file=report)
        for row in sms:
            if row[8] in row[4]:
                print("Email received from", row[3], file=email)
            else:
                print("Email sent to", row[4], file=email)
            print("Date:", dateConversion(row[1]), file=email)
            print("Subject:", row[2], file=email)
            print("Snippet:", row[7], "\n", file=email)
    else:
        print(dt(), "[ERROR] Email Database not found")
    email.close()


def chromeDateTimeConv(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    format = epoch_start + delta
    return format.strftime("%d/%m/%y %H:%M:%S")


def chromeQuery():
    '''Extract downloads, keyword search terms and url entries from chrome database'''
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("reports/chrome")

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("reports/chrome"):
            raise
    downloads = open("reports/chrome/downloads.txt", "w+", 1)
    db = ("evidence/Databases/chrome/History")
    print(dt(), "Querying Google Chrome Databases")
    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=downloads)
        print("                  Chrome Download Data\n", file=downloads)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=downloads)
        connect = sqlite3.connect(db)
        print("\n"+dt(), "Connection made to Chrome Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT target_path, start_time, mime_type,tab_url,total_bytes FROM downloads;")
        download = cur.fetchall()

        print(dt(), "Extracting Chrome download metadata, see /reports/chrome/downloads.txt for detailed information", file=report)
        for row in download:
            print("File Type:", row[2], file=downloads)
            print("Download Path:", row[0], file=downloads)
            print("Downloaded From:", row[3], file=downloads)
            print("Time:", chromeDateTimeConv(row[1]), file=downloads)
            print("Total Bytes:", row[4], "\n", file=downloads)
        downloads.close()
        searchterms = open("reports/chrome/searchterms.txt", "w+", 1)
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=searchterms)
        print("                  Chrome Search Terms Data\n", file=searchterms)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=searchterms)
        cur.execute("SELECT DISTINCT term from keyword_search_terms;")
        keyword = cur.fetchall()

        print(dt(), "Extracting Chrome Search Terms, see /reports/chrome/searchterms.txt for detailed information:", file=report)
        for row in keyword:
            print(row[0], file=searchterms)
        searchterms.close()
        URLS = open("reports/chrome/visitedurls.txt", "w+", 1)
        print(dt(), "Extracting Chrome Visited URLS, see /reports/chrome/visitedurls.txt for detailed information:", file=report)

        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=URLS)
        print("                  Chrome Visited URLs\n", file=URLS)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=URLS)
        cur.execute("SELECT DISTINCT url,title, visit_count,last_visit_time  from urls;")
        urls = cur.fetchall()

        for row in urls:
            print("Title:", row[1], file=URLS)
            print("URL:", row[0], file=URLS)
            print("Visit Count: ", row[2], file=URLS)
            print("Time:", chromeDateTimeConv(row[3]), "\n", file=URLS)
        URLS.close()

    else:
        print(dt(), "[ERROR] Chrome Database not found", file=report)


def smsQuery():
    '''Extract SMS messages from SMS Database'''
    db = ("evidence/Databases/sms/mmssms.db")
    SMS = open("reports/SMS.txt", "w+", 1)

    print(dt(), "Querying SMS Databases")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=SMS)
    print("                  SMS Data\n", file=SMS)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=SMS)
    if os.path.isfile(db):

        connect = sqlite3.connect(db)
        print("\n"+dt(), "Connection made to SMS Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT address, date, type, body FROM sms")
        sms = cur.fetchall()
        print(dt(), "Extracting SMS Messages, See /reports/SMS.txt for detailed information", file=report)
        for row in sms:
            if row[2] == 1:
                print("Message Received from:", row[0], file=SMS)
            else:
                print("Message Sent to:", row[0], file=SMS)
            print("Date:", dateConversion(row[1]), file=SMS)
            print("Message:", row[3], "\n", file=SMS)

    else:
        print(dt(), "[ERROR] SMS Database not found", file=report)
        print(dt(), "[ERROR] SMS Database not found")
    SMS.close()


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
            print("Date/Time:", dateConversion(row[3]), "\n", file=message)

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
            print("Date:", dateConversion(row[3]), file=files)
            print("File Type:", row[4], "\n", file=files)
        files.close()

        calls = open("reports/WhatsApp/calls.txt", "w+", 1)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)
        print("                  WhatsApp Call Logs\n", file=calls)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=calls)

        cur.execute("SELECT key_remote_jid, key_from_me, messages.timestamp, call_logs.video_call, call_logs.duration FROM messages JOIN call_logs ON message_row_id == messages._id")
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
            print("Date:", dateConversion(row[2]), file=calls)
            if row[4] != 0:
                print("Duration:", row[4],"Seconds \n", file=calls)
            else:
                print("Call Missed\n", file=calls)
        calls.close()

    else:
        print(dt(), "[ERROR] WhatsApp Database not found", file=report)


def skypeQuery():
    '''Extract contacts and messages from skype Database'''
    print(dt(), "Querying Skype Databases")
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("reports/Skype")

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("reports/Skype"):
            raise
    contact = open("reports/contacts.txt", "w+", 1)
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
            print(dt(), "Extracting Skype Contacts, see /reports/skype/contacts.txt for detailed information", file=report)
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

                    print("\n", file=contact)
            contact.close()
        else:
            print(dt(), "[ERROR] Skype Database not found", file=report)


def skypeMessageQuery():
    '''Extract contacts and messages from skype Database'''
    mssg = open("reports/skypeMessages.txt", "w+", 1)

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
            print(dt(), "Extracting Skype Messages, see /report/skype/messages.txt for detailed information:", file=report)
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
            mssg.close()
        else:
            print(dt(), "[ERROR] Skype Database not found", file=mssg)


def main():
    connCheck = subprocess.check_output([adb, "devices"], universal_newlines=True)
    # Only run script if device is connected & authorised
    if ("device" in connCheck[23:]):
            clearFolders()
            deviceInfo()
            adbExtract()
            fileSigAnalysis("rawdump")
            evidenceGathering()
            fileFoundGen()
            databaseExtract()
            contactQuery()
            smsQuery()
            calendarQuery()
            callQuery()
            emailQuery()
            chromeQuery()
            whatsAppQuery()
            skypeQuery()
            skypeMessageQuery()
            accountQuery()

    elif ("unauthorized" in connCheck):
        print("[ERROR] Device Unauthorized")

    else:
        print("[ERROR] No Device Connected")


if __name__ == '__main__':
    main()
