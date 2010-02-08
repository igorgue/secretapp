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
    return re.sub(r'[^a-zA-Z0-9_\ \-]', '', text).strip().replace('  ', ' ').replace(' ', '-')



PERMISSION_LEVELS = ('Visitor', 'Member', 'Keeper', 'Seneschal', 'Secretary')
PERMISSION_SESSION_NAME = 'permission_level'

def permission_level(name):
    """
    Makes handling permission levels easier by converting name into number

    See tests.py for usage
    """
    for i in xrange(len(PERMISSION_LEVELS)):
        if PERMISSION_LEVELS[i] == name:
            break
    return i

def calculate_permission_name(user):
    """
    Calculates a users permission name based on give `user`

    See test.py for usage
    """
    name = None
    if user.is_authenticated():
        # if user belongs to one of the top groups
        # then select that as permission name
        groups = list(PERMISSION_LEVELS[2:])
        groups.reverse()
        for group_name in groups:
            if user.groups.filter(name=group_name).count() > 0:
                name = group_name
                break
        # if doesn't belong to any group - is just a Member
        if not name:
            name = 'Member'
    else:
        # if not even logged in - then is just a Visitor
        name = 'Visitor'
    # return the name
    return name
