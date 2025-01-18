#################################################################
##   __ ____ ____ ______   ____            _            
##  /_ |___ \___ \____  | |  _ \          | |           
##   | | __) |__) |  / /  | |_) |_   _ ___| |_ ___ _ __ 
##   | ||__ <|__ <  / /   |  _ <| | | / __| __/ _ \ '__|
##   | |___) |__) |/ /    | |_) | |_| \__ \ ||  __/ |   
##   |_|____/____//_/     |____/ \__,_|___/\__\___|_|   
## 
#################################################################

from modules.identifier import LeetCandidate
from modules.normalizer import norm4l1z3
from modules.resolver import extract_final_text
import time
import pandas as pd


texts_df=pd.read_csv('data.csv')

texts=texts_df['text'].to_list()

if __name__ == "__main__":
    detector = LeetCandidate(verbose=False)
    start_time=time.time()
    list_of_candidates = []

    for text in texts:
        leets = detector.analyze_text(text)

        candidates={}
        for key in leets:
            candidates[key]=norm4l1z3(key)
            
        list_of_candidates.append(candidates)
        
    results=extract_final_text(texts, list_of_candidates)
    print(results)
    texts_df['results']=results
    texts_df.to_csv('reviewing.csv', index=False)

    print(f'Total time: {time.time()-start_time}')

