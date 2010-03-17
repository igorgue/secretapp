from django.contrib.auth.models import User
from django.conf import settings
from facebook import Facebook

from socialauth.models import FacebookUserProfile, AuthMeta
from socialauth.lib.facebook import get_user_info, get_facebook_signature

from tools import clear_permissions
from datetime import datetime
import random

FACEBOOK_API_KEY = getattr(settings, 'FACEBOOK_API_KEY', '')
FACEBOOK_SECRET_KEY = getattr(settings, 'FACEBOOK_SECRET_KEY', '')
FACEBOOK_URL = getattr(settings, 'FACEBOOK_URL', 'http://api.facebook.com/restserver.php')

class ClaimFacebookBackend:
    def authenticate(self, request):

        """
        Started at 
            http://github.com/uswaretech/Django-Socialauth/blob/master/socialauth/auth_backends.py
        
        Made massive improvements with error handling.
        """
        facebook =  Facebook(settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
        check = facebook.check_session(request)
        clear_permissions(request) # for internal perms
        try:
            fb_user = facebook.users.getLoggedInUser()
            profile = FacebookUserProfile.objects.get(facebook_uid = unicode(fb_user))
            user = profile.user
            if not user.email:
                fb_data = facebook.users.getInfo([fb_user], ['email'])
                user.email = fb_data[0]['email']
                user.save()
            return user
        except FacebookUserProfile.DoesNotExist:
            fb_data = None
            try_count = 0
            max_count = 3
            while not fb_data and try_count < max_count:
                try:
                    fb_data = facebook.users.getInfo([fb_user], ['uid', 'email', 'about_me', 'first_name', 'last_name', 'pic_big', 'pic', 'pic_square', 'current_location', 'profile_url'])
                    break
                except:
                    try_count += 1
            if not fb_data:
                return None
            fb_data = fb_data[0]
            username = 'FB:%s' % fb_data['uid']
            if 'email' in fb_data:
                user_email = fb_data['email']
            user,new_user = User.objects.get_or_create(username = username)
            user.is_active = True
            user.first_name = fb_data['first_name']
            user.last_name = fb_data['last_name']
            user.save()
            location = unicode(fb_data['current_location'])
            about_me = unicode(fb_data['about_me'])[0:100]
            url = unicode(fb_data['profile_url'])
            fb_profile = FacebookUserProfile(facebook_uid = unicode(fb_data['uid']), user = user, profile_image_url = fb_data['pic'], profile_image_url_big = fb_data['pic_big'], profile_image_url_small = fb_data['pic_square'], location=location, about_me=about_me, url=url)
            try:
                fb_profile.save()
                auth_meta = AuthMeta(user=user, provider='Facebook').save()
            except:
                pass
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
