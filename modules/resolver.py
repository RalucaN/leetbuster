import enchant
from nltk.corpus import wordnet
import string
import time
import re
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
            if key.lower().startswith('ph'):
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

def score_word(word):
    enchant_check = is_valid_word(word)
    wordnet_check = word_exists_in_wordnet(word)
    return enchant_check + wordnet_check

def rank_decoded_versions(word_set):
    word_scores = {}
    
    for word in word_set:
        if isinstance(word, str):
            clean_word = word.rstrip(string.punctuation)
            is_punctuation = is_relevant_punctuation(word)

            if clean_word:
                whole_word_score = score_word(clean_word)
                
                if whole_word_score > 0:
                    word_score = 1000  + whole_word_score
                else:
                    parts = clean_word.split('-')
                    part_scores = [score_word(part) for part in parts if part]
                    if part_scores:

                        word_score = sum(part_scores) / len(part_scores)
                    else:
                        word_score = 0
            else:
                word_score = is_punctuation * 2  # Score for punctuation
        else:
            word_score = 0
        
        word_scores[word] = word_score

    ranked_set = dict(sorted(word_scores.items(), key=lambda item: item[1], reverse=True))
    
    max_score = max(ranked_set.values(), default=0)
    best_words = [word for word, score in ranked_set.items() if score == max_score]
    return best_words, max_score

def find_best_candidate(context, candidates, model):
    

    context_vector = sum(model[word] for word in context if isinstance(word, str) and word in model)

    if np.linalg.norm(context_vector) == 0:
        return None  # Handle empty context vector

    best_candidate = None
    best_score = float('-inf')

    for candidate in candidates:
        if candidate in model:  # Check if candidate is in the model
            candidate_embedding = model[candidate]
            candidate_norm = np.linalg.norm(candidate_embedding)

            if candidate_norm > 0:  # Ensure candidate embedding is valid
                score = np.dot(context_vector, candidate_embedding) / (np.linalg.norm(context_vector) * candidate_norm)
                if score > best_score:
                    best_score = score
                    best_candidate = candidate

    return best_candidate, best_score


def resolve_ambiguities(text, ambiguous_cases, model):
    words = text.split()
    resolved_text = []
    best_score = float('-inf')
    for word in words:
        if word in ambiguous_cases:
            context = [w for w in words if w != word]
            best_candidate, best_score = find_best_candidate(context, ambiguous_cases[word], model)
            if best_candidate is not None:
                resolved_text.append(best_candidate)
            else:
                resolved_text.append(word)

        else:
            resolved_text.append(word)

    
    return ' '.join(resolved_text), best_score

def update_text(text, updates):
    sorted_updates = sorted(updates.items(), key=lambda x: len(x[0]), reverse=True)
    
    words = re.findall(r'\S+|\s+', text)
    
    for i, word in enumerate(words):
        for leet, replacement in sorted_updates:
            if isinstance(leet, str) and isinstance(replacement, str):
                if word.strip() == leet:
                    words[i] = replacement
                    break
    
    updated_text = ''.join(words)
    return updated_text

def process_candidates(text, candidates):
    updates = {}
    ambiguous = {}

    for key, values in candidates.items():
        best_words, max_score = rank_decoded_versions(values)
        
        if len(best_words) == 1:
            updates[key] = best_words[0] # to update the casing to be the same as the key
        elif len(best_words) > 1:
            ambiguous[key] = best_words

    text = update_text(text, updates)
    return text, ambiguous

def extract_final_text(texts, list_of_candidates):
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
        import compress_fasttext
        try:
            model = compress_fasttext.models.CompressedFastTextKeyedVectors.load('../data/compress_fasttext/cc.en.300.compressed.bin')
        except:
            model = compress_fasttext.models.CompressedFastTextKeyedVectors.load('https://github.com/avidale/compress-fasttext/releases/download/v0.0.4/cc.en.300.compressed.bin')

    # Second pass: resolve ambiguities if necessary
    resolved_texts = []
    for text, ambiguous in final_texts:
        if len(ambiguous) > 0:
            text = resolve_ambiguities(text, ambiguous, model)
        resolved_texts.append(text)

    return resolved_texts
