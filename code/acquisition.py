# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import shutil
# TODO: Fix date & time printing the same to file
dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
dt = dt+":\t "
report = open("report.txt", "w+", 1)
print(dt+"Script Started", file=report)

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
            "AVI": "52484646",
            "DB": "53514C69746520666F726D6174203300",
            "MP3": "494433",
            "MOV": "6D6F6F76",
            "TIFF": "49492A",
            "GIF": 	"47494638"}


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

    # Create Directory for ADB/Tar to go
    # If Directory Exists Delete .ab and .tar files for fresh extraction
    try:
        os.makedirs("android_backup")
        print(dt+" Android Backup Folder Successfully Created", file=report)
    except OSError:
        if not os.path.isdir("android_backup"):
            raise

    print(dt+" Extracting Backup From Android Device\n", file=report)
    # Create ADB File into directory ./android_backup
    subprocess.call([adb, "backup", "-apk", "-shared", "-all", "-f", "android_backup/backup.ab"])

    if os.path.isfile("android_backup/backup.ab") and os.path.getsize("android_backup/backup.ab") >= 1:
        print(dt+" Android Backup Successfully Created", file=report)
        # Convert .ab file to .Tar
        print(dt, "Converting Android backup to Tar", file=report)
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

    # TODO: Get device, android version, size of backup, total files


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
        backupSize = os.path.getsize(platPath+"/backup.ab")
        backupSize = (backupSize / 1000000000)
        print("Backup Size: {} GB ".format(round(backupSize, 2)), file=report)
        print(type(backupSize))
    except subprocess.CalledProcessError:
        print("[ERROR]: No Device Connected", file=report)


def main():
    clearFolders()
    adbExtract()
    fileSigAnalysis("rawdump")
    evidenceGathering()
    reportGen()


if __name__ == '__main__':
    main()
