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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

'''
Here we define what GELPI (aka L'HOME)
calls 'controllers'. Each user input will go
to a specific 'function' (aka, view) inside the variable request.
Then, the view will 'answer' the user with an HttpResponse,
calling a template.
'''

#----------------------------------------------------------------
# FUNCTIONS
#----------------------------------------------------------------

def search_news(search_term, category):
    news = list()
    sql_query = 'SELECT * FROM search_news_article'

    if len(search_term) > 0:
        search_term = "+" + search_term
        search_term = search_term.replace(" ", " +")
        search_term = search_term.replace("'", "\"")

        sql_query += ' WHERE (MATCH(title) AGAINST(\'%s\' IN BOOLEAN MODE) \
                       OR MATCH(content)   AGAINST(\'%s\' IN BOOLEAN MODE) )' % (search_term, search_term)
        if category != "All":
            sql_query += ' AND category = "%s"' % (category)
    elif category != "All" and len(category) > 0:
        sql_query += ' WHERE category = "%s"' % (category)

    sql_query += ' ORDER BY pubdate DESC'

    for article in Article.objects.raw (sql_query):
        news.append(article)

    return news

def paginate_news(request, news):
    paginator = Paginator(news, 20)
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)

    return news

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
            search_term = form.cleaned_data['sterm']
            category    = form.cleaned_data['categ']

            news = search_news(search_term, category)
            if news:
                count = len(news)
                news  = paginate_news(request, news)
                return render(request, 'search_news/index.html', {'form': form, 'term' : search_term, 'category': category, 'news': news, 'count': count} )
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
