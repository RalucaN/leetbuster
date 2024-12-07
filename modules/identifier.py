import re
import datefinder
from dateutil.parser import parse

class LeetCandidate:
    def __init__(self, verbose=False):
        self.leet_chars = frozenset('0123456789@$!')
        self.leet_pattern = re.compile(r'^(?=.*[0-9@$!]).+$')
        self.verbose = verbose
        self.word_logs = {}

    def log_word(self, word, message):
        if self.verbose:
            if word not in self.word_logs:
                self.word_logs[word] = []
            self.word_logs[word].append(message)

    def is_potential_leet(self, word):
        result = bool(self.leet_pattern.match(word))
        self.log_word(word, f"Potential leet: {result}")
        return result


    def is_date(self, word):
        try:
            # Try parsing with dayfirst
            parse(word, dayfirst=True)
            result = True
        except ValueError:
            try:
                # Try parsing with yearfirst
                parse(word, yearfirst=True)
                result = True
            except ValueError:
                    result = False
        self.log_word(word, f"Is date: {result}")
        return result


    def is_leet_candidate(self, word):
        check_word = word.lstrip('#')
        
        if self.is_potential_leet(check_word):
            if not self.is_date(check_word):
                self.log_word(word, "Leet candidate: True")
                return True
        
        self.log_word(word, "Leet candidate: False")
        return False

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
