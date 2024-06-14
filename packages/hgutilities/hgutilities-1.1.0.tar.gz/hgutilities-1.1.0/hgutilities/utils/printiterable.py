import numpy as np

def get_iterable_string(iterable, indent=2):
    string = ""
    level = -1
    string = recurse(iterable, string, level, indent)
    return string

def recurse(iterable, string, level, indent):
    if if_iterable(iterable):
        return is_iterable(iterable, string, level, indent)
    else:
        return end_of_iterable(iterable, string, level, indent)

def if_iterable(iterable):
    has_iter = hasattr(iterable, "__iter__")
    is_not_string = not isinstance(iterable, str)
    return (has_iter and is_not_string)
        
def is_iterable(iterable, string, level, indent):
    if isinstance(iterable, dict):
        return dict_iterable(iterable, string, level+1, indent)
    else:
        return non_dict_iterable(iterable, string, level, indent)

def dict_iterable(iterable, string, level, indent):
    for key, value in iterable.items():
        string += f"{' '*indent*level}{key}:\n"
        string += add_dict_value(value, level, indent)
    return string

def add_dict_value(value, level, indent):
    if if_iterable(value):
        return recurse(value, "", level, indent)
    else:
        return recurse(value, "", level+1, indent)

def non_dict_iterable(iterable, string, level, indent):
    if np.any([if_iterable(item) for item in iterable]):
        return non_dict_iterable_iterate(iterable, string, level+1, indent)
    else:
        return end_of_iterable(iterable, string, level, indent)

def non_dict_iterable_iterate(iterable, string, level, indent):
    new_string = "".join([recurse(value, "", level, indent)
                          for value in iterable])
    string += new_string
    return string
    
def end_of_iterable(non_iterable, string, level, indent):
    string += f"{' '*indent*level}{non_iterable}\n"
    return string

def print_iterable(iterable, indent=2):
    string = get_iterable_string(iterable, indent=indent))
    print(string)
    return string
