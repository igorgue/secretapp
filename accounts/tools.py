from socialauth.models import FacebookUserProfile
from models import *

AUGMENTED_USER_SESSION_NAME = 'extended_user'

def augment_user_dict(user):
    """
    Builds a dictionary of information which can be
    applied to the user object as attributes.
    This is a culmination of extra data we may need on an average page.
    """
    data = {}
    
    # check socialauth-facebook profile data
    try:
        data['facebook'] = FacebookUserProfile.objects.filter(user=user).latest('pk')
    except FacebookUserProfile.DoesNotExist:
        data['facebook'] = None
    
    # check notification settings
    data['settings'], new = UserSettings.objects.get_or_create(user=user)
    
    return data

def update_agument_session(request, data=None):
    """
    Helper for the above which updates the session with the new data
    """
    if data is None:
        data = augment_user_dict(request.user)
    request.session[AUGMENTED_USER_SESSION_NAME] = data
    request.session.modified = True
    return request


def augment_user(user, data=None):
    """
    Helper for the above but applies everything to it
    """
    if data is None:
        data = augment_user_dict(user)
    
    # assign data to user
    for key, value in data.items():
        setattr(user, key, value)
    
    return user