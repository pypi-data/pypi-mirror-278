def remove_none_values(dictionary):
    filtered_dictionary = {key: value for key, value in dictionary.items()
                           if value is not None}
    return filtered_dictionary

def transpose_list(my_list):
    transposed_list = list(map(list, zip(*my_list)))
    return transposed_list

def print_dict_aligned(dictionary):
    keys = list(dictionary.keys())
    max_length = max([len(str(key)) for key in keys])
    for key, value in dictionary.items():
        spaces = max_length - len(str(key))
        print(f"{key}: {spaces*' '}{value}")
