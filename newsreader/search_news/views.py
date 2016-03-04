#----------------------------------------------------------------
# MODULES
#----------------------------------------------------------------
from django.shortcuts import render
from django.http import Http404
from .forms import SearchForm
from .models import Article
from .models import Search_Subscription
from .models import Source
from .models import Source_Subscription
from .models import Bookmark ###
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import (
    PasswordChangeForm, PasswordResetForm
)
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, update_session_auth_hash,
)


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

def search_news(search_term, category, diario, black_names):
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
        elif black_names:
            for black in black_names:
                sql_query += ' AND NOT source = "%s"' % (black)


    elif category != "" and len(category) > 0:

        sql_query += ' WHERE category = "%s"' % (category)
        if diario != None:
            sql_query += ' AND source = "%s"' % (diario)
        elif black_names:
            for black in black_names:
                sql_query += ' AND NOT source = "%s"' % (black)

    elif diario != None:
            sql_query += ' WHERE source = "%s"' % (diario)
    elif black_names:
        sql_query += ' WHERE NOT source = "%s"  ' % black_names[0]
        for black in black_names[1:]:
            sql_query += ' AND NOT source = "%s"' % (black)


    sql_query += ' ORDER BY pubdate DESC'

    for article in Article.objects.raw (sql_query):
        news.append(article)



    return news

def paginate_news(request, news):
    paginator = Paginator(news, 15)
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

def get_feeds():
    feeds = Source.objects.all()
    return feeds

def get_black_list(user):
    black_list = None
    black_names = list()
    black_list = Source_Subscription.objects.filter(username = user)
    if black_list:
        # We don't want some feeds
        for black in black_list:
            black_names.append(black.source)

    return black_names



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
    black_list    = None
    black_names   = list()
    feeds         = get_feeds()
    bookmarks     = list()

    if request.user.is_authenticated():
        subscriptions = get_user_subscriptions(request.user.username)
        black_names = get_black_list(request.user.username)
        bookmark_rows = Bookmark.objects.filter(
            username = request.user.username
        )
        if bookmark_rows:
            for book_row in bookmark_rows:
                bookmarks.append(book_row.article)





    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search_term   = form.cleaned_data['sterm']
            category      = form.cleaned_data['categ']

            if category == "Todo":
                category = ""

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

            diario_row = None
            if diario is not None:
                try:
                    diario_row = Source.objects.get(
                        name = diario
                    )
                except Exception as m:
                    return render(request, 'search_news/error404.html')

            news = search_news(search_term, category, diario, black_names)
            if news:
                count = len(news)
                news  = paginate_news(request, news)
                return render(request, 'search_news/index.html', {'term'    : search_term, 'diario'        : diario,
                                                                  'category': category,    'news'          : news,
                                                                  'count'   : count,       'subscriptions' : subscriptions,
                                                                  'is_subs' : is_subs,     'request'       : request,
                                                                  'feeds'   : feeds,       "black_list"    : black_names,
                                                                  'bookmarks': bookmarks,  'diario_row'    : diario_row}  )
            else:
                error = "No results for %s in category %s" % (search_term, category)
                return render(request, 'search_news/index.html', {'error': error} )
        else:
            return render(request, 'search_news/error404.html')
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
    else:
        return render(request, 'search_news/error404.html')

def unsubscribed(request):
    username = None
    if request.method == "POST" and request.user.is_authenticated():
        username = request.user.username
        if "unsub" in request.POST:
            sterm    = request.POST.get("sub_sterm", "")
            category = request.POST.get("sub_category", "")
            Search_Subscription.objects.filter(
                username=username,
                keyword=sterm,
                category=category
            ).delete()
            return render(request, 'search_news/unsubscribed.html', {'sterm': sterm, 'category': category })
    else:
        return render(request, 'search_news/error404.html')


def register(request):
     if request.method == 'POST':
         form = UserCreationForm(request.POST)
         if form.is_valid():
             form.save()
             return render(request, 'registration/registration_complete.html')
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
    feeds = list()
    black_names = list()
    if request.user.is_authenticated():
        subscriptions = get_user_subscriptions(request.user.username)
        feeds = get_feeds()
        black_names = get_black_list(request.user.username)

    else:
        return render(request, 'search_news/error404.html')

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
    return render(request, 'search_news/user_search.html', {'subscriptions': subscriptions, 'message': msg, 'feeds':feeds, 'black_list':black_names})

def feed_subscriptions(request):
    black_list  = ""
    black_names = list() # List of sources in black list
    all_feeds  = ""

    if request.user.is_authenticated():
        subscriptions = get_user_subscriptions(request.user.username)
        if request.method == "POST":
            for feed, value in request.POST.items():
                if not feed.startswith('s_'):
                    continue
                else:
                    source = feed[2:]
                    if value == "1":
                        # Remove from black list if exists
                        msg = source
                        Source_Subscription.objects.filter(
                            username = request.user.username,
                            source   = source
                            ).delete()

                    else:
                        # Add to black list if it doesn't exist
                        Source_Subscription.objects.get_or_create(
                            username = request.user.username,
                            source   = source
                        )

        # Get user feed subscriptions

        feeds = get_feeds()
        black_names = get_black_list(request.user.username)

    else:
        return render(request, 'search_news/error404.html')

    return render(request, 'search_news/feed_subscriptions.html', {'black_list': black_names,
                                                                   'feeds': feeds, 'subscriptions': subscriptions})


def user_bookmarks(request):
    if request.user.is_authenticated():
        subscriptions = get_user_subscriptions(request.user.username)
        feeds = get_feeds()
        black_names = get_black_list(request.user.username)

        if request.method == "POST":
            for article, value in request.POST.items():
                if not article.startswith('s_'):
                    continue
                else:
                    url = article[2:]
                    if value == "0":
                        Bookmark.objects.filter(
                            username = request.user.username,
                            article = url
                        ).delete()
        bookmarked = Bookmark.objects.filter(username=request.user.username)


        user_articles = list()

        if bookmarked:
            for row in bookmarked:
                name = Article.objects.filter(link = row.article)
                if name:
                    user_articles.append(name)
        return render(request, 'search_news/user_bookmarks.html',{'user_articles': user_articles,'subscriptions':subscriptions, 'feeds':feeds, 'black_list':black_names})


    else:
        return render(request, 'search_news/error404.html')


def user_booked(request):
    if request.user.is_authenticated():
        if request.is_ajax() or request.method == 'POST':
            for name, url in request.POST.items():
                if name != "name":
                    continue
                try:
                    # Try to get the article
                    book = Bookmark.objects.get(
                        username = request.user.username,
                        article  = url
                    )
                    # Delete it if it exists
                    book.delete()

                    # Get it again (is it bookmarked by someone else?)
                    try:
                        book_after = Bookmark.objects.get(article = url)
                    except:
                        # No one has it, set to False
                        art = Article.objects.get(link = url)
                        art.bookmarked = False
                        art.save()

                except:
                    # Create bookmark for user
                    Bookmark.objects.get_or_create(
                        username = request.user.username,
                        article  = url
                    )
                    # Set article as bookmarked by someone
                    article = Article.objects.get(link = url)
                    article.bookmarked = True
                    article.save()

            return render(request, 'search_news/user_booked.html',{
                                                               'url' : url
                                                              })
    else:
        return render(request, 'search_news/error404.html')



def handler404(request):
    return render(request, 'search_news/error404.html')


def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        print("REQUEST IS POST")
        if form.is_valid():
            print ("FORM IS VALID")
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return render(request, 'registration/password_change_done.html')
        else:
            print("FORM NOT VALID")
    else:
        print("NOT POST!")
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
