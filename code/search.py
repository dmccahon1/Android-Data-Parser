# Script: search
# Desc: Search & Extract file types with File Signature Analysis
# Author: David McCahon (40214392)
# 2018 - 2019 Honours Project
import datetime
import os
import shutil


def dbSearch():
    '''Searches for Database files within rawdump, moves to evidence'''
    dt = datetime.datetime.now()
    # Directory Setup
    try:
        os.makedirs("evidence/database")
    except OSError:
        if not os.path.isdir("evidence/database"):
            raise

    count = 0
    for root, directories, files in os.walk('./rawdump'):
        for file in files:
            fileOpen = open(os.path.join(root, file), 'rb')
            sig = fileOpen.readline(13)
            prefix = os.path.basename(root)
            fileOpen.close()
            if b"SQLite format" in sig:
                count += 1
    print(count)





def main():
    dbSearch()


if __name__ == '__main__':
    main()
