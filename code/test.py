# Script: Acquisition
# Desc: Create Android Backup, Convert to Tar & Extract to Raw Dump
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project

import os
import datetime
import subprocess
import pprint

report = open("report.txt", "w+", 1)
dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

platPath = os.path.abspath(os.path.join(__file__, "../../platform-tools"))
adb = platPath+'/adb'
abe = platPath+'/abe.jar'
unzip = platPath+'/7za.exe'

fileSig = {"PNG": "89504E47",
            "JPEG": "FFD8FFE0",
            "AVI": "52484646",
            "DB": "53514C69746520666F726D6174203300",
            "MP3": "494433",
            "MP4": "0000001866747970",
            "TIFF": "49492A",
            "GIF": 	"47494638"}

fileFound = {}
filePath = {}

def dt():
    '''Generates date and time to be used in reports
    Saves having to repeatly write out datetime for each line.'''
    dt = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
    dt = dt+":\t "
    return(dt)





def fileSigAnalysis(folder):
    '''Searches for files within rawdump and matches to stored file filesignature '''

    # TODO: JPEG finds CNT files
    for root, directories, files in os.walk(folder):   # For folders/files in rawdump
        for file in files:
            for key, value in fileSig.items():   # Iterate over File types & Signatures
                for sig in value:
                    path = os.path.join(root, file)
                    sigLen = int(len(value)/2)  # Divide length of signature by 2 to read in bytes, i.e length 16 = 8bytes
                    read = open(path, "rb").read(sigLen)  # Read for length of signature
                    hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])  # Convert binary to hex
                    stripBytes = hexBytes.replace(" ", "")  # Strip all spaces, required due to having to strip spaces in dict to calcuate bytes
                    if stripBytes.startswith(sig):   # If file sig is found, append to fileFound dict
                        if key in fileFound:
                            fileFound[key].append(file)  # Append key: file to fileFound dictionary
                            filePath[key].append(path)   # Append key: path to filePath
                        else:
                            fileFound[key] = [file]
                            filePath[key] = [path]
    pprint.pprint(filePath)



def main():
    fileSigAnalysis("rawdump")


if __name__ == '__main__':
    main()
