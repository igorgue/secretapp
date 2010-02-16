from django.conf import settings as conf


def globals(request):
    return {
        'FB_API_KEY':   conf.FACEBOOK_API_KEY,
        'GOOGLE_MAPS_API': conf.GOOGLE_MAPS_API,
        'IS_AJAX':      request.is_ajax(),
        'MEMBER_LEVEL': member_level(request),
    }


def member_level(request):
    """
        Returns the permission level name of a user
            {{MEMBER_LEVEL}} => {Visitor|Member|...}
    """
    from perm.tools import PERMISSION_LEVELS
    if hasattr(request.user, 'permission_level'):
        level = PERMISSION_LEVELS[request.user.permission_level]
    else:
        level = PERMISSION_LEVELS[0]
    return level


def build_tabs(tabs):
    """
        Returns a handy object for use in templates
        View usage:
            context_response(request, template, context, tabs=['example','page'])
        Template usage:
            {% if tabs.home %}// do something
            {% if tabs.edit and tabs.home %}// do else
    """
    if isinstance(tabs, (str, unicode)):
        tabs = [tabs]
    
    class Tab(object):
        def __init__(self, lst):
            self.__list = lst
            for l in lst:
                setattr(self, l, True)
    
    return Tab(tabs)

