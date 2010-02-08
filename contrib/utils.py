import re

def safe_title(text):
    """
    For making URL's pretty
        1. Removes danger characters
        2. Strips space
        3. Removes double space
        4. Converts remaining space to dashes
    
    >>> safe_title("Where can I buy good cheese ")
    'Where-can-I-buy-good-cheese'
    
    >>> safe_title("Is 12 fish  enough $!}{} pur-ple monkey")
    'Is-12-fish-enough-pur-ple-monkey'
    """
    return re.sub(r'[^a-zA-Z0-9_\ \-]', '', text).strip().replace('  ', ' ').replace(' ', '-')