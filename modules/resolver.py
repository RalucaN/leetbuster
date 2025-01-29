import enchant
from nltk.corpus import wordnet
import string
import re
import numpy as np
import compress_fasttext

enchant_dict = enchant.Dict("en_US")

def preprocess_candidates(candidates):
    """Preprocess the candidates by handling special cases."""
    processed_candidates = {}

    for key, values in candidates.items():
        if isinstance(key, str):
            processed_candidates[key] = values

            if all(isinstance(value, str) and value.endswith(string.punctuation) for value in values):
                clean_key = key.rstrip(string.punctuation)
                clean_values = {value.rstrip(string.punctuation) for value in values if isinstance(value, str)}
                processed_candidates[clean_key] = clean_values
                del processed_candidates[key]

    return processed_candidates

def is_valid_word(word):
    """Check if a word is valid using the enchant dictionary."""
    return enchant_dict.check(word)

def word_exists_in_wordnet(word):
    """Check if a word exists in WordNet."""
    return len(wordnet.synsets(word)) > 0

def is_relevant_punctuation(word):
    """Check if a word is a relevant punctuation mark."""
    return word in string.punctuation

def score_word(word):
    """Score a word based on its validity in enchant and WordNet."""
    return is_valid_word(word) + word_exists_in_wordnet(word)

def rank_decoded_versions(word_set):
    """Rank the decoded versions of a word."""
    word_scores = {}
    
    for word in word_set:
        if isinstance(word, str):
            clean_word = word.rstrip(string.punctuation)
            is_punctuation = is_relevant_punctuation(word)

            if clean_word:
                whole_word_score = score_word(clean_word)
                
                if whole_word_score > 0:
                    word_score = 1000 + whole_word_score
                else:
                    parts = clean_word.split('-')
                    part_scores = [score_word(part) for part in parts if part]
                    word_score = sum(part_scores) / len(part_scores) if part_scores else 0
            else:
                word_score = is_punctuation * 2
        else:
            word_score = 0
        
        word_scores[word] = word_score

    ranked_set = dict(sorted(word_scores.items(), key=lambda item: item[1], reverse=True))
    
    max_score = max(ranked_set.values(), default=0)
    best_words = [word for word, score in ranked_set.items() if score == max_score]
    return best_words, max_score

def find_best_candidate(context, candidates, model):
    """Find the best candidate based on context using a word embedding model."""
    context_vector = sum(model[word] for word in context if isinstance(word, str) and word in model)

    if np.linalg.norm(context_vector) == 0:
        return None, float('-inf')

    best_candidate = None
    best_score = float('-inf')

    for candidate in candidates:
        if candidate in model:
            candidate_embedding = model[candidate]
            candidate_norm = np.linalg.norm(candidate_embedding)

            if candidate_norm > 0:
                score = np.dot(context_vector, candidate_embedding) / (np.linalg.norm(context_vector) * candidate_norm)
                if score > best_score:
                    best_score = score
                    best_candidate = candidate

    return best_candidate, best_score

def resolve_ambiguities(text, ambiguous_cases, model):
    """Resolve ambiguous cases in the text using context and a word embedding model."""
    words = text.split()
    resolved_text = []
    best_score = float('-inf')

    for word in words:
        if word in ambiguous_cases:
            context = [w for w in words if w != word]
            best_candidate, score = find_best_candidate(context, ambiguous_cases[word], model)
            resolved_text.append(best_candidate if best_candidate is not None else word)
            best_score = max(best_score, score)
        else:
            resolved_text.append(word)

    return ' '.join(resolved_text), best_score

def update_text(text, updates):
    """Update the text with resolved leet speak candidates."""
    sorted_updates = sorted(updates.items(), key=lambda x: len(x[0]), reverse=True)
    
    words = re.findall(r'\S+|\s+', text)
    
    for i, word in enumerate(words):
        for leet, replacement in sorted_updates:
            if isinstance(leet, str) and isinstance(replacement, str):
                if word.strip() == leet:
                    words[i] = replacement
                    break
    
    return ''.join(words)

def process_candidates(text, candidates):
    """Process candidates to resolve unambiguous cases and identify ambiguous ones."""
    updates = {}
    ambiguous = {}

    for key, values in candidates.items():
        best_words, _ = rank_decoded_versions(values)
        
        if len(best_words) == 1:
            updates[key] = best_words[0]
        elif len(best_words) > 1:
            ambiguous[key] = best_words

    text = update_text(text, updates)
    return text, ambiguous

def load_fasttext_model(model_path):
    """Load the FastText model."""
    try:
        return compress_fasttext.models.CompressedFastTextKeyedVectors.load(model_path)
    except Exception as e:
        print(f"Error loading FastText model: {e}")
        return None

def extract_final_text(texts, list_of_candidates, model_path='../data/compress_fasttext/cc.en.300.compressed.bin'):
    """Extract the final text by resolving leet speak candidates."""
    final_texts = []
    model = None
    need_model = False

    # First pass: process candidates and check if we need the model
    for text, candidates in zip(texts, list_of_candidates):
        processed_candidates = preprocess_candidates(candidates)
        text_first, ambiguous = process_candidates(text, processed_candidates)
        if ambiguous:
            need_model = True
        final_texts.append((text_first, ambiguous))

    # Load the model only if needed
    if need_model:
        print('Loading model...')
        model = load_fasttext_model(model_path)
        if model is None:
            print("Failed to load FastText model. Ambiguous cases will not be resolved.")

    # Second pass: resolve ambiguities if necessary
    resolved_texts = []
    for text, ambiguous in final_texts:
        if ambiguous and model:
            text, _ = resolve_ambiguities(text, ambiguous, model)
        resolved_texts.append(text)

    return resolved_texts
