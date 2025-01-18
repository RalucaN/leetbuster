import re
from dateutil.parser import parse
from dateutil.parser._parser import ParserError
import string
import emoji

class LeetCandidate:
    def __init__(self, verbose=False):
        self.leet_pattern = re.compile(r'^(?=.*[0-9@$!_€£¥]).+$')
        self.website_pattern = re.compile(
                                r'^(https?|ftp|file):\/\/'  # Protocol
                                r'|(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Domain name with optional www
                                r'(:[0-9]+)?'  # Port
                                r'(\/[^\s]*)?$'  # Path
                            )
        self.punctuation_pattern = re.compile(f'^[{re.escape(string.punctuation)}]+$')
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        self.file_extension_pattern = re.compile(r'\.[a-zA-Z0-9]{2,4}$')
        self.numeric_separator = re.compile(r'^\d{1,3}(,\d{3})+(.\d+)?$')
        self.float = re.compile(r'^\d+\.\d+$')
        # add %, with or without float num
        self.money_pattern = re.compile(r'^([^\w\s])(\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+(\.\d{1,2})?)$|^(\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+(\.\d{1,2})?)([^\w\s])$')
        self.isbn=re.compile(r'^(\d{1,5}-){1,5}\d{1,5}$')
        self.version_num=re.compile(r'^v?\d+(\.\d+)+$')
        self.verbose = verbose
        self.word_logs = {}
        
    # TO DO: HANDLING ENCODING AND UNICODE CHARS

    def log_word(self, word, message):
        if self.verbose:
            if word not in self.word_logs:
                self.word_logs[word] = []
            self.word_logs[word].append(message)

    def is_potential_leet(self, word):
        result = bool(self.leet_pattern.match(word))
        self.log_word(word, f"Potential leet: {result}")
        return result
    
    def is_numeric(self, word):
        word = word.strip()

        if self.float.match(word):
            self.log_word(word, f"Is numeric (float): True")
            return True

        if self.numeric_separator.match(word):
            self.log_word(word, f"Is numeric (with thousand separator): True")
            return True

        self.log_word(word, f"Is numeric: False")
        return False

    def is_date(self, word):
        try:
            parse(word, dayfirst=True, fuzzy=False)
            result = True
        except (ValueError, OverflowError, ParserError):
            try:
                parse(word, yearfirst=True, fuzzy=False)
                result = True
            except (ValueError, OverflowError, ParserError):
                result = False
        self.log_word(word, f"Is date: {result}")
        return result
    
    def is_website(self, word):
        result = bool(self.website_pattern.match(word))
        self.log_word(word, f"Is website: {result}")
        return result
    
    def is_just_punctuation(self, word):
        result=bool(self.punctuation_pattern.match(word))
        self.log_word(word, f"Contains only punctuation:{result}")
        return result
    
    def is_email(self, word):
        result = bool(self.email_pattern.match(word))
        self.log_word(word, f"Is email: {result}")
        return result

    def has_file_extension(self, word):
        result = bool(self.file_extension_pattern.search(word))
        self.log_word(word, f"Is file extension: {result}")
        return result
    
    def is_money(self, word):
        result = bool(self.money_pattern.match(word))
        self.log_word(word, f"Is money: {result}")
        return result

    def is_emoji_code(self, word):
        contains_emoji = emoji.emoji_count(word) > 0

        is_shortcode = emoji.is_emoji(emoji.emojize(word, language='alias'))
        
        try:
            is_unicode = emoji.is_emoji(chr(int(word.strip('U+'), 16)))
        except ValueError:
            is_unicode = False
        
        result = contains_emoji or is_shortcode or is_unicode
        self.log_word(word, f"Contains emoji or is emoji code: {result}")
        return result

    def is_version_number(self, word):
        return bool(self.version_num.match(word))

    def is_isbn(self, word):
        return bool(self.isbn.match(word))

    def is_leet_candidate(self, word):
        check_word = word.lstrip('#')

        if check_word.isdigit():
            self.log_word(word, "Leet candidate: True (digit)")
            return True

        if self.is_numeric(check_word) or self.is_just_punctuation(check_word):
            self.log_word(word, "Leet candidate: False")
            return False

        if not self.is_potential_leet(check_word):
            self.log_word(word, "Leet candidate: False")
            return False

        if (self.is_website(check_word) or 
            self.is_version_number(check_word) or 
            self.is_isbn(check_word) or 
            self.is_email(check_word) or
            self.has_file_extension(check_word) or
            self.is_money(check_word) or
            self.is_date(check_word) or
            self.is_emoji_code(check_word)):
            self.log_word(word, "Leet candidate: False")
            return False

        self.log_word(word, "Leet candidate: True")
        return True


    def analyze_text(self, text):
        words = text.split()
        candidates = set()
        
        current_index = 0
        
        for word in words:
            start_position = text.find(word, current_index)
            self.log_word(word, f"Position: {start_position}")

            if self.is_leet_candidate(word):
                candidates.add(word)

            current_index = start_position + len(word)

        return candidates

    def get_word_logs(self, word):
        return self.word_logs.get(word, [])
