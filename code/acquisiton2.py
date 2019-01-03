# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil
# TODO: Fix date & time printing the same to file

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

    print(dt(), "Trying to copy databases to /sdcard/databases", file=report)
    for key, value in target.items():
        for path in value:
            bPath = path.encode()  # Convert path to Bytes
            bType = key.encode()  # Convert type to Bytes
            procId = subprocess.Popen([adb, 'shell'], stdin=subprocess.PIPE)  # Open ADB Shell
            procId.communicate(b'su\nmkdir -p /sdcard/Databases/%s\ncp %s /sdcard/Databases/%s/ >> /dev/null \nexit\nexit' % (bType, bPath, bType))  # Make Directories, Copy file to temporary directory
            print("\t %s database is being copied from %s to /sdcard/databases/%s" % (key, path, key), file=report)
    # rename skype databases to remove special character
    print("\n", dt(), "Databases have been copied to sdcard/databases", file=report)
    print(dt(), "Removing Special Characters from Skype Database Name", file=report)
    procId = subprocess.Popen([adb, 'shell'], stdin=subprocess.PIPE)  # Open ADB Shell
    procId.communicate(b'su\ncd sdcard/databases/Skype/\nfor file in *; do mv "$file" `echo $file | tr \':\' \'-\'` ; done\nexit\nexit')  # Make Directories, Copy file to temporary directory
    try:  # Create Directory for ADB/TAR files to go
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

    print(dt(), "%d Databases have been successfully extracted" % (totalFiles), file=report)


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
            print("\t\t\t {} : {}".format(file, path), file=report)
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
    elif ("unauthorized" in connCheck):
        print("[ERROR] Device Unauthorized")
    else:
        print("[ERROR] No Device Found")


if __name__ == '__main__':
    main()
