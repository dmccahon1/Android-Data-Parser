# MobileSQLiteAnalysis

Extract SQLite Files from Mobile Devices using Android Debug Bridge Tools with Python.  This Program Generates a Backup of an Android Mobile Device and Extracts SQLite Files for Analysis. 


## Setup Instructions
**Notice**: You will need Python 3 and Java installed for this program.

### 1. Setup Environment Variables
1. Press Windows Key and Search for "Environment Variables", Select "Edit System Environment Variables"
2. Select "Environment Variables" at the Bottom Right of the Window
3. Select Path Variable and Select Edit
4. Select New at the Right of Opened Window
5. Copy the Path of the Platform-Tools Folder Within This Program and Paste into the Blank Box Available, Select OK
6. Open CMD and type "adb devices" to Confirm that Environment is Setup Correctly
7. If You Currently Have Your Python IDLE Open, Restart

### 2. Enable USB Debugging
1. On Your Android Device go to Settings > About
2. Tap the Build Number Seven Times, You Should be Prompted with "Developer Mode Enabled" Message
3. Go back to the Settings Page > Developer Options
4. Scroll Down to USB Debugging and Enable
5. Connect Android Device to Computer, Click OK to Allow USB Debugging. 
