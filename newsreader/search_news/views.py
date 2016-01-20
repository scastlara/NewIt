#--------
# MODULES
#--------
from django.shortcuts import render
# from .models import Post
# from .forms import PostFor

'''
Here we define what GELPI (aka L'HOME)
calls 'controllers'. Each user input will go
to a specific 'function' (aka, view) inside the variable request.
Then, the view will 'answer' the user with an HttpResponse,
calling a template
'''

#--------
# VIEWS
#--------

def index_view(request):
    string = "Esto es content que viene de index_view() en views.py y se envía a la template base.html"
    return render(request, 'search_news/index.html', {'content': string})
