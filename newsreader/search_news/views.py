#----------------------------------------------------------------
# MODULES
#----------------------------------------------------------------
from django.shortcuts import render
from django.http import Http404
from .forms import SearchForm
from .models import Article
from .models import Search_Subscription
from .models import Source
from .models import Bookmark ###
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

def search_news(search_term, category, diario):
    news = list()
    sql_query = 'SELECT * FROM search_news_article'


    if len(search_term) > 0:
        search_term = "+" + search_term
        search_term = search_term.replace(" ", " +")
        search_term = search_term.replace("'", "\"")

        sql_query += ' WHERE (MATCH(title) AGAINST(\'%s\' IN BOOLEAN MODE) \
                       OR MATCH(content)   AGAINST(\'%s\' IN BOOLEAN MODE) )' % (search_term, search_term)
        if category != "":
            sql_query += ' AND category = "%s"' % (category)

        if diario != None:
            sql_query += ' AND source = "%s"' % (diario)

    elif category != "" and len(category) > 0:

        sql_query += ' WHERE category = "%s"' % (category)
        if diario != None:
            sql_query += ' AND source = "%s"' % (diario)

    elif diario != None:
            sql_query += ' WHERE source = "%s"' % (diario)


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


def get_user_subscriptions(user):
    subscriptions = None
    try:
        subscriptions = Search_Subscription.objects.filter(
            username = user
        )
    except:
        subscriptions = False
    return subscriptions

#----------------------------------------------------------------
# VIEWS
#----------------------------------------------------------------
'''
INDEX VIEW: Here we have all the pages in which there are news displayed.
    PROBLEMS: The logic of this functions is completely crap
              Someone fix it pls
'''
def index_view(request, diario=None):
    subscriptions = None
    if request.user.is_authenticated():
        subscriptions = get_user_subscriptions(request.user.username)

    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term   = form.cleaned_data['sterm']
            category      = form.cleaned_data['categ']
            is_subs       = None
            if request.user.is_authenticated():
                # Check if user is subscribed to this search!
                try:
                    sub = Search_Subscription.objects.get(
                        username = request.user.username,
                        keyword  = search_term,
                        category = category
                    )
                    is_subs = True
                except:
                    is_subs = False

            if diario != None:
                try:
                    sub = Source.objects.get(
                    name = diario
                    )
                except Exception as m:
                    return render(request, 'search_news/error404.html') 

            news = search_news(search_term, category, diario)
            if news:
                count = len(news)
                news  = paginate_news(request, news)
                return render(request, 'search_news/index.html', {'term'    : search_term, 'diario'        : diario,
                                                                  'category': category,    'news'          : news,
                                                                  'count'   : count,       'subscriptions' : subscriptions,
                                                                  'is_subs' : is_subs,   } )
            else:
                error = "No results for %s in category %s" % (search_term, category)
                return render(request, 'search_news/index.html', {'error': error} )
    else:
        form = SearchForm()

    return render(request, 'search_news/index.html', )


def subscribed(request):
    username = None
    if request.method == "POST" and request.user.is_authenticated():
        username = request.user.username
        if "sub" in request.POST:
            sterm    = request.POST.get("sub_sterm", "")
            category = request.POST.get("sub_category", "")
            subscription = Search_Subscription(username=username, keyword=sterm, category=category)
            subscription.save()
            return render(request, 'search_news/subscribed.html', {'sterm': sterm, 'category': category })


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


def user_subscriptions(request):
    msg = ""
    subscriptions = ""
    if request.user.is_authenticated():
        subscriptions = get_user_subscriptions(request.user.username)
    if request.method == "POST":
        for sub, value in request.POST.items():
            if not sub.startswith('s_'):
                continue
            else:
                if value == "1":
                    continue
                msg = "Changes saved."
                elements = sub[2:].split("||") # starts from [2:] to omit "s_"
                sterm    = elements[0]
                category = elements[1]
                Search_Subscription.objects.filter(
                    username=request.user.username,
                    keyword=sterm,
                    category=category
                ).delete()
    return render(request, 'search_news/user_search.html', {'subscriptions': subscriptions, 'message': msg })


def user_bookmarks(request):
    username = 'kk'
    if request.user.is_authenticated():
        bookmarked = Bookmark.objects.filter(username=request.user.username

        )
        string = 'ta pata madra'
        return render(request, 'search_news/user_bookmarks.html',{'username' : username,
                                                                  'string': string,
                                                                  'bookmarked': bookmarked
                                                                })

     