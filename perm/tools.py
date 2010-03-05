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


def remove_user_contributions(user):
    """
    Given a user. This set all UserContent contributions by that user to the anonymous user (pk=1)
    """
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import User
    
    # define old user
    if isinstance(user, (int, long, float)):
        user = User.objects.get(pk=user)
    elif not isinstance(user, User):
        raise "Please provide user as a User object or its primary key"
    
    # define anonymous user
    anon = User.objects.get(pk=1)
    
    # find all the content-types
    for ct in ContentType.objects.all():
        # check that it is a UserContent instance
        model = ct.model_class()
        if hasattr(model, 'created_by'):
            # swap the objects over to anon
            model.objects.filter(created_by=user).update(created_by=anon)
    
    return user










