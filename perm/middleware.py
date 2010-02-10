from tools import permission_level, calculate_permission_name, PERMISSION_SESSION_NAME, PERMISSION_LEVELS

class PermissionUserMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session') and hasattr(request, 'user'), \
            "The PermissionUserMiddleware requires session and authentification \
                middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert."
        
        # if permission level is already in session, then assign it to user object
        if PERMISSION_SESSION_NAME in request.session:
            request.user.permission_level = request.session[PERMISSION_SESSION_NAME]
        
        # otherwise workout and save
        else:
            # save to user and session
            level = permission_level(calculate_permission_name(request.user))
            request.user.permission_level = level
            request.session[PERMISSION_SESSION_NAME] = level
            request.session.modified = True
        
        return None