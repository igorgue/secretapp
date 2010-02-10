#from discussion.models import Discussion
from utils.shortcuts import context_response
#from forms import *
#from models import *

def login(request):
    user = request.user
    
    if request.method == 'POST':
        return context_response(request, 'facebook/login.html', {'test': 'test' })
    # TODO (GET): whoops

