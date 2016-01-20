#--------
# MODULES
#--------
from django.shortcuts import render
from .forms import NameForm

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

    if request.method == "POST":
        form = NameForm(request.POST)
        if form.is_valid():
            # Here we would do the mySQL search
            return render(request, 'search_news/index.html', {'form': form, 'content': "has buscado algo", 'term' : form.cleaned_data["sterm"]} )
    else:
        form = NameForm()

    return render(request, 'search_news/index.html', {'content': string, 'form': form})
