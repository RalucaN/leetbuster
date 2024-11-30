#################################################################
##   __ ____ ____ ______   ____            _            
##  /_ |___ \___ \____  | |  _ \          | |           
##   | | __) |__) |  / /  | |_) |_   _ ___| |_ ___ _ __ 
##   | ||__ <|__ <  / /   |  _ <| | | / __| __/ _ \ '__|
##   | |___) |__) |/ /    | |_) | |_| \__ \ ||  __/ |   
##   |_|____/____//_/     |____/ \__,_|___/\__\___|_|   
## 
#################################################################

import os                                        
import json

current_dir = os.path.dirname(__file__)
json_file_path = os.path.join(current_dir, '..', 'data', '1337_dict.json')
json_file_path = os.path.abspath(json_file_path)
with open(json_file_path, 'r') as file:
    l337_dict = json.load(file)

def norm4l1z3(d4t4):
    # This will hold all the word variations
    d4t4=d4t4.lower()
    varSet = set([])
    # This will save all the special characters in a word
    l33tChars = set([])
    maxCount=0
    for ch4r in l337_dict:
        if ch4r in d4t4:
            l33tChars.add(ch4r)
            newD4t4 = d4t4.replace(ch4r, l337_dict[ch4r][0])
            varSet.add(newD4t4)
    for ch4r in l33tChars:
        varSet=h4ndleCh4r(varSet, ch4r)
    return varSet

def h4ndleCh4r(d4t4Set, ch4r):
    h4ndl3d = set([])
    for w0rd in d4t4Set:
        for i in range(len(l337_dict[ch4r])):
            newD4t4 = w0rd.replace(ch4r, (l337_dict[ch4r])[i])
            h4ndl3d.add(newD4t4)
    return h4ndl3d