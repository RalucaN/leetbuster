import json
import random
import re
from pyleetspeak.LeetSpeaker import LeetSpeaker

def generate_leet_variations(words, num_variations=5):
    all_variations = {}
    
    for word in words:
        word_variations = set()
        
        for _ in range(num_variations):
            change_prb = random.uniform(0.5, 1.0)
            change_frq = random.uniform(0.5, 1.0)
            
            leet_speaker = LeetSpeaker(
                change_prb=change_prb,
                change_frq=change_frq,
                mode="basic", #"basic", "intermediate", "advanced", "covid_basic", "covid_intermediate", None
                seed=None,
                verbose=False
            )
            leet_result = leet_speaker.text2leet(word)
            if leet_result != word:
                word_variations.add(leet_result)
        
        if word_variations:
            all_variations[word] = list(word_variations)
    
    return all_variations


def custom_tokenizer(text):
    pattern = re.compile(r'(?<!\w\.\w.)(?<!\w\.\w\.\w)(?<=\s|\.)|(?<=[a-z])(?=[A-Z])')
    
    tokens = pattern.split(text)
    tokens = [token for token in tokens if token]
    return tokens

def transform_to_leet_variations(texts, use_nltk=False, pos_types=None, num_variations=5):
    leet_variations_dict = {}
    
    for input_text in texts:

        if use_nltk:
            import nltk
            words = nltk.word_tokenize(input_text)
            pos_tags = nltk.pos_tag(words)
            
            for word, tag in pos_tags:
                if pos_types is not None and tag in pos_types:
                    variations = generate_leet_variations([word], num_variations)
                    for key, value in variations.items():
                        if key in leet_variations_dict:
                            leet_variations_dict[key] = list(set(leet_variations_dict[key]) | set(value))
                        else:
                            leet_variations_dict[key] = value
        else:
            words = custom_tokenizer(input_text)

            for word in words:
                variations = generate_leet_variations([word], num_variations)
                for key, value in variations.items():
                    if key in leet_variations_dict:
                        leet_variations_dict[key] = list(set(leet_variations_dict[key]) | set(value))
                    else:
                        leet_variations_dict[key] = value

    return leet_variations_dict

def save_variations_to_json(variations_dict, filename):
    with open(filename, 'w') as json_file:
        json.dump(variations_dict, json_file, indent=4)


pos_types_to_replace_nltk = [
    'NN', 'NNS', 'NNP', 'NNPS',   # Nouns
    'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ',   # Verbs
    'JJ', 'JJR', 'JJS',   # Adjectives
    'RB', 'RBR', 'RBS'    # Adverbs
]

text = ["Andrew is a boy.He is my friend."]
filename='leet_variations_advanced.json'


variations_dict = transform_to_leet_variations(text, num_variations=10)
save_variations_to_json(variations_dict, filename)

print("Leet Variations Dictionary:", len(variations_dict))
