import os
import shutil
import filecmp
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

def setup_logger(log_file='sync.log'):
    """Setup and return a logger."""
    logger = logging.getLogger('sync_logger')
    logger.setLevel(logging.INFO)

    # File handler with UTF-8 encoding
    fh = logging.FileHandler(log_file, encoding='utf-8')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # Console handler for optional console logging
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(ch)

    return logger

def copy_file_or_directory(src_path, dest_path, logger):
    """Copy a file or directory from src_path to dest_path."""
    try:
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            logger.info(f"Directory copied: '{dest_path}'")
        else:
            shutil.copy2(src_path, dest_path)
            logger.info(f"File copied: '{dest_path}'")
    except Exception as e:
        logger.error(f"Failed to copy '{src_path}' to '{dest_path}': {e}")

def remove_file_or_directory(dest_path, logger):
    """Remove a file or directory at dest_path."""
    try:
        if os.path.isdir(dest_path):
            shutil.rmtree(dest_path)
            logger.info(f"Directory removed: '{dest_path}'")
        else:
            os.remove(dest_path)
            logger.info(f"File removed: '{dest_path}'")
    except Exception as e:
        logger.error(f"Failed to remove '{dest_path}': {e}")

def sync_directories(source_dir, dest_dir, logger, executor):
    """Synchronize source directory to destination directory using parallel processing."""
    if not os.path.exists(source_dir):
        logger.error(f"Source directory '{source_dir}' does not exist.")
        return
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        logger.info(f"Created destination directory '{dest_dir}'.")

    # Compare source and destination directories
    comparison = filecmp.dircmp(source_dir, dest_dir)

    # Parallel processing for copying new files and directories from source
    futures = []
    for item in comparison.left_only:
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        futures.append(executor.submit(copy_file_or_directory, src_path, dest_path, logger))

    # Parallel processing for updating files that differ
    for item in comparison.diff_files:
        src_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        futures.append(executor.submit(copy_file_or_directory, src_path, dest_path, logger))

    # Recursively synchronize common subdirectories
    for item in comparison.common_dirs:
        sync_directories(os.path.join(source_dir, item), os.path.join(dest_dir, item), logger, executor)

    # Parallel processing for removing files and directories only present in destination
    for item in comparison.right_only:
        dest_path = os.path.join(dest_dir, item)
        futures.append(executor.submit(remove_file_or_directory, dest_path, logger))

    # Wait for all parallel tasks to complete
    for future in futures:
        future.result()

if __name__ == "__main__":
    # Setup logger
    logger = setup_logger()

    # Read source and destination directories from 'directories.txt'
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

    # Start synchronization
    start_time = datetime.now()
    logger.info("Synchronization started.")

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        sync_directories(source_directory, destination_directory, logger, executor)

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    logger.info(f"Synchronization completed in {elapsed_time}.")

    print("Check 'sync.log' for details.")
