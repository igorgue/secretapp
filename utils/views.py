from utils.shortcuts import context_response
import environment

def home(request):
    "Landing page to site. Much more to come..."
    # TODO: everything
    context = {'facebook_key': environment.FACEBOOK_API_KEY }
    return context_response(request, 'utils/home.html', context)
