# Script: search
# Desc: Search & Extract file types with File Signature Analysis
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project
# https://www.filesignatures.net/
import datetime
import os
import shutil
import pathlib

report = open("report.txt", "w+", 1)

def dbSearch():
    '''Searches for Database files within rawdump, moves to evidence'''
    dt = datetime.datetime.now()
    evidence = "evidence/database"
    # Directory Setup
    try:
        os.makedirs(evidence)
    except OSError:
        if not os.path.isdir(evidence):
            raise

    count = 0
    for root, directories, files in os.walk('./rawdump'):
        for file in files:
            path = os.path.join(root, file)
            fileOpen = open(path, 'rb')
            sig = fileOpen.readline(13)
            fileOpen.close()
            if b"SQLite format" in sig:
                count += 1
                filePath = pathlib.Path(root).parts
                appFile = evidence + "/" + filePath[2] + "-" + file
                shutil.move(path, appFile)
    print(count, "databases have been found")

    print(dt, ": Databases Successfully Extracted")


def imgSearch():
    '''Searches for Database files within rawdump, moves to evidence'''
    dt = datetime.datetime.now()
    evidence = "evidence/images"
    # Directory Setup
    try:
        os.makedirs(evidence)
    except OSError:
        if not os.path.isdir(evidence):
            raise

    count = 0
    for root, directories, files in os.walk('./rawdump'):
        for file in files:
            path = os.path.join(root,file)
            read = open(path, "rb").read(8)
            hexBytes = " ".join(['{:02X}'.format(byte) for byte in read])
            if "89 50 4E 47" in hexBytes:
                shutil.move(path, evidence)


    print(count,"images have been found!")

def filesRename(folder):
    '''Renames all files to filename+incremental count to avoid duplicate filenamesself.
    This is due to different appliations using the same names, i.e icon, cache etc.
    Attempted to rename as filename+datetime however in smaller tests searchin
    g was to fast to change the name to be unique'''
    now = str(datetime.datetime.now())
    now = now.replace(":", "_")

    count = 1
    for root, directories, files in os.walk(folder):
        for file in files:
            count += 1
            homePath = os.path.abspath(os.path.join(__file__, "../.."))  # Gets home directory of application
            dirPath = homePath+"\\"+root
            absPath = os.path.join(dirPath, file)   # Get the absolute path for each file
            fileExtension = os.path.splitext(file)[1]  # Extract file extention & append to end of file
            os.rename(absPath, absPath+"_"+str(count)+"_"+fileExtension)  # Rename file to file + date/time


def fileRename(file):
    '''Renames all files to filename+incremental count to avoid duplicate filenamesself.
    This is due to different appliations using the same names, i.e icon, cache etc.
    Attempted to rename as filename+datetime however in smaller tests searchin
    g was to fast to change the name to be unique'''
    now = str(datetime.datetime.now())
    now = now.replace(":", "_")

    print(file)

def main():
    dbSearch()
    # imgSearch()


if __name__ == '__main__':
    main()
