# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import shutil

report = open("report.txt", "w+")
dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M")


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
                fileExtension = os.path.splitext(item)[1]
                fileName = os.path.splitext(item)[0]
                oldName = fileName + fileExtension
                newName = fileName + str(count) + fileExtension  # Stores new filename and path, required as os.rename does not hold data and returns nonetype
                if key not in dupFiles:
                    dupFiles[key] = {}
                dupFiles[key].update({oldName: newName})
                os.rename(absPath, fileName + str(count) + fileExtension)  # Rename file to file + date/time
                shutil.move(newName, evidence)
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
    dupTotal = 0

    for key, value in dupFiles.items():
        for files in value:
            dupTotal += 1

    print("\n{} Duplicate Files Have Been Found:".format(dupTotal), file=report)

    for key, value in dupFiles.items():
        print("\t\t{} ".format(len(value))+key+" file(s) have been renamed", file=report)
        for old, new in value.items():
            print("\t\t\t\t{} has been renamed to {}".format(old, new), file=report)


def main():
    fileSigAnalysis("test")
    evidenceGathering()
    reportGen()
    shutil.rmtree('evidence', ignore_errors=True)

if __name__ == '__main__':
    main()
