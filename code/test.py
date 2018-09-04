# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess

report = open("abc123.txt", "w+", 1)
dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
dt2 = datetime.datetime.now()

platPath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = platPath+'/adb'
abe = platPath+'/abe.jar'
unzip = platPath+'/7za.exe'

fileSig = {"PNG": "89504E47",
            "JPEG": "FFD8FFE0",
            "DB": "53514C69746520666F726D6174203300"}
fileFound = {}
filePath = {}


def deviceInfo(folder):
    '''Gets information about connected device
    Backup Size, Device Type, Android Version'''
    for root, directories, files in os.walk(folder):   # For all files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Sigs
                path = os.path.join(root, file)
                sigLen = int(len(value)/2)
                read = open(path, "rb").read(sigLen)  # Read the first 16 bytes in binary
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                stripBytes = hexBytes.replace(" ", "")
                if stripBytes.startswith(value):   # If file sig is found, append to fileFound dict
                    if key in fileFound:
                        fileFound[key].append(file)
                        filePath[key].append(path)
                    else:
                        fileFound[key] = [file]
                        filePath[key] = [path]
    print(fileFound)
    print(filePath)



def main():
    deviceInfo("test")


if __name__ == '__main__':
    main()
