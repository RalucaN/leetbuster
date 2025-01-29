import os                                        
import json

current_dir = os.path.dirname(__file__)
json_file_path = os.path.join(current_dir, '..', 'data', '1337_dict.json')
json_file_path = os.path.abspath(json_file_path)
with open(json_file_path, 'r') as file:
    LEET_DICT = json.load(file)


def normalize(data):

    data = data.lower()
    varSet = set([])

    leet_chars = set([])

    for char in LEET_DICT:
        if char in data:
            leet_chars.add(char)
            newdata = data.replace(char, LEET_DICT[char][0])
            varSet.add(newdata)
            
            if newdata.startswith('f'):
                varSet.add('ph' + newdata[1:])
            elif newdata.startswith('ph'):
                varSet.add('f' + newdata[2:])

    for char in leet_chars:
        varSet=handle_char(varSet, char)
    return varSet


def handle_char(data_set, char):
    handled = set()
    for word in data_set:
        for replacement in LEET_DICT[char]:
            new_data = word.replace(char, replacement)
            handled.add(new_data)
    return handled
