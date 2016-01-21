from django import forms

'''
This file has the info needed to create web forms
'''

class SearchForm(forms.Form):
    sterm = forms.CharField(label='', max_length=100)
