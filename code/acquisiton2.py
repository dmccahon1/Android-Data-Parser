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

report = open("report.txt", "w+", 1)

# Platform Tools
homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'
abe = homePath+'/abe.jar'
unzip = homePath+'/7za.exe'

# Dictionaries
fileFound = {}
filePath = {}
dupFiles = {}
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


def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)


print(dt()+"Script Started", file=report)


def clearFolders():
    '''Deletes androidbackup, rawdump and evidence folders'''
    shutil.rmtree('android_backup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)

    print(dt()+"Folders Successfully Cleared", file=report)


def deviceInfo():
    '''Gets information about connected device
    Backup Size, Device Type, Android Version'''
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  Device Information\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    try:
        serialNo = subprocess.check_output([adb, "shell", "getprop", "ro.serialno"]).decode()
        print("Serial Number: "+serialNo, file=report)
        devProduct = subprocess.check_output([adb, "shell", "getprop", "ro.product.device"]).decode()
        print("Product: "+devProduct, file=report)
        devModel = subprocess.check_output([adb, "shell", "getprop", "ro.product.model"]).decode()
        print("Model: "+devModel, file=report)
        androidVersion = subprocess.check_output([adb, "shell", "getprop", "ro.build.version.release"]).decode()
        print("Android Version: "+androidVersion, file=report)
        platPath = os.path.abspath(os.path.join(__file__, "../../android_backup"))
    except subprocess.CalledProcessError:
        print("[ERROR]: No Device Connected", file=report)


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files to RawDump'''

    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("              Shared Storage Acquisition\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    # TODO: Calculate time taken for each part in acquisition i.e 10mins to extract

    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("rawdump/sdcard")
        print(dt()+" Rawdump Folder Successfully Created", file=report)

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("rawdump/sdcard"):
            raise
    print(dt(), "Extracting Shared Storage", file=report)
    subprocess.call([adb, "pull", "sdcard/", "rawdump/sdcard/", ])
    print(dt(), "Shared Storage Successfully Extracted", file=report)
    # subprocess.call([adb, "pull", "storage/", "rawdump/storage/", ])
    totalFiles = 0
    for root, directories, files in os.walk("rawdump/sdcard"):
        for file in files:
            totalFiles += 1

    print(dt()+" {} Files Have Been Found\n".format(str(totalFiles)), file=report)
    print(dt()+" Shared Storage Acquisition Complete", file=report)


def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''

    # TODO: JPEG finds CNT files
    print("FileSig Started")
    for root, directories, files in os.walk(folder):   # For folders/files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Signatures
                path = os.path.join(root, file)
                sigLen = int(len(value)/2)  # Divide length of signature by 2 to read in bytes, i.e length 16 = 8bytes
                read = open(path, "rb").read(sigLen)  # Read for length of signature
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                stripBytes = hexBytes.replace(" ", "")  # Strip all spaces, required due to having to strip spaces in dict to calcuate bytes
                if stripBytes.startswith(value):   # If file sig is found, append to fileFound dict
                    if key not in fileFound:
                        fileFound[key] = {}
                    fileFound[key][file] = path


def evidenceGathering():
    '''Moves evidence to an evidence folder for each found filetype
    Renames duplicate files to avoid errors'''
    print("Evidence Gathering Started")
    for key, value in fileFound.items():
        for item in value:
            evidence = "evidence/"+key
            for file, path in value.items():
                try:  # Make directory if doesnt exist, error raised if it does exist
                    os.makedirs(evidence)
                except OSError:
                    if not os.path.isdir(evidence):
                        raise
                try:  # Moves file to evidence folder
                    shutil.move(path, evidence)
                except shutil.Error as err:  # if duplicate name, file is renamed an then moved
                    pass


def fileFoundGen():
    '''Creates file signature section within report including file types searched, file
    types found and duplicate file information - how many, file old + new name'''

    # TODO: Add list of applications installed on device?  Ugly output, extract required information?

    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  File Signature Searching\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)

    print("{} file types have been searched for: ".format(len(fileSig)), file=report)
    for key, value in fileSig.items():
        print("\t\t"+key, file=report)

    totalFiles = 0

    print("\n{} file types have successfully been found:".format(len(fileFound)), file=report)
    for key, value in fileFound.items():
        print("\t\t"+key, file=report)
        for found in value:
            totalFiles += 1

    print("\n{} Files have successfully been found:".format(totalFiles), file=report)

    for key, value in fileFound.items():
        print("\t\t {} ".format(len(value))+key+" files have been found", file=report)
        for file, path in value.items():
            print("\t\t\t\t {} : {}".format(file, path), file=report)
    # dupTotal = 0

    # for key, value in dupFiles.items():
    #     for files in value:
    #         dupTotal += 1

    # print("\n{} Duplicate Files Have Been Found:".format(dupTotal), file=report)
    #
    # for key, value in dupFiles.items():
    #     print("\t\t{} ".format(len(value))+key+" file(s) have been renamed", file=report)
    #     for old, new in value.items():
    #         print("\t\t\t\t{} has been renamed to {}".format(old, new), file=report)


def databaseExtract():
    '''Extract databases from android device by copying databases to a locally accessible directory
    such as /sdcard.  Files are then pulled to evidence directory.  Skype database requires rename
    due to filename containing : causing error on extraction.'''
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("             Application Database Acquisition\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    # Dictionary with path to databases, multiple entries added for support of multiple locations
    # Errors found are thrown within shell and do not distrupt script execution
    target = {"SMS": ["/data/user_de/0/com.android.providers.telephony/databases/mmssms.db",
    "/data/data/com.android.providers.telephony/databases/mmssms.db",
    "/data/data/com.android.providers.telephony/databases/mmssms.db"],
    "ContactCall": ["/data/data/com.android.providers.contacts/databases/contacts2.db"],
    "Calendar": ["/data/data/com.android.providers.calendar/databases/calendar.db"],
    "WhatsApp" : ["data/data/com.whatsapp/databases/msgstore.db"],
    "Chrome" : ["/data/data/com.android.chrome/app_chrome/Default/History"],
    "Skype" : ["/data/data/com.skype.raider/databases/*live*.db"]}

    # TODO: Fix for Samsung Device

    print(dt(), "Trying to copy databases to /sdcard/databases", file=report)
    for key, value in target.items():
        for path in value:
            bPath = path.encode()  # Convert path to Bytes
            bType = key.encode()  # Convert type to Bytes
            procId = subprocess.Popen([adb, 'shell'], stdin=subprocess.PIPE)  # Open ADB Shell
            procId.communicate(b'su\nmkdir -p /sdcard/Databases/%s\ncp %s /sdcard/Databases/%s/ >> /dev/null \nexit\nexit' % (bType, bPath, bType))  # Make Directories, Copy file to temporary directory
            print("\t\t %s database is being copied from %s to /sdcard/databases/%s" % (key, path, key), file=report)

    # rename skype databases to remove special character
    print("\n"+dt(), "Databases have been copied to sdcard/databases", file=report)
    print(dt(), "Removing Special Characters from Skype Database Name", file=report)

    procId = subprocess.Popen([adb, 'shell'], stdin=subprocess.PIPE)  # Open ADB Shell
    procId.communicate(b'su\ncd sdcard/databases/Skype/\nfor file in *; do mv "$file" `echo $file | tr \':\' \'-\'` ; done\nexit\nexit')  # Remove : from filename

    try:  # Create Directory for app dbs to go
        os.makedirs("evidence")
        print(dt()+" Database Evidence Folder Successfully Created", file=report)

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("evidence"):
            raise
    print(dt(), "Pulling databases from /sdcard/databases/ to /evidence/databases", file=report)

    subprocess.call([adb, "pull", "sdcard/Databases", "evidence", ])  # Pull database files from sdcard

    totalFiles = 0
    for root, directories, files in os.walk("evidence/databases/"):
        for file in files:
            totalFiles += 1

    print(dt(), "%d Databases have been successfully extracted\n" % (totalFiles), file=report)


def accountQuery():
    '''Extract SMS messages from SMS Database'''
    db = ("evidence/Databases/ContactCall/contacts2.db")

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

    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        print("                 Contact Information\n", file=report)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        connect = sqlite3.connect(db)
        print(dt(), "Connection made to SMS Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT account_id, display_name,number,times_contacted, email_ori, address_ori, note_ori   from hwsearch_contacts WHERE account_id == \"|3|\"")
        contact = cur.fetchall()
        print(dt()+"The following contacts have been found:", file=report)
        for row in contact:
            print("\t\tName:", row[1], file=report)

            if(type(row[2]) == str):
                print("\t\tNumber:",row[2].replace("|",""), file=report)
            else:
                print("\t\tNumber: None", file=report)

            print("\t\tNo. Times Contacted:", row[3], file=report)

            if(type(row[4]) == str):
                print("\t\tEmail:",row[4].replace("|",""), file=report)
            else:
                print("\t\tEmail: None", file=report)

            if(type(row[5]) == str):
                print("\t\tAddress:",row[5].replace("|",""), file=report)
            else:
                print("\t\tAddress: None", file=report)
            print("\t\tNotes:", row[6], file=report)
            print("\n", file=report)

    else:
        print("[ERROR] Contact Database Could Not Be Found", file=report)


def calendarQuery():
    '''Extract calendar entries from calendar database'''
    db = ("evidence/Databases/Calendar/calendar.db")

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
            sDT = datetime.datetime.strptime(row[2], "%Y%m%dT%H%M%S")
            sDT = sDT.strftime("%d-%m-%Y %H:%M")

            eDT = datetime.datetime.strptime(row[3], "%Y%m%dT%H%M%S")
            eDT = eDT.strftime("%d-%m-%Y %H:%M")

            if (row[1] == 1):
                print("\t\t", row[0], sDT, "All Day Event", "@", row[4], file=report)
            else:
                print("\t\t", row[0], sDT, "-", eDT, " @ ", row[4], file=report)

    else:
        print("[ERROR] Calendar Database not found")


def chromeDateTimeConv(timestamp):
    '''Convert chrome timestamp to DD/MM/YYYY, MM:HH:SS'''
    epoch_start = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(microseconds=int(timestamp))
    format = epoch_start + delta
    return format.strftime("%d/%m/%y %H:%M:%S")


def chromeQuery():
    '''Extract downloads, keyword search terms and url entries from chrome database'''
    db = ("evidence/Databases/chrome/History")

    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        print("                  Chrome Data\n", file=report)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        connect = sqlite3.connect(db)
        print("\n", dt(), "Connection made to Chrome Database", file=report)
        cur = connect.cursor()
        cur.execute("SELECT target_path, start_time, mime_type,tab_url,total_bytes FROM downloads;")
        downloads = cur.fetchall()

        print(dt() + "The following files have been downloaded from Chrome:", file=report)
        for row in downloads:
            print("\t\t File Type:", row[2], file=report)
            print("\t\t Download Path:", row[0], file=report)
            print("\t\t Downloaded From:", row[3], file=report)
            print("\t\t Time:", chromeDateTimeConv(row[1]), file=report)
            print("\t\t Total Bytes:", row[4], "\n", file=report)

        cur.execute("SELECT DISTINCT term from keyword_search_terms;")
        keyword = cur.fetchall()

        print(dt(), "The Following search terms have been searched:", file=report)
        for row in keyword:
            print("\t\t", row[0], file=report)

        cur.execute("SELECT DISTINCT url,title, visit_count,last_visit_time  from urls;")
        urls = cur.fetchall()

        print("\n"+dt(), "The Following URLs have been visited", file=report)
        for row in urls:
            print("\t\t Title:", row[1], file=report)
            print("\t\t URL:", row[0], file=report)
            print("\t\t Visit Count: ", row[2], file=report)
            print("\t\t Time:", chromeDateTimeConv(row[3]), "\n", file=report)

    else:
        print(dt(), "[ERROR] Chrome Database not found", file=report)


def smsQuery():
    '''Extract SMS messages from SMS Database'''
    db = ("evidence/Databases/sms/mmssms.db")
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  SMS Data\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    if os.path.isfile(db):

        connect = sqlite3.connect(db)
        print(dt(), "Connection made to SMS Database", file=report)
        cur = connect.cursor()
        cur.execute("select address, date, type, body from sms")
        sms = cur.fetchall()

        for row in sms:
            if row[2] == 1:
                print("\t\tMessage Received from:", row[0], file=report)
            else:
                print("\t\tMessage Sent to:", row[0], file=report)

            date = str(row[1])
            nDate = date[:-3]

            conv = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(nDate)))
            print("\t\tDate:", conv, file=report)
            print("\t\tMessage:", row[3], "\n", file=report)

    else:
        print(dt(), "[ERROR] SMS Database not found", file=report)


def whatsAppQuery():
    '''Extract SMS messages from SMS Database'''
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
                print("\t\tMessage sent to", row[0], file=report)
            else:
                print("\t\tMessage received from", row[0], file=report)
            print("\t\tMessage:", row[2], file=report)
            print("\t\tDate/Time:", row[3], "\n", file=report)

        cur.execute("SELECT key_remote_jid,key_from_me,media_url,timestamp  from messages WHERE key_remote_jid != \"status@broadcast\" AND media_url IS NOT NULL")
        media = cur.fetchall()
        print(dt(), "The following media has been sent/received via WhatsApp:", file=report)
        for row in media:
            if row[1] == 1:
                print("\t\tMedia sent to", row[0], file=report)
            else:
                print("\t\tMedia received from", row[0], file=report)
            print("\t\tMedia URL:", row[2], file=report)
            date = str(row[3])
            nDate = date[:-3]

            conv = time.strftime("%d/%M/%Y %H:%M:%S", time.localtime(int(nDate)))
            print("\t\tDate:", conv, file=report)
            print("\t\tDate/Time:", nDate, "\n", file=report)

    else:
        print(dt(), "[ERROR] WhatsApp Database not found", file=report)


def skypeQuery():
    '''Extract contacts and messages from skype Database'''
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  Skype Data\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    db = glob.glob("evidence/Databases/Skype/*live*.db")
    for file in db:
        if os.path.isfile(file):
            connect = sqlite3.connect(file)
            print(dt(), "Connection made to WhatsApp Database", file=report)
            cur = connect.cursor()
            cur.execute("SELECT nsp_data from localaddressbookcontacts")
            contacts = cur.fetchall()
            print(dt(), "Skype has the Following Contacts:", file=report)
            for row in contacts:
                for line in row:
                    data = json.loads(line)
                    for key, value in data.items():
                        target = ["firstName", "middleName", "lastName", "phones"]
                        if key in target:
                            print("\t\t", key, ":", value, file=report)
                    print("\n", file=report)

            cur.execute("SELECT nsp_data from messagesv12")
            messages = cur.fetchall()
            print(dt(), "The following messages have been found:", file=report)
            for row in messages:
                for line in row:
                    msg = json.loads(line)
                    if msg["conversationId"] == msg["creator"]:
                        print("\t\tMessage received from", msg["conversationId"], file=report)
                    else:
                        print("\t\tMessage sent to", msg["conversationId"], file=report)
                    for key, value in msg.items():
                        target = ["createdTime", "content", "messagetype"]
                        if key in target:
                            print("\t\t"+key, ":", value, file=report)
                    time = datetime.datetime.strptime(msg["_serverMessages"][0]["originalarrivaltime"][:-8], "%Y-%m-%dT%H:%M")
                    print("\t\tTime:", time.strftime("%d/%m/%Y %H:%M"), file=report)

                print("\n", file=report)

        else:
            print(dt(), "[ERROR] Skype Database not found", file=report)


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
            accountQuery()
            calendarQuery()
            chromeQuery()
            whatsAppQuery()
            skypeQuery()

    elif ("unauthorized" in connCheck):
        print("[ERROR] Device Unauthorized")

    else:
        print("[ERROR] No Device Connected")


if __name__ == '__main__':
    main()
