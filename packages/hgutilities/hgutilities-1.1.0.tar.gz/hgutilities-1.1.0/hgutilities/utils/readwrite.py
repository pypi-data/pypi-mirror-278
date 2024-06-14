import os

import numpy as np

from .paths import make_folder

def save_to_path(path, data, separator=","):
    make_folder(path, force=True)
    with open(path, "w") as file:
        write_header_to_file(file, data, separator)
        write_columns_to_file(file, data, separator)

def write_header_to_file(file, data, separator):
    header_string = separator.join([str(key) for key in data.keys()])
    file.writelines(header_string + "\n")

def write_columns_to_file(file, data, separator):
    rows = zip(*list(data.values()))
    for row in rows:
        file.writelines(separator.join([str(value) for value in row]) + "\n")

def read_from_path(path, separater=",", skip_first_n=0,
                   data_type=float, enforce_type=True):
    with open(path, "r") as file:
        skip_first_lines(file, skip_first_n)
        keys = file.readline().strip("% \n").split(separater)
        values = get_data_from_file(file, separater, data_type, enforce_type)
        return dict(zip(keys, values))

def skip_first_lines(file, skip_first_n):
    for line_number in range(skip_first_n):
        file.readline()

def get_data_from_file(file, separater, data_type, enforce_type):
    rows = [line.strip().split(separater) for line in file]
    columns = [process_column(column, data_type, enforce_type)
               for column in zip(*rows)]
    return columns

def process_column(column, data_type, enforce_type):
    try:
        column = [data_type(value) for value in column]
    except:
        return process_column_error(column, data_type, enforce_type)
    return np.array(column)

def process_column_error(column, data_type, enforce_type):
    if enforce_type:
        enforce_type_error_message(column, data_type)
    else:
        return column

def enforce_type_error_message(column, data_type):
        raise ValueError(f"Could not convert data to {data_type}\n"
                         "Change the data type or see the enforce_type"
                         "kwarg to False\n"
                         f"First five entries: {column[:5]}")


def save_combined_files(folder_path, blacklist=None, name="Combined.txt"):
    results_path = os.path.join(folder_path, name)
    data = combine_files(folder_path, blacklist=blacklist)
    save_to_path(results_path, data)
    return data

def combine_files(folder_path, blacklist=None):
    blacklist = get_blacklist(blacklist)
    paths = get_combined_paths(folder_path, blacklist)
    data = get_data_from_paths(paths)
    return data

def get_blacklist(blacklist):
    if blacklist is None:
        blacklist = []
    return blacklist

def get_data_from_paths(paths):
    contents = [read_from_path(path) for path in paths]
    header = list(contents[0].keys())
    data = {key: np.concatenate([partial_contents[key]
                                 for partial_contents in contents],
                                axis=0)
            for key in header}
    return data

def get_combined_paths(folder_path, blacklist):
    paths = [os.path.join(folder_path, file_name)
             for file_name in os.listdir(folder_path)
             if file_name_not_blacklisted(file_name, blacklist)]
    return paths

def file_name_not_blacklisted(file_name, blacklist):
    for blacklisted_item in blacklist:
        if blacklist in file_name:
            return False
    return True
