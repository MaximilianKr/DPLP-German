#!/usr/bin/env python3
"""
Splits a corpus of .rs3 files into training, development, and test sets.

This script takes a source directory containing .rs3 files and splits them
into 'training', 'dev', and 'test' subdirectories within a specified
destination directory. The split is performed randomly but uses a fixed
seed for reproducibility.
"""

import os
import random
import shutil
import argparse
import sys

def split_corpus(source_dir, dest_dir, split, seed):
    """
    Splits .rs3 files from a source directory into train, dev, and test sets.

    Args:
        source_dir (str): The directory containing the original .rs3 files.
        dest_dir (str): The base directory where 'training', 'dev', and 'test'
                        subdirectories will be created.
        split (list[int]): A list of three integers specifying the number of
                           files for the training, dev, and test sets.
        seed (int): The random seed for shuffling, ensuring reproducibility.
    """
    # --- 1. Define and create directories ---
    train_dir = os.path.join(dest_dir, 'training')
    dev_dir = os.path.join(dest_dir, 'dev')
    test_dir = os.path.join(dest_dir, 'test')

    print(f"Creating directories in '{dest_dir}'...")
    for d in [train_dir, dev_dir, test_dir]:
        os.makedirs(d, exist_ok=True)

    # --- 2. Get all file names ---
    try:
        files = os.listdir(source_dir)
        files = [f for f in files if f.endswith('.rs3')]
        if not files:
            print(f"Error: No .rs3 files found in '{source_dir}'")
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Source directory '{source_dir}' not found.")
        sys.exit(1)

    total_files_requested = sum(split)
    if total_files_requested > len(files):
        print(f"Error: Requested {total_files_requested} files for the split, but only {len(files)} are available in '{source_dir}'.")
        sys.exit(1)

    # --- 3. Shuffle with a fixed seed ---
    print(f"Using random seed: {seed}")
    random.seed(seed)
    random.shuffle(files)

    # --- 4. Define split boundaries ---
    train_end = split[0]
    dev_end = train_end + split[1]

    # --- 5. Get file lists for each set ---
    train_files = files[:train_end]
    dev_files = files[train_end:dev_end]
    test_files = files[dev_end:dev_end + split[2]]


    # --- 6. Function to copy files ---
    def copy_files(file_list, dest_dir):
        # Clear the directory first
        for item in os.listdir(dest_dir):
            os.remove(os.path.join(dest_dir, item))
        # Copy new files
        for f in file_list:
            shutil.copy(os.path.join(source_dir, f), os.path.join(dest_dir, f))

    # --- 7. Execute the copy ---
    copy_files(train_files, train_dir)
    copy_files(dev_files, dev_dir)
    copy_files(test_files, test_dir)

    print(f"Successfully copied {len(train_files)} files to {train_dir}")
    print(f"Successfully copied {len(dev_files)} files to {dev_dir}")
    print(f"Successfully copied {len(test_files)} files to {test_dir}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Split a corpus of .rs3 files into training, dev, and test sets.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('source_dir', type=str,
                        help="Directory containing the original .rs3 files (e.g., 'data/pcc/rs3').")
    parser.add_argument('dest_dir', type=str,
                        help="Base directory where 'training', 'dev', and 'test' folders will be created (e.g., 'data/pcc').")
    parser.add_argument('--split', type=int, nargs=3, required=True,
                        metavar=('TRAIN_COUNT', 'DEV_COUNT', 'TEST_COUNT'),
                        help="Three integers for the train, dev, and test set sizes.\nExample: --split 141 18 17")
    parser.add_argument('--seed', type=int, default=42,
                        help="The random seed for shuffling (default: 42).")

    args = parser.parse_args()

    split_corpus(args.source_dir, args.dest_dir, args.split, args.seed)
