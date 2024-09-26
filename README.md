## **Description**

This Python script synchronizes two directories by ensuring that the destination directory mirrors the source directory. It performs the following actions:

- **Copies new files and directories** from the source to the destination.
- **Updates modified files** in the destination if they have changed in the source.
- **Deletes files and directories** from the destination that no longer exist in the source.
- **Recursively synchronizes** subdirectories.
- **Logs all activities** to a log file named `sync.log`, including any errors encountered during the synchronization process.

The script reads the paths of the source and destination directories from an external file named `directories.txt`, allowing you to change the directories without modifying the script itself.

---

## **Instructions**

### **Prerequisites**

- **Python Version**: Ensure you have Python 3.5 or higher installed on your system.
- **Permissions**: You must have read permissions for the source directory and write permissions for the destination directory.
- **Logging**: The script will create or append to a log file named `sync.log` in the same directory as the script.

### **Setup**

1. **Create the `directories.txt` File**

   - In the same directory as the script, create a text file named `directories.txt`.
   - On the **first line**, write the full path to the **source directory**.
   - On the **second line**, write the full path to the **destination directory**.
   - **Example `directories.txt` content:**

     ```
     /path/to/source_directory
     /path/to/destination_directory
     ```

   - Replace `/path/to/source_directory` and `/path/to/destination_directory` with the actual directory paths.

2. **Review the Script (Optional)**

   - Ensure the script is named appropriately (e.g., `sync_script.py`).
   - Verify that the script has execute permissions if required.

### **Running the Script**

1. **Open a Terminal or Command Prompt**

   - Navigate to the directory containing the script and the `directories.txt` file.

2. **Execute the Script**

   - Run the script using Python:

     ```bash
     python sync_script.py
     ```

     - Replace `sync_script.py` with the actual name of your script file.

3. **Monitor the Output**

   - The script will display a message upon completion, indicating the time taken for synchronization.

     ```
     Synchronization completed in 0:00:05. Check 'sync.log' for details.
     ```

4. **Check the Log File**

   - Open the `sync.log` file to review detailed logs of the synchronization process.
   - The log file includes timestamps, log levels (INFO or ERROR), and messages about files and directories that were copied, updated, or deleted.

---

## **Example Usage**

Suppose you want to synchronize the following directories:

- **Source Directory**: `/home/user/documents/source`
- **Destination Directory**: `/home/user/documents/backup`

Your `directories.txt` file should contain:

```
/home/user/documents/source
/home/user/documents/backup
```

After running the script, the destination directory `/home/user/documents/backup` will mirror the source directory `/home/user/documents/source`.

---

## **Notes**

- **Backup Important Data**: Before running the script on critical data, it's advisable to back up your destination directory to prevent accidental data loss.
- **Testing**: Consider testing the script with sample directories to ensure it behaves as expected.
- **Error Handling**: Any errors encountered during synchronization are logged in `sync.log`.
- **Script Customization**: You can modify the script to adjust logging levels, add exclusion patterns, or handle multiple directory pairs if needed.

---

## **Summary**

This script provides a straightforward way to keep two directories in sync, making it useful for backups and mirroring data. By reading the directory paths from an external file and logging all activities, it offers flexibility and transparency in its operations.

