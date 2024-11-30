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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from normalizer import norm4l1z3
import time

testData = [
    "H3ll0, h0w 4r3 y0u?",
    "L3t's g0 70 th3 m0v13s 70n1ght.",
    "Th1s 1s g01ng 70 b3 4w3s0m3!",
    "1 c4n h3lp y0u w1th y0ur c0d3.",
    "Wh3n 1s th3 n3xt g4m3?",
    "4lw4ys b3 l34rn1ng n3w th1ngs.",
    "5t4y c00l 4nd k33p h4ck1ng!",
    "1 l0v3 pl4y1ng v1d30 g4m3s.",
    "C0ngr47ul4710ns 0n y0ur succ3ss!",
    "D0 y0u kn0w 4ny g00d b00ks 70 r34d?"
]

validationData = [
    "Hello, how are you?",
    "Let's go to the movies tonight.",
    "This is going to be awesome!",
    "I can help you with your code.",
    "When is the next game?",
    "Always be learning new things.",
    "Stay cool and keep hacking!",
    "I love playing video games.",
    "Congratulations on your success!",
    "Do you know any good books to read?"
]

normalizedVariants = {}
total=len(testData)
accuracy=0
passing=0
start = time.time()
for index in range(len(testData)):
    normalizedVariants[index]=norm4l1z3(testData[index])
    if validationData[index].lower() in normalizedVariants[index]:
        passing+=1
end = time.time()
duration = end - start
print(f"[{passing/total*100}%]: {passing}/{total} successful in {duration} seconds")