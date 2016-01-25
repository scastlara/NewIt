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
            category    = form.cleaned_data['categ']
            news = list()


            sql_query = 'SELECT * FROM search_news_articles'

            if len(search_term) > 0:
                sql_query += ' WHERE (MATCH(title) AGAINST("%s") \
                              OR MATCH(content) AGAINST("%s") )' % (search_term, search_term)
                if category != "All":
                    sql_query += ' AND category = "%s"' % (category)
            elif category != "All":
                sql_query += ' WHERE category = "%s"' % (category)

            for article in Articles.objects.raw (sql_query):
            	news.append(article.title)

            # Here we would do magic (MySQL search) and we will return something that will go to
            # the template =D
            return render(request, 'search_news/index.html', {'form': form, 'content': sql_query, 'news': news, 'term' : search_term} )

    else:
        form = SearchForm()

    return render(request, 'search_news/index.html', {'content': string, 'form': form})
