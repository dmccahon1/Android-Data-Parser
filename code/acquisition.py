# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import tkinter


def adbExtract(alert):
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
    subprocess.call([adb, "backup", "-apk", "-shared", "-all", "-f", "android_backup/backup.ab"])

    if os.path.isfile("android_backup/backup.ab") and os.path.getsize("android_backup/backup.ab") >= 1:
        print(dt, ": Android Backup Successfully Created")
        # Convert .ab file to .Tar
        print(dt, ": Converting Android backup to Tar")
        # os.system("start cmd.exe @cmd cd E:\Dropbox\cyber_security\yr4\honours\script & java -jar abe.jar unpack ./android_backup/backup.ab ./android_backup/backup.tar")
        subprocess.call(["java", "-jar", abe, "unpack", "android_backup/backup.ab", "android_backup/backup.tar"])
        if os.path.isfile("android_backup/backup.tar"):
            print(dt, ": .ab Successfully Converted to .tar")
            # Extract Tar File to RawDump

            subprocess.call([unzip, "x", "android_backup/backup.tar", "-orawdump", "-aou"])
        else:
            alert.config(text="Error: .Tar File Not Found!")
            # print("Error: .Tar File Not Found!")
    else:
        print("Error: .AB File Not Found!")
        alert.tkinter.config(text="Error: .AB File Not Found!")


def main():
    # adbExtract()
    adbExtract()


if __name__ == '__main__':
    main()
