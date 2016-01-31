from django import forms
from search_news.models import Category

'''
This file has the info needed to create web forms
'''


'''
This implementation is awful. We are reading a static file that is a mirror of a file
located in bin/. No way we are going to be famous with this implementation.

A better approach would be to do a query to the MySQL database using Django models
and add to the set_of_cat all the categories found in the DB table 'Category'.
Someone do it PLS.
'''

def get_categories():
    set_of_cat = set()
    all_categories = list(Category.objects.values_list('category'))
    for cat in all_categories:
        set_of_cat.add(cat[0])
    set_of_cat.add("All")

    list_of_cats = list()
    for element in set_of_cat:
        view_choice = element.lower()
        view_choice = view_choice.title()
        list_of_cats.append((element, view_choice))

    return(sorted(list_of_cats))

class SearchForm(forms.Form):
    sterm = forms.CharField(label='', max_length=100, required=False)
    categ = forms.ChoiceField(label='', choices=get_categories(), required=False)
