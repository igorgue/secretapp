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


def unique(seq, preserve=False):
    """
    Given a sequence. This returns the unique version.
    Takes second optional argument which specifies whether to preserve order.
    """
    if preserve:
        # order preserving 
        seen = {} 
        result = [] 
        for item in seq:
            if item in seen: continue
            seen[item] = 1 
            result.append(item) 
        return result
    else:
        seen = {}
        for item in seq: 
            seen[item] = 1 
        return seen.keys()