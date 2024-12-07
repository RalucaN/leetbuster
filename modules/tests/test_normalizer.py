#################################################################
##   __ ____ ____ ______   ____            _            
##  /_ |___ \___ \____  | |  _ \          | |           
##   | | __) |__) |  / /  | |_) |_   _ ___| |_ ___ _ __ 
##   | ||__ <|__ <  / /   |  _ <| | | / __| __/ _ \ '__|
##   | |___) |__) |/ /    | |_) | |_| \__ \ ||  __/ |   
##   |_|____/____//_/     |____/ \__,_|___/\__\___|_|   
## 
#################################################################

import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from normalizer import norm4l1z3
import time

# Load the test data
def loadData(filename):
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, '../..', 'data', filename)
    json_file_path = os.path.abspath(json_file_path)
    with open(json_file_path, 'r') as file:
        d4t4 = json.load(file)
    return d4t4

def test(d4t4):
    failedWords = []
    total=0
    accuracy=0
    passing=0
    start = time.time()
    for key in d4t4.keys():
        for leet in d4t4[key]:
            total+=1
            normalizedVariants=norm4l1z3(leet)
            if key.lower() in normalizedVariants:
                passing+=1
            else:
                failedWords.append({"natural":key,
                    "leet":leet, 
                    "variants":normalizedVariants})
    end = time.time()
    duration = end - start
    print(f"[{passing/total*100}%]: {passing}/{total} successful in {duration} seconds")

def main():
    test(loadData("test_basic.json"))

if __name__ == "__main__": 
    main()