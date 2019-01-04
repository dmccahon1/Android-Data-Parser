# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil
import sqlite3

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
            print("\t %s database is being copied from %s to /sdcard/databases/%s" % (key, path, key), file=report)

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
            print("\t", row[0], file=report)

        # Event Information
        cur.execute("SELECT title,allDay,EventsRawTimes.dtstart2445,EventsRawTimes.dtend2445 FROM Events JOIN EventsRawTimes on Events._id == EventsRawTimes.event_id ORDER BY dtstart2445;")
        events = cur.fetchall()
        print("\n"+dt(), "Calendar Contains the Following Events:", file=report)
        for row in events:
            title = row[0]
            allDay = row[1]
            startTime = row[2]
            endTime = row[3]

            # Date / Time Decoding
            # Start Date/Time
            # TODO: Create function to decode data/time
            sYear = startTime[0]+startTime[1]+startTime[2]+startTime[3]
            sMonth = startTime[4]+startTime[5]
            sDay = startTime[6]+startTime[7]
            sDate = (sDay+"/"+sMonth+"/"+sYear)
            sHour = startTime[9]+startTime[10]
            sMinute = startTime[11]+startTime[12]
            sSecond = startTime[13]+startTime[14]
            sTime = (sHour+":"+sMinute+":"+sSecond)

            # End Date/Time
            eYear = endTime[0]+endTime[1]+endTime[2]+endTime[3]
            eMonth = endTime[4]+endTime[5]
            eDay = endTime[6]+endTime[7]
            eDate = (eDay+"/"+eMonth+"/"+eYear)
            eHour = endTime[9]+endTime[10]
            eMinute = endTime[11]+endTime[12]
            eSecond = endTime[13]+endTime[14]
            eTime = (eHour+":"+eMinute+":"+eSecond)

            if (allDay == 1):
                print("\t\t", title, sDate, "-", eDate, "All Day Event", file=report)
            else:
                print("\t\t", title, sDate, sTime, "-", eDate, eTime, file=report)

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

        print(dt(), "The following files have been downloaded from Chrome:", file=report)
        for row in downloads:
            path = row[0]
            time = row[1]
            type = row[2]
            url = row[3]
            size = row[4]

            timeDecode = chromeDateTimeConv(time)
            print("\t File Type:", type, file=report)
            print("\t Download Path:", path, file=report)
            print("\t Downloaded From:", url, file=report)
            print("\t Time:", timeDecode, file=report)
            print("\t Total Bytes:", size, "\n", file=report)

        cur.execute("SELECT DISTINCT term from keyword_search_terms;")
        keyword = cur.fetchall()

        print(dt(), "The Following search terms have been searched:", file=report)
        for row in keyword:
            term = row[0]
            print("\t", term, file=report)

        cur.execute("SELECT DISTINCT url,title, visit_count,last_visit_time  from urls;")
        urls = cur.fetchall()

        print("\n"+dt(), "The Following URLs have been visited", file=report)
        for row in urls:
            url = row[0]
            title = row[1]
            visit_count = row[2]
            time = row[3]

            timeDecode = chromeDateTimeConv(time)

            print("\t Title:", title, file=report)
            print("\t URL:", url, file=report)
            print("\t Visit Count: ", visit_count, file=report)
            print("\t Time:", timeDecode, "\n", file=report)

    else:
        print(dt(), "[ERROR] Chrome Database not found", file=report)


def smsQuery():
    '''Extract SMS messages from SMS Database'''
    db = ("evidence/Databases/sms/mmssms.db")

    if os.path.isfile(db):
        print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        print("                  SMS Data\n", file=report)
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
        connect = sqlite3.connect(db)
        print(dt(), "Connection made to SMS Database", file=report)
        cur = connect.cursor()
        cur.execute("select address, date, type, body from sms")
        sms = cur.fetchall()

        for row in sms:
            contact = row[0]
            date = row[1]
            type = row[2]
            message = row[3]

            if type == 1:
                print("\tMessage Received from:", contact, file=report)
            else:
                print("\tMessage Sent to:", contact, file=report)
            print("\tDate:", date, file=report)
            print("\tMessage:", message, "\n", file=report)

    else:
        print(dt(), "[ERROR] SMS Database not found", file=report)


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
            print("\tMessage:", message, file=report)
            print("\tDate/Time:", date, "\n", file=report)

        cur.execute("SELECT key_remote_jid,key_from_me,media_url,timestamp  from messages WHERE key_remote_jid != \"status@broadcast\" AND media_url IS NOT NULL")
        media = cur.fetchall()
        print(dt(), "The following media has been sent/received via WhatsApp:", file=report)
        for row in media:
            contact = row[0]
            type = row[1]
            url = row[2]
            date = row[3]

            if type == 1:
                print("\tMedia sent to", contact, file=report)
            else:
                print("\tMedia received from", contact, file=report)
            print("\tMedia URL:", url, file=report)
            print("\tDate/Time:", date, "\n", file=report)

    else:
        print(dt(), "[ERROR] WhatsApp Database not found", file=report)


def main():
    connCheck = subprocess.check_output([adb, "devices"], universal_newlines=True)
    # Only run script if device is connected & authorised
    if ("device" in connCheck[23:]):
            clearFolders()
            deviceInfo()
            adbExtract()
            deviceInfo()
            fileSigAnalysis("rawdump")
            evidenceGathering()
            fileFoundGen()
            databaseExtract()
            calendarQuery()
            chromeQuery()
            smsQuery()
            whatsAppQuery()

    elif ("unauthorized" in connCheck):
        print("[ERROR] Device Unauthorized")
    else:
        print("[ERROR] No Device Connected")


if __name__ == '__main__':
    main()
