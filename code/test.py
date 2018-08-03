# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import shutil


def fileSearch(folder):

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
            try:
                os.makedirs(evidence)
            except OSError:
                if not os.path.isdir(evidence):
                    raise
            try:
                shutil.move(item, evidence)
            except shutil.Error as err:
                homePath = os.path.abspath(os.path.join(__file__, "../../"))  # Gets home directory of application
                absPath = homePath+"\\"+item
                fileExtension = os.path.splitext(absPath)[1]
                fileName = os.path.splitext(absPath)[0]
                newName = fileName + " " + str(count) + " " + fileExtension
                os.rename(absPath, fileName + " " + str(count) + " " + fileExtension)  # Rename file to file + date/time
                shutil.move(newName, evidence)
                count += 1


def main():
    fileSearch("rawdump")
    # filesRename("rawdump")


if __name__ == '__main__':
    main()
