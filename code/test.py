import subprocess
import os
working_directory = os.getcwd()

subprocess.call(["7za", "x", "../android_backup/backup.tar", "-o../../rawdump", "-aou"], cwd=working_directory)
