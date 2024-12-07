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
from modules.checker import extract_final_text
import time

texts = ["! @m a l33t h@ck3r. ph3@r my m4d $k|ll$. +h3 90s w3r3 0ver tw0 d3(ad3$ 4g0 29/04/87."]

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

    results=extract_final_text(texts, list_of_candidates, "glove-twitter-50")
    
    for t in results:
        print(t)

    print(f'Total time: {time.time()-start_time}')

