# Script: search
# Desc: Search & Extract file types with File Signature Analysis
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project
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
            fileOpen = open(os.path.join(root, file), 'rb')
            sig = fileOpen.readline(13)
            fileOpen.close()
            if b"SQLite format" in sig:
                filePath = pathlib.Path(root).parts
                app = filePath[2]

                print(file)

    print(count)





def main():
    dbSearch()


if __name__ == '__main__':
    main()
