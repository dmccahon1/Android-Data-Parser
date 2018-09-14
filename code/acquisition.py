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
            "AVI": "52484646",
            "DB": "53514C69746520666F726D6174203300",
            "MP3": "494433",
            "MOV": "6D6F6F76",
            "TIFF": "49492A",
            "GIF": 	"47494638"}


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


def adbExtract():
    '''Create Android Backup File, Convert to Tar, Extract Files to RawDump'''

    print("\n#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    print("                  Acquisition Stage\n", file=report)
    print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*\n", file=report)
    # TODO: Calculate time taken for each part in acquisition i.e 10mins to extract

    try:  # Create Directory for ADB/TAR files to go
        os.makedirs("android_backup")
        print(dt()+" Android Backup Folder Successfully Created", file=report)
    except OSError: # If directory already exists, ignore
        if not os.path.isdir("android_backup"):
            raise

    print(dt()+" Extracting Backup From Android Device\n", file=report)

    subprocess.call([adb, "backup", "-apk", "-shared", "-all", "-f", "android_backup/backup.ab"])  # Generates android backup, outputs to android_backup

    if os.path.isfile("android_backup/backup.ab") and os.path.getsize("android_backup/backup.ab") >= 1:
        print(dt()+" Android Backup Successfully Created", file=report)  # If backup exists continue, otherwise stop
        # Convert .ab file to .Tar
        print(dt(), "Converting Android backup to Tar", file=report)
        subprocess.call(["java", "-jar", abe, "unpack", "android_backup/backup.ab", "android_backup/backup.tar"])  # Converts to tar
        if os.path.isfile("android_backup/backup.tar"):
            print(dt()+" Android Backup Successfully Converted to Tar", file=report)
            # Extract Tar File to RawDump
            print(dt()+" Extracting Tar File to RawDump", file=report)
            quiet = open(os.devnull, "w")  # Unzipping generates unrequired output, silence by diverting to null
            subprocess.call([unzip, "x", "android_backup/backup.tar", "-orawdump", "-aou"], stdout=quiet)
            print(dt()+" Android Backup Successfully Extracted to Rawdump", file=report)

            totalFiles = 0

            for root, directories, files in os.walk("rawdump"):
                for file in files:
                    totalFiles += 1

            print(dt()+" {} Files Have Been Found\n".format(str(totalFiles))+dt()+" Acquisition Complete", file=report)
        else:
            print(dt()+" ERROR: .Tar File Not Found!", file=report)  # ADB not converted to Tar / Not Found
    else:
        print(dt()+" ERROR: .AB File Not Found", file=report)  # Backup not created / Not Found


def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''
    for root, directories, files in os.walk(folder):   # For folders/files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Signatures
                path = os.path.join(root, file)
                sigLen = int(len(value)/2)  # Divide length of signature by 2 to read in bytes, i.e length 16 = 8bytes
                read = open(path, "rb").read(sigLen)  # Read for length of signature
                hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                stripBytes = hexBytes.replace(" ", "")  # Strip all spaces, required due to having to strip spaces in dict to calcuate bytes
                if stripBytes.startswith(value):   # If file sig is found, append to fileFound dict
                    if key in fileFound:
                        fileFound[key].append(file)  # Append key: file to fileFound dictionary
                        filePath[key].append(path)   # Append key: path to filePath
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
                fileExtension = os.path.splitext(item)[1]  # Get the file extension from name, later append back after rename
                fileName = os.path.splitext(item)[0]
                oldName = fileName + fileExtension
                newName = fileName + str(count) + fileExtension  # Stores new filename and path, required as os.rename does not hold data and returns nonetype
                if key not in dupFiles:
                    dupFiles[key] = {}  # Create nested dictionary
                dupFiles[key].update({oldName: newName})     # e.g  {png : {test.png : test1.png}}
                os.rename(absPath, fileName + str(count) + fileExtension)  # Rename file to file + count + extension
                shutil.move(newName, evidence)
                count += 1


def reportGen():
    '''Creates file signature section within report including file types searched, file
    types found and duplicate file information - how many, file old + new name'''

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
    # clearFolders()
    # adbExtract()
    fileSigAnalysis("rawdump")
    evidenceGathering()
    reportGen()


if __name__ == '__main__':
    main()
