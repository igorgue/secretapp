from django.conf import settings as conf

def settings(request):
    return {
        'FB_API_KEY': conf.FACEBOOK_API_KEY,
    }

def ajax(request):
    return {
        'IS_AJAX': request.is_ajax(),
    }

def member_level(request):
    from perm.tools import PERMISSION_LEVELS
    if hasattr(request.user, 'permission_level'):
        level = PERMISSION_LEVELS[request.user.permission_level]
    else:
        level = 0
    return {
        'MEMBER_LEVEL': level,
        }