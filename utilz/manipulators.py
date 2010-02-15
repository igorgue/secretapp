import re

def safe_title(text):
    """
    For making URL's pretty
        1. Removes danger characters
        2. Strips space
        3. Removes double space
        4. Converts remaining space to dashes
    
    See tests.py for usage
    """
    return re.sub(r'[^a-zA-Z0-9_\ \-]', '', text).strip().replace('  ', ' ').replace(' ', '-').lower()