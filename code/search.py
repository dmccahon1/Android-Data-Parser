# Script: search
# Desc: Search & Extract file types with File Signature Analysis
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project
# https://www.filesignatures.net/
import datetime
import os
import shutil
import pathlib


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


def main():
    dbSearch()
    # imgSearch()


if __name__ == '__main__':
    main()
