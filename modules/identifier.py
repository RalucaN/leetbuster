from .constants import *
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
import emoji

def log_word(word, message, word_logs):
    if word not in word_logs:
        word_logs[word] = []
    word_logs[word].append(message)

def is_potential_leet(word, word_logs=None):
    result = bool(LEET_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Potential leet: {result}", word_logs)
    return result

def is_numeric(word, word_logs=None):
    word = word.strip()
    result = bool(FLOAT_PATTERN.match(word) or NUMERIC_SEPARATOR.match(word))
    if word_logs is not None:
        log_word(word, f"Is numeric: {result}", word_logs)
    return result

def is_date(word, word_logs=None):
    try:
        parse(word, dayfirst=True, fuzzy=False)
        result = True
    except (ValueError, OverflowError, ParserError):
        try:
            parse(word, yearfirst=True, fuzzy=False)
            result = True
        except (ValueError, OverflowError, ParserError):
            result = False
    if word_logs is not None:
        log_word(word, f"Is date: {result}", word_logs)
    return result

def is_website(word, word_logs=None):
    result = bool(WEBSITE_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Is website: {result}", word_logs)
    return result

def is_just_punctuation(word, word_logs=None):
    result = bool(PUNCTUATION_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Contains only punctuation: {result}", word_logs)
    return result

def is_email(word, word_logs=None):
    result = bool(EMAIL_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Is email: {result}", word_logs)
    return result

def has_file_extension(word, word_logs=None):
    result = bool(FILE_EXTENSION_PATTERN.search(word))
    if word_logs is not None:
        log_word(word, f"Has file extension: {result}", word_logs)
    return result

def is_money(word, word_logs=None):
    result = bool(MONEY_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Is money: {result}", word_logs)
    return result

def is_emoji_code(word, word_logs=None):
    contains_emoji = emoji.emoji_count(word) > 0
    is_shortcode = emoji.is_emoji(emoji.emojize(word, language='alias'))
    try:
        is_unicode = emoji.is_emoji(chr(int(word.strip('U+'), 16)))
    except ValueError:
        is_unicode = False
    result = contains_emoji or is_shortcode or is_unicode
    if word_logs is not None:
        log_word(word, f"Contains emoji or is emoji code: {result}", word_logs)
    return result

def is_version_number(word, word_logs=None):
    result = bool(VERSION_NUM_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Is version number: {result}", word_logs)
    return result

def is_isbn(word, word_logs=None):
    result = bool(ISBN_PATTERN.match(word))
    if word_logs is not None:
        log_word(word, f"Is ISBN: {result}", word_logs)
    return result

def is_leet_candidate(word, word_logs=None):
    check_word = word.lstrip('#')

    if check_word.isdigit():
        if word_logs is not None:
            log_word(word, "Leet candidate: True (digit)", word_logs)
        return True

    if is_numeric(check_word, word_logs) or is_just_punctuation(check_word, word_logs):
        if word_logs is not None:
            log_word(word, "Leet candidate: False", word_logs)
        return False

    if not is_potential_leet(check_word, word_logs):
        if word_logs is not None:
            log_word(word, "Leet candidate: False", word_logs)
        return False

    if (is_website(check_word, word_logs) or 
        is_version_number(check_word, word_logs) or 
        is_isbn(check_word, word_logs) or 
        is_email(check_word, word_logs) or
        has_file_extension(check_word, word_logs) or
        is_money(check_word, word_logs) or
        is_date(check_word, word_logs) or
        is_emoji_code(check_word, word_logs)):
        if word_logs is not None:
            log_word(word, "Leet candidate: False", word_logs)
        return False

    if word_logs is not None:
        log_word(word, "Leet candidate: True", word_logs)
    return True

def analyze_text(text, verbose=False):
    words = text.split()
    candidates = set()
    word_logs = {} if verbose else None
    
    for word in words:
        if is_leet_candidate(word, word_logs):
            candidates.add(word)

    return candidates, word_logs

def get_word_logs(word_logs, word):
    return word_logs.get(word, []) if word_logs else []
