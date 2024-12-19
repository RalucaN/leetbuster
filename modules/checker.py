import enchant
from nltk.corpus import wordnet
import string
import time
import numpy as np 

d = enchant.Dict("en_US")

start_time = time.time()


def preprocess_candidates(candidates):
    processed_candidates = {}

    for key, values in candidates.items():
        new_candidates = set()

        # Checking if key is a string
        if isinstance(key, str):
            # Case 1: Replacing first occurrence of "ph" with "f"
            if key.startswith('ph'):
                new_candidates.update(value.replace('ph', 'f', 1) for value in values if isinstance(value, str))
                processed_candidates[key] = new_candidates
            else:
                processed_candidates[key] = values

            # Case 2: Removing punctuation if all candidates end with punctuation
            if all(isinstance(value, str) and value.endswith(string.punctuation) for value in processed_candidates[key]):
                clean_key = key.rstrip(string.punctuation)
                clean_values = {value.rstrip(string.punctuation) for value in processed_candidates[key] if isinstance(value, str)}
                processed_candidates[clean_key] = clean_values
                del processed_candidates[key]  # Remove old key

    return processed_candidates


def is_valid_word(clean_word):
    return d.check(clean_word)

def word_exists_in_wordnet(clean_word):
    return len(wordnet.synsets(clean_word)) > 0

def is_relevant_punctuation(word):
    return word in string.punctuation

def rank_decoded_versions(word_set):
    word_scores = {}
    
    for word in word_set:
        # Ensure word is a string before processing
        if isinstance(word, str):
            clean_word = word.rstrip(string.punctuation)
            is_punctuation = is_relevant_punctuation(word)

            if clean_word:
                enchant_check = is_valid_word(clean_word)
                wordnet_check = word_exists_in_wordnet(clean_word)
                word_score = enchant_check + wordnet_check
            else:
                word_score = is_punctuation * 2  # Score for punctuation
        else:
            # If not a string, assign a low score or handle as needed
            word_score = 0
        
        word_scores[word] = word_score

    ranked_set = dict(sorted(word_scores.items(), key=lambda item: item[1], reverse=True))
    
    max_score = max(ranked_set.values(), default=0)
    best_words = [word for word, score in ranked_set.items() if score == max_score]

    return best_words, max_score



def find_best_candidate(context, candidates, model):
    context_vector = sum(model[word] for word in context if isinstance(word, str) and word in model)

    if context_vector.size == 0:
        return None  # Handle empty context vector

    context_norm = np.linalg.norm(context_vector)

    best_candidate = max(
        (c for c in candidates if isinstance(c, str)),
        key=lambda c: np.dot(context_vector, model[c]) / (context_norm * np.linalg.norm(model[c])) if c in model else -1,
        default=None
    )
    
    return best_candidate

def resolve_ambiguities(text, ambiguous_cases, model):
    '''
    Word2Vec models:

        'word2vec-google-news-300': Google News dataset (3 million words)
        'glove-wiki-gigaword-300': Wikipedia 2014 + Gigaword 5 (6B tokens)

    GloVe models:

        'glove-twitter-25': Twitter (2B tweets, 27B tokens)
        'glove-twitter-50': Twitter (2B tweets, 27B tokens)
        'glove-twitter-100': Twitter (2B tweets, 27B tokens)

    FastText models:

        'fasttext-wiki-news-subwords-300': Wikipedia 2017 + UMBC webbase corpus + statmt.org news dataset
    '''
    words = text.split()
    resolved_text = []
    
    for word in words:
        if word in ambiguous_cases:
            context = [w for w in words if w != word]
            best_candidate = find_best_candidate(context, ambiguous_cases[word], model)
            if best_candidate is not None:
                resolved_text.append(best_candidate)
            else:
                resolved_text.append(word)
        else:
            resolved_text.append(word)
    
    return ' '.join(resolved_text)


def update_text(text, updates):
    for leet, replacement in updates.items():

        if isinstance(leet, str) and isinstance(replacement, str):
            text = text.replace(leet, replacement)
        else:
            print(f"Skipping replacement for {leet} because it is not a string.")
    return text


def process_candidates(text, candidates):
    updates = {}
    ambiguous = {}

    for key, values in candidates.items():
        best_words, max_score = rank_decoded_versions(values)
        
        if len(best_words) == 1:
            updates[key] = best_words[0]
        elif len(best_words) > 1:
            ambiguous[key] = best_words

    text = update_text(text, updates) 
    return text, ambiguous

def extract_final_text(texts, list_of_candidates, model_name):
    final_texts = []
    model = None
    need_model = False

    # First pass: process candidates and check if we need the model
    for text, candidates in zip(texts, list_of_candidates):
        processed_candidates = preprocess_candidates(candidates)
        text_first, ambiguous = process_candidates(text, processed_candidates)
        if len(ambiguous) > 0:
            need_model = True
        final_texts.append((text_first, ambiguous))

    # Load the model only if needed
    if need_model:
        print('Loading model...')
        import gensim.downloader as api
        model = api.load(model_name)

    # Second pass: resolve ambiguities if necessary
    resolved_texts = []
    for text, ambiguous in final_texts:
        if len(ambiguous) > 0:
            text = resolve_ambiguities(text, ambiguous, model)
        resolved_texts.append(text)
    return resolved_texts

