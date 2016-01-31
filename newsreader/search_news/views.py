#----------------------------------------------------------------
# MODULES
#----------------------------------------------------------------
from django.shortcuts import render
from .forms import SearchForm
from .models import Article
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf

'''
Here we define what GELPI (aka L'HOME)
calls 'controllers'. Each user input will go
to a specific 'function' (aka, view) inside the variable request.
Then, the view will 'answer' the user with an HttpResponse,
calling a template.
'''

#----------------------------------------------------------------
# VIEWS
#----------------------------------------------------------------
'''
INDEX VIEW: Here we have all the pages in which there are news displayed.
    PROBLEMS: The logic of this functions is completely crap
              Someone fix it pls
'''
def index_view(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            # Get what the user wrote:
            search_term = form.cleaned_data['sterm']
            category    = form.cleaned_data['categ']
            news = list()


            sql_query = 'SELECT * FROM search_news_article'

            if len(search_term) > 0:
                sql_query += ' WHERE (MATCH(title) AGAINST("%s") \
                              OR MATCH(content) AGAINST("%s") )' % (search_term, search_term)
                if category != "All":
                    sql_query += ' AND category = "%s"' % (category)
            elif category != "All" and len(category) > 0:
                sql_query += ' WHERE category = "%s"' % (category)

            sql_query += ' ORDER BY pubdate DESC'

            for article in Article.objects.raw (sql_query):
            	news.append(article)

            if news:
                return render(request, 'search_news/index.html', {'form': form, 'term' : search_term, 'category': category, 'news': news} )
            else:
                error = "No results for %s in category %s" % (search_term, category)
                return render(request, 'search_news/index.html', {'form': form, 'error': error} )
    else:
        form = SearchForm()

    return render(request, 'search_news/index.html', {'content': string, 'form': form})




def register(request):
     if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             return HttpResponseRedirect('/accounts/register/complete')
     else:
         form = UserCreationForm()
     token = {}
     token.update(csrf(request))
     token['form'] = form

     return render_to_response('registration/registration_form.html', token)

def registration_complete(request):
     return render_to_response('registration/registration_complete.html')

def loggedin(request):
    return render_to_response('registration/loggedin.html',
                              {'username': request.user.username})
