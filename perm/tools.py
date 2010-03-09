PERMISSION_LEVELS = ('Visitor', 'Member', 'Keeper', 'Seneschal', 'Secretary')
PERMISSION_SESSION_NAME = 'permission_level'

def clear_permissions(request):
    """
    Clears the permissions from the session so they can be reset
    """
    if PERMISSION_SESSION_NAME in request.session:
        del request.session[PERMISSION_SESSION_NAME]
        request.session.modified = True
    return request

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
        if user.is_superuser:
            # make superusers the top
            name = PERMISSION_LEVELS[-1]
        else:
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



def calculate_time_since(then):
    from datetime import datetime, timedelta
    from django.template.defaultfilters import date as formatdate  
    
    if not then:
        return "unknown"
    
    now = datetime.now()
    
    if then >= now:
        return "just now"
    
    diff = now - then
    
    seconds = diff.seconds
    if seconds < 60:
        return "%s seconds ago" % (str(seconds))
    
    minutes = seconds / 60    
    if minutes < 60:
        return "%s minutes ago" % (str(minutes))

    hours = minutes / 60
    if hours <= 12:
        return "%s hours ago" % (str(hours))
    
    if now.year == then.year:
        if diff.days < 7:
            return "last %s" % (formatdate(then, "l"))
        else:
            return formatdate(then, "M d") 
    else:
        return formatdate(then, "M d, Y") 
    
    
    
    
    
