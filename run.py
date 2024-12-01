#################################################################
##   __ ____ ____ ______   ____            _            
##  /_ |___ \___ \____  | |  _ \          | |           
##   | | __) |__) |  / /  | |_) |_   _ ___| |_ ___ _ __ 
##   | ||__ <|__ <  / /   |  _ <| | | / __| __/ _ \ '__|
##   | |___) |__) |/ /    | |_) | |_| \__ \ ||  __/ |   
##   |_|____/____//_/     |____/ \__,_|___/\__\___|_|   
## 
#################################################################

from modules.identifycandidates import LeetCandidate
from modules.normalizer import norm4l1z3


if __name__ == "__main__":
    detector = LeetCandidate(verbose=False)
    text = "! @m a l33t h@(]<er. ph3@r my m4|) $k|ll$. +h3 90s w3r3 0ver tw0 d3(ad3$ 4g0 24/02/90."
    candidates = detector.analyze_text(text)


    for key in candidates.keys():
        print(norm4l1z3(key))