from utils.shortcuts import context_response

def login(request):
    user = request.user
    
    if request.method == 'POST':
        return context_response(request, 'facebook/login.html', {'test': 'test' })

