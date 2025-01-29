# constants.py
import re
import string

LEET_PATTERN = re.compile(r'^(?=.*[0-9@$!_€£¥]).+$')
WEBSITE_PATTERN = re.compile(r'^(https?|ftp|file):\/\/|(?:www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(:[0-9]+)?(\/[^\s]*)?$')
PUNCTUATION_PATTERN = re.compile(f'^[{re.escape(string.punctuation)}]+$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
FILE_EXTENSION_PATTERN = re.compile(r'\.[a-zA-Z0-9]{2,4}$')
NUMERIC_SEPARATOR = re.compile(r'^\d{1,3}(,\d{3})+(.\d+)?$')
FLOAT_PATTERN = re.compile(r'^\d+\.\d+$')
MONEY_PATTERN = re.compile(r'^([^\w\s])(\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+(\.\d{1,2})?)$|^(\d{1,3}(,\d{3})*(\.\d{1,2})?|\d+(\.\d{1,2})?)([^\w\s])$')
ISBN_PATTERN = re.compile(r'^(\d{1,5}-){1,5}\d{1,5}$')
VERSION_NUM_PATTERN = re.compile(r'^v?\d+(\.\d+)+$')
# add %, with or without float num
# TO DO: HANDLING ENCODING AND UNICODE CHARS