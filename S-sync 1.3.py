import os
import shutil
import filecmp
import logging
from datetime import datetime

def sync_directories(source_dir, dest_dir):
    # Ensure source and destination directories exist
    if not os.path.exists(source_dir):
        logger.error(f"Source directory '{source_dir}' does not exist.")
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logger.info(f"Created destination directory '{dest_dir}'.")

    # Compare the directories
    comparison = filecmp.dircmp(source_dir, dest_dir)

    # Files and directories only in the source
    for item in comparison.left_only:
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        try:
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dest_path)
                logger.info(f"Directory created: {dest_path}")
            else:
                shutil.copy2(src_path, dest_path)
                logger.info(f"File copied: {dest_path}")
        except Exception as e:
            logger.error(f"Failed to copy '{src_path}' to '{dest_path}': {e}")

    # Files that are in both directories but differ
    for item in comparison.diff_files:
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        try:
            shutil.copy2(src_path, dest_path)
            logger.info(f"File updated: {dest_path}")
        except Exception as e:
            logger.error(f"Failed to update '{dest_path}': {e}")

    # Recursively synchronize common subdirectories
    for item in comparison.common_dirs:
        sync_directories(os.path.join(source_dir, item), os.path.join(dest_dir, item))

    # Files and directories only in the destination (should be removed)
    for item in comparison.right_only:
        dest_path = os.path.join(dest_dir, item)
        try:
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)
                logger.info(f"Directory removed: {dest_path}")
            else:
                os.remove(dest_path)
                logger.info(f"File removed: {dest_path}")
        except Exception as e:
            logger.error(f"Failed to remove '{dest_path}': {e}")

if __name__ == "__main__":
    # Configure logging with UTF-8 encoding and custom formatter
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create file handler with UTF-8 encoding
    fh = logging.FileHandler('sync.log', encoding='utf-8')
    fh.setLevel(logging.INFO)

    # Create formatter that outputs Windows-style paths
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Optionally, add console handler if you want logs to appear in the console as well
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

    # Read source and destination directories from an external file
    try:
        with open('directories.txt', 'r', encoding='utf-8') as file:
            lines = file.read().splitlines()
            if len(lines) < 2:
                logger.error("The 'directories.txt' file must contain at least two lines: source and destination directories.")
                exit(1)
            source_directory = lines[0]
            destination_directory = lines[1]
    except FileNotFoundError:
        logger.error("The 'directories.txt' file was not found.")
        exit(1)
    except Exception as e:
        logger.error(f"An error occurred while reading 'directories.txt': {e}")
        exit(1)

    start_time = datetime.now()
    logger.info("Synchronization started.")
    sync_directories(source_directory, destination_directory)
    end_time = datetime.now()
    elapsed_time = end_time - start_time
    logger.info(f"Synchronization completed in {elapsed_time}.")

    print(f"Synchronization completed in {elapsed_time}. Check 'sync.log' for details.")
