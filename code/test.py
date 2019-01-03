# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import subprocess
import os
import datetime

report = open("report.txt", "w+", 1)

homePath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = homePath+'/adb'

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)


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
    "/data/data/com.android.providers.telephony/databases/mmssms.db"],
    "ContactCall": ["/data/data/com.android.providers.contacts/databases/contacts2.db"],
    "Calendar": ["/data/data/com.android.providers.calendar/databases/calendar.db"],
    "WhatsApp" : ["data/data/com.whatsapp/databases/msgstore.db"],
    "Chrome" : ["/data/data/com.android.chrome/app_chrome/Default/History"],
    "Skype" : ["/data/data/com.skype.raider/databases/*live*.db"]}

    print(dt(),"Trying to copy databases to /sdcard/databases", file=report)
    for key,value in target.items():
        for path in value:
            bPath = path.encode() # Convert path to Bytes
            bType = key.encode() # Convert type to Bytes
            procId = subprocess.Popen([adb,'shell'], stdin = subprocess.PIPE) # Open ADB Shell
            procId.communicate(b'su\nmkdir -p /sdcard/Databases/%s\ncp %s /sdcard/Databases/%s/ \nexit\nexit' % (bType,bPath, bType)) # Make Directories, Copy file to temporary directory
            print("\t %s database is being copied from %s to /sdcard/databases/%s" % (key,path,key), file=report)
    # rename skype databases to remove special character
    print("\n",dt(),"Databases have been copied to sdcard/databases", file=report)
    print(dt(), "Removing Special Characters from Skype Database Name", file=report)
    procId = subprocess.Popen([adb,'shell'], stdin = subprocess.PIPE) # Open ADB Shell
    procId.communicate(b'su\ncd sdcard/databases/Skype/\nfor file in *; do mv "$file" `echo $file | tr \':\' \'-\'` ; done\nexit\nexit') # Make Directories, Copy file to temporary directory
    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("evidence")
        print(dt()+" Database Evidence Folder Successfully Created", file=report)

    except OSError:  # If directory already exists, ignore
        if not os.path.isdir("evidence"):
            raise
    print(dt(),"Pulling databases from /sdcard/databases/ to /evidence/databases", file=report)
    # subprocess.call([adb, "pull", "sdcard/Databases", "evidence", ]) # Pull database files from sdcard
    totalFiles = 0
    for root, directories, files in os.walk("evidence/databases/"):
        for file in files:
            totalFiles += 1

    print(dt(),"%d Databases have been successfully extracted" % (totalFiles), file=report)

def main():
    connCheck = subprocess.check_output([adb,"devices"], universal_newlines=True)
    print(connCheck)
    if ("device" in connCheck[23:]):
        print("authorised")
    elif ("unauthorized" in connCheck):
        print("[ERROR] Device Unauthorized")
    else:
        print("[ERROR] No Device Found")

if __name__ == '__main__':
    main()
