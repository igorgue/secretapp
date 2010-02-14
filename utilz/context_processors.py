from django.conf import settings as conf

def settings(request):
    return {
        'FB_API_KEY': conf.FACEBOOK_API_KEY,
    }

def member_level(request):
    from perm.tools import PERMISSION_LEVELS
    return {
        'MEMBER_LEVEL': PERMISSION_LEVELS[request.user.permission_level],
    }