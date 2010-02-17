from django.contrib.auth.models import User
from django.conf import settings
from facebook import Facebook

from socialauth.models import FacebookUserProfile, AuthMeta
from socialauth.lib.facebook import get_user_info, get_facebook_signature

from datetime import datetime
import random

FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')
FACEBOOK_URL = getattr(settings, 'FACEBOOK_URL', 'http://api.facebook.com/restserver.php')

        
class ClaimFacebookBackend:
    def authenticate(self, request):

        """
        This is exactly the same as the backend found in
            http://github.com/uswaretech/Django-Socialauth/blob/master/socialauth/auth_backends.py
        
        @@ ~ line 46
        -- user = User.objects.create(username = username)
        ++ user, new_user = User.objects.get_or_create(username = username)
        ++ user.is_active = True
        
        ++ from perm.tools import PERMISSION_LEVEL
        ++ del request.session[PERMISSION_SESSION_NAME]
        ++ request.session.modified = True
        """

        facebook =  Facebook(settings.FACEBOOK_API_KEY,
                             settings.FACEBOOK_SECRET_KEY)
                             
        check = facebook.check_session(request)
        try:
            fb_user = facebook.users.getLoggedInUser()
            profile = FacebookUserProfile.objects.get(facebook_uid = unicode(fb_user))
            return profile.user
        except FacebookUserProfile.DoesNotExist:
            fb_data = facebook.users.getInfo([fb_user], ['uid', 'about_me', 'first_name', 'last_name', 'pic_big', 'pic', 'pic_small', 'current_location', 'profile_url'])
            if not fb_data:
                return None
            fb_data = fb_data[0]

            username = 'FB:%s' % fb_data['uid']
            #user_email = '%s@example.facebook.com'%(fb_data['uid'])
            user,new_user = User.objects.get_or_create(username = username)
            user.is_active = True
            user.first_name = fb_data['first_name']
            user.last_name = fb_data['last_name']
            user.save()
            location = unicode(fb_data['current_location'])
            about_me = unicode(fb_data['about_me'])[0:100]
            url = unicode(fb_data['profile_url'])
            fb_profile = FacebookUserProfile(facebook_uid = unicode(fb_data['uid']), user = user, profile_image_url = fb_data['pic'], profile_image_url_big = fb_data['pic_big'], profile_image_url_small = fb_data['pic_small'], location=location, about_me=about_me, url=url)
            try:
                fb_profile.save()
                auth_meta = AuthMeta(user=user, provider='Facebook').save()
            except:
                pass
            
            from perm.tools import PERMISSION_SESSION_NAME
            if PERMISSION_SESSION_NAME in request.session:
                del request.session[PERMISSION_SESSION_NAME]
                request.session.modified = True
            return user
        except Exception, e:
            pass
            #print unicode(e)

        return None

    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None
