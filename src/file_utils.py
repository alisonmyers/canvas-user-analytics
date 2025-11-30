"""
File/folder and CSV helpers.
"""

import os
import shutil
from pathlib import Path
import pandas as pd
from shutil import copyfile

from .settings import status, COURSE_ID
from .logging_utils import _output_status_table
from .utils import print_success, print_unexpected


def create_folder(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    return f'creating {folder_path}'

def check_for_data(folder_path, file_regex=None):
    if os.path.exists(folder_path):
        if file_regex is None:
            print_success(f'SUCCESS: Folder, {folder_path}, exists.')
            return True
        else:
            import re
            pattern = re.compile(file_regex)
            (_, _, filenames) = next(os.walk(folder_path))
            all_data_files = [i for i in filenames if re.search(pattern, i)]
            if all_data_files:
                printable_files = '\n\t-'.join(all_data_files)
                print_success(f'SUCCESS: At least one file found! {printable_files}')
                return True
            else:
                print_unexpected(f'FAIL: Folder {folder_path} found, but no matching files {file_regex}.')
                return False
    else:
        print_unexpected(f'FAIL: Folder, {folder_path}, not found...')
        return False

def _copy_to_folder(src_folder, dst_folder, file_name, print_details=False):
    Path(dst_folder).mkdir(parents=True, exist_ok=True)
    src_file = f'{src_folder}/{file_name}'
    dst_file = f'{dst_folder}/{file_name}'
    try:
        copyfile(src_file, dst_file)
        if print_details:
            print(f'file copied to: {dst_file}')
    except Exception as e:
        print(f'Error: {e}')
    return

def write_data_directory(dataframes, cid):
    course_path = _make_output_dir(cid)
    for name, dataframe in dataframes.items():
        path = Path(f"{course_path}/{name}.csv")
        dataframe.to_csv(path, index=False)


def write_tableau_directory(COURSE_ID, list_of_dfs):
    tableau_path = _make_output_dir(f"{COURSE_ID}/module_progress-Tableau")
    union = pd.concat(list_of_dfs, axis=0, ignore_index=True)
    module_data_output_path = tableau_path / "module_data.csv"
    union.to_csv(module_data_output_path, index=False)
    src = Path(f"course_entitlements.csv")
    dst = Path(f"data/module_progress-Tableau/course_entitlements.csv")
    print(f"Module Progress: {src}, {dst}")
    shutil.copyfile(src, dst)
    _output_status_table(tableau_path)

def _make_output_dir(name):
    directory_path = Path(f"data/{name}")
    print(f"Creating directory path...{directory_path}")
    if not os.path.exists(directory_path):
        print(f"for the first time...")
        os.makedirs(directory_path)
    return directory_path
