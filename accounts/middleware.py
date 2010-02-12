from socialauth.models import FacebookUserProfile
from tools import *

"""
Handles saving of cool extra user data onto request.user
This data includes but is not limited to, is_facebook (bool), profile_image_url etc...
"""

class AugmentAccountMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session') and hasattr(request, 'user'), \
            "The PermissionUserMiddleware requires session and authentification \
                middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert."
        
        user = request.user
        
        # obviously only applicable if logged in
        if user.is_authenticated():
            # if object already exists in session get from there
            if AUGMENTED_USER_SESSION_NAME in request.session:
                data = request.session[AUGMENTED_USER_SESSION_NAME]
            # otherwise calculate a fresh copy and save to object
            else:
                data = augment_user_dict(user)
                update_agument_session(request, data)
            
            user = augment_user(user, data)
        else:
            user.augmented = False
        
        # this isn't really needed by makes it more clear
        request.user = user
        return None