#--------
# MODULES
#--------
from django.shortcuts import render
from .forms import SearchForm
from .models import Articles

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

    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            # Get what the user wrote:
            search_term = form.cleaned_data['sterm']
            news = []
            if len(search_term) > 0:
                for p in Articles.objects.raw (' SELECT * FROM search_news_articles '):               
                	news.append(p.title) ### AQUI ES ON ESTIC! PRINTA L'ULTIM! CAL FER UN APPEND!

            # Here we would do magic (MySQL search) and we will return something that will go to
            # the template =D
            return render(request, 'search_news/index.html', {'form': form, 'content': string, 'news': news,	 'term' : search_term} )

    else:
        form = SearchForm()

    return render(request, 'search_news/index.html', {'content': string, 'form': form})
