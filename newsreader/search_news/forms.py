from django import forms
import os

'''
This file has the info needed to create web forms
'''
def get_categories():
    script_path = os.path.abspath(__file__)
    script_path = script_path.replace("forms.py", "")
    path = script_path + "static/feeds.tbl"
    file = open(path, "r")
    set_of_cat = set()
    for line in file:
        line     = line.strip()
        elements = line.split()
        set_of_cat.add(elements[1])

    # Add All choice
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
