from tools import permission_level, calculate_permission_name, PERMISSION_SESSION_NAME, PERMISSION_LEVELS

"""
Simple middleware to assign a users permission level to their user object.
This `level` is used when handling editable and viewable permissions on UserContent objects.
See models.py file for more details.
"""

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
        
        from urllib import urlopen
        from datetime import datetime, timedelta
        from django.utils import simplejson
        request.has_deal = False
        
        try:
            daily_deal = simplejson.loads(urlopen("http://dealer.heroku.com/ads/1/61733ff7.json").read())
            request.has_deal = daily_deal['active_now']
            request.daily_deal = daily_deal['deal']
            request.daily_deal['expires_at_date'] = datetime.strptime(request.daily_deal['expires_at'][:-6], "%Y-%m-%dT%H:%M:%S")
            timeleft = request.daily_deal['expires_at_date'] - datetime.now()
            request.daily_deal['seconds_left'] = max(0,timeleft.seconds + timeleft.days*86400)
            if request.daily_deal['seconds_left'] == 0:
                request.has_deal = False
        except:
            pass        
        
        return None