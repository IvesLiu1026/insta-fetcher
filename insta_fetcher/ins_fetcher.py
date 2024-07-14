#!/usr/bin/env python

import os
import sys
import argparse
import subprocess
import importlib.util

def ensure_instaloader_installed():
    """Ensure that instaloader is installed, install it if not."""
    if importlib.util.find_spec("instaloader") is None:
        print("Instaloader is not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "instaloader"])

def show_help():
    print("Usage: insta_fetcher -a INSTAGRAM_ACCOUNT")
    print("  -a INSTAGRAM_ACCOUNT  Instagram account name to fetch data from")

def extract_files(file, dest):
    subprocess.run(['tar', '-xzvf', file, '-C', dest], check=True)

def create_date_folders(source_dir):
    for file in os.listdir(source_dir):
        file_path = os.path.join(source_dir, file)
        if os.path.isfile(file_path):
            date_part = None
            basename = os.path.basename(file)
            parts = basename.split('_')
            if len(parts) >= 2:
                date_part = parts[0] + '_' + parts[1]
            if date_part:
                date_dir = os.path.join(source_dir, date_part)
                os.makedirs(date_dir, exist_ok=True)
                os.rename(file_path, os.path.join(date_dir, file))

def process_directories(source_dir, dest_dir):
    for date_dir in os.listdir(source_dir):
        date_dir_path = os.path.join(source_dir, date_dir)
        if os.path.isdir(date_dir_path):
            print(f"Processing directory: {date_dir_path}")
            for root, _, files in os.walk(date_dir_path):
                for file in files:
                    if file.endswith('.tar.gz'):
                        file_path = os.path.join(root, file)
                        print(f"Extracting file: {file_path}")
                        extract_files(file_path, dest_dir)

def main():
    parser = argparse.ArgumentParser(description="Fetch and organize Instagram data using instaloader")
    parser.add_argument('-a', '--account', required=True, help="Instagram account name to fetch data from")
    args = parser.parse_args()

    INSTAGRAM_ACCOUNT = args.account
    SOURCE_DIR = INSTAGRAM_ACCOUNT

    ensure_instaloader_installed()
    import instaloader

    result = subprocess.run(['instaloader', INSTAGRAM_ACCOUNT], capture_output=True)
    if result.returncode != 0:
        print("Instaloader failed with exit code", result.returncode)
        print(result.stderr.decode())
        sys.exit(1)

    create_date_folders(SOURCE_DIR)
    # Uncomment the next line if tar.gz files to process
    # process_directories(SOURCE_DIR, DEST_DIR)

    print("Extraction and organization completed.")

if __name__ == "__main__":
    main()
