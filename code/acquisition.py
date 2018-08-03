# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil

def clearFolders():
    '''Deletes androidbackup, rawdump and evidence folders'''
    # shutil.rmtree('android_backup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files to RawDump'''
    # Tools
    # UPGRADE TOOLS TO ABSOLUTE PATH
    adb = './platform-tools/adb'
    abe = './platform-tools/abe.jar'
    unzip = './platform-tools/7za.exe'
    # Date and Time for Logs
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
    # Create Directory for ADB/Tar to go
    # If Directory Exists Delete .ab and .tar files for fresh extraction
    try:
        os.makedirs("android_backup")
    except OSError:
        if not os.path.isdir("android_backup"):
            raise
    # List Attached Devices
    # os.system("start cmd.exe @cmd cd ./platform-tools & adb devices -l & exit")
    subprocess.call([adb, "devices", "-l"])
    print(dt, ": Extracting Android Backup")
    # Create ADB File into directory ./android_backup
    # os.system("start cmd.exe @cmd /k cd ./platform-tools & adb backup -apk -shared -all -f E:/Dropbox/cyber_security/yr4/honours/script/android_backup/backup.ab & exit")
    # subprocess.call([adb, "backup", "-apk", "-shared", "-all", "-f", "android_backup/backup.ab"])

    if os.path.isfile("android_backup/backup.ab") and os.path.getsize("android_backup/backup.ab") >= 1:
        print(dt, ": Android Backup Successfully Created")
        # Convert .ab file to .Tar
        print(dt, ": Converting Android backup to Tar")
        # os.system("start cmd.exe @cmd cd E:\Dropbox\cyber_security\yr4\honours\script & java -jar abe.jar unpack ./android_backup/backup.ab ./android_backup/backup.tar")
        # SILENECE OUTPUT OF EXTRACTION
        # subprocess.call(["java", "-jar", abe, "unpack", "android_backup/backup.ab", "android_backup/backup.tar"])
        if os.path.isfile("android_backup/backup.tar"):
            print(dt, ": .ab Successfully Converted to .tar")
            # Extract Tar File to RawDump

            subprocess.call([unzip, "x", "android_backup/backup.tar", "-orawdump", "-aou"])
        else:
            print("Error: .Tar File Not Found!")
    else:
        print("Error: .AB File Not Found!")


def fileSearch(folder):
    '''Searches for files within rawdump and matches to stored file filesignatures
    Renames files if duplicate named using count '''
    now = str(datetime.datetime.now())
    now = now.replace(":", "_")

    fileSig = {"PNG": "89 50 4E 47",
                "JPEG": "FF D8 FF E0",
                "AVI": "52 48 46 46",
                "DB": "53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00",
                "MP3": "49 44 33",
                "MOV": "6D 6F 6F 76",
                "TIFF": "49 49 2A",
                "GIF": 	"47 49 46 38"}
    fileFound = {}
    filePath = {}
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
                os.rename(absPath, fileName + " " + str(count) + " " + fileExtension)  # Rename file to file + date/time
                shutil.move(newName, evidence)
                count += 1


def main():
    clearFolders()
    adbExtract()
    fileSearch()


if __name__ == '__main__':
    main()
