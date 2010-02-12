from django.conf import settings as conf

def settings(request):
    return {
        'FB_API_KEY': conf.FACEBOOK_API_KEY,
    }