# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import shutil

def search():

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
                print(path)
                '''read = open(path, "rb").read(16)  # Read the first 16 bytes in binary
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                if hexBytes.startswith(value):   # If file sig is found, append to fileFound dict
                    if key in fileFound:
                        fileFound[key].append(file)
                        filePath[key].append(path)  # Append filetype and filepath to filePath
                    else:
                        fileFound[key] = [file]
                        filePath[key] = [path]

    count = 1
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
            try:
                shutil.move(item, evidence)  # Move source file to evidence folder
            except:
                rename = evidence
                shutil.move(item, evidence)
                count += 1'''



def main():
    search()


if __name__ == '__main__':
    main()
