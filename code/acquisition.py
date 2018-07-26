# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files'''
    # Tools
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
        # subprocess.call(["java", "-jar", abe, "unpack", "android_backup/backup.ab", "android_backup/backup.tar"])
        if os.path.isfile("android_backup/backup.tar"):
            print(dt, ": .ab Successfully Converted to .tar")
            # Extract Tar File to RawDump

            subprocess.call([unzip, "x", "android_backup/backup.tar", "-orawdump", "-aou"])
        else:
            print("Error: .Tar File Not Found!")
    else:
        print("Error: .AB File Not Found!")


def fileSearch():

    fileSig = {"PNG": "89 50 4E 47",
                "JPEG": "FF D8 FF E0",
                "AVI": "52 48 46 46",
                "DB": "53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00",
                "MP3": "49 44 33",
                "MOV": "6D 6F 6F 76",
                "TIFF": "49 49 2A",
                "GIF": 	"	47 49 46 3847 49 46 38"}

    fileFound = {}
    filePath = {}

    for root, directories, files in os.walk('./test'):   # For all files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Sigs
                path = os.path.join(root, file)   # Get the path for each file
                read = open(path, "rb").read(16)  # Read the first 16 bytes in binary
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                if hexBytes.startswith(value):   # If file sig is found, append to fileFound dict
                    if key in fileFound:
                        fileFound[key].append(file)
                        filePath[key].append(path)  # Append filetype and filepath to filePath
                    else:
                        fileFound[key] = [file]
                        filePath[key] = [path]

    for key, value in filePath.items():    # For each file found, create a directory for the file type
        for item in value:
            evidence = "evidence/"+key
            path = "".join(value)  # List converted to string in order to be moved
            print(path)
            try:
                os.makedirs(evidence)  # For each filetype found, create an evidence directory
            except OSError:
                if not os.path.isdir(evidence):
                    raise
            shutil.move(item, evidence)  # Move source file to evidence folder


def clearFolders():
    '''Deletes androidbackup, rawdump and evidence folders'''
    shutil.rmtree('android_backup', ignore_errors=True)
    shutil.rmtree('rawdump', ignore_errors=True)
    shutil.rmtree('evidence', ignore_errors=True)


def main():
    clearFolders()
    adbExtract()
    fileSearch()


if __name__ == '__main__':
    main()
