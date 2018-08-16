# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil

dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
dt = dt+":\t "
report = open("report.txt", "w+", 1)
print(dt+"Script Started", file=report)

# Dictionaries
fileFound = {}
filePath = {}
dupFiles = {}
fileSig = {"PNG": "89 50 4E 47",
                "JPEG": "FF D8 FF E0",
                "AVI": "52 48 46 46",
                "DB": "53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00",
                "MP3": "49 44 33",
                "MOV": "6D 6F 6F 76",
                "TIFF": "49 49 2A",
                "GIF": 	"47 49 46 38"}


def clearFolders():
    '''Deletes androidbackup, rawdump and evidence folders'''
    shutil.rmtree('android_backup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)

    print(dt+"Folders Successfully Cleared", file=report)


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files to RawDump'''
    # Tools
    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  Acquisition Stage\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    # UPGRADE TOOLS TO ABSOLUTE PATH
    adb = './platform-tools/adb'
    abe = './platform-tools/abe.jar'
    unzip = './platform-tools/7za.exe'
    # Create Directory for ADB/Tar to go
    # If Directory Exists Delete .ab and .tar files for fresh extraction
    try:
        os.makedirs("android_backup")
        print(dt+" Android Backup Folder Successfully Created", file=report)
    except OSError:
        if not os.path.isdir("android_backup"):
            raise

    # List Attached Devices
    # os.system("start cmd.exe @cmd cd ./platform-tools & adb devices -l & exit")
    subprocess.call([adb, "devices", "-l"], stdout=report)

    print(dt+" Extracting Backup From Android Device\n", file=report)
    # Create ADB File into directory ./android_backup
    # os.system("start cmd.exe @cmd /k cd ./platform-tools & adb backup -apk -shared -all -f E:/Dropbox/cyber_security/yr4/honours/script/android_backup/backup.ab & exit")
    subprocess.call([adb, "backup", "-apk", "-shared", "-all", "-f", "android_backup/backup.ab"])

    if os.path.isfile("android_backup/backup.ab") and os.path.getsize("android_backup/backup.ab") >= 1:
        print(dt+" Android Backup Successfully Created", file=report)
        # Convert .ab file to .Tar
        print(dt, "Converting Android backup to Tar", file=report)
        # os.system("start cmd.exe @cmd cd E:\Dropbox\cyber_security\yr4\honours\script & java -jar abe.jar unpack ./android_backup/backup.ab ./android_backup/backup.tar")
        # SILENECE OUTPUT OF EXTRACTION
        subprocess.call(["java", "-jar", abe, "unpack", "android_backup/backup.ab", "android_backup/backup.tar"])
        if os.path.isfile("android_backup/backup.tar"):
            print(dt+" Android Backup Successfully Converted to Tar", file=report)
            # Extract Tar File to RawDump
            print(dt+" Extracting Tar File to RawDump", file=report)
            quiet = open(os.devnull, "w")
            subprocess.call([unzip, "x", "android_backup/backup.tar", "-orawdump", "-aou"], stdout=quiet)
            print(dt+" Android Backup Successfully Extracted to Rawdump", file=report)

            totalFiles = 0

            for root, directories, files in os.walk("rawdump"):
                for file in files:
                    totalFiles += 1

            print(dt+"{} Files Have Been Found\n".format(str(totalFiles))+dt+" Acquistion Complete", file=report)
        else:
            print(dt+" ERROR: .Tar File Not Found!", file=report)
    else:
        print(dt+" ERROR: .AB File Not Found", file=report)


def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''

    now = str(datetime.datetime.now())
    now = now.replace(":", "_")

    for root, directories, files in os.walk(folder):   # For all files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Sigs
                path = os.path.join(root, file)
                read = open(path, "rb").read(16)  # Read the first 16 bytes in binary
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                if hexBytes.startswith(value):   # If file sig is found, append to fileFound dict
                    if key in fileFound:
                        fileFound[key].append(file)
                        filePath[key].append(path)
                    else:
                        fileFound[key] = [file]
                        filePath[key] = [path]



def evidenceGathering():
    '''Moves evidence to an evidence folder for each found filetype
    Renames duplicate files to avoid errors'''

    count = 1
    for key, value in filePath.items():
        for item in value:
            evidence = "evidence/"+key
            try:  # Make directory if doesnt exist, error raised if it does exist
                os.makedirs(evidence)
            except OSError:
                if not os.path.isdir(evidence):
                    raise
            try:  # Moves file to evidence folder
                shutil.move(item, evidence)
            except shutil.Error as err:  # if duplicate name, file is renamed an then moved
                homePath = os.path.abspath(os.path.join(__file__, "../../"))  # Gets home directory of application
                absPath = homePath+"\\"+item
                fileExtension = os.path.splitext(absPath)[1]
                fileName = os.path.splitext(absPath)[0]
                newName = fileName + " " + str(count) + " " + fileExtension  # Stores new filename and path, required as os.rename does not hold data and returns nonetype
                if key in fileRename:
                    fileRename[key].append(newName)
                else:
                    fileRename[key] = [newName]
                    os.rename(absPath, fileName + " " + str(count) + " " + fileExtension)  # Rename file to file + date/time
                    # shutil.move(newName, evidence)
                    count += 1


def reportGen():
    '''Blaa Blaa'''

    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  File Signature Analysis\n", file=report)
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

    dupFiles = 0
    dupTypes = 0

    for key, value in fileRename.items():
        for files in value:
            dupFiles += 1

    print("\n{} Duplicate Files Have Been Found:".format(dupFiles), file=report)

    for key, value in fileRename.items():
        print("\t\t{} ".format(len(value))+key+" file(s) have been renamed", file=report)
        for files in value:
            print("\t\t\t\t x has been renamed to "+files, file=report)

def main():
    clearFolders()
    adbExtract()
    fileSigAnalysis("rawdump")
    evidenceGathering()
    reportGen()

if __name__ == '__main__':
    main()
