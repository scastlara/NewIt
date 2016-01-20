from django import forms

'''
This file has the info needed to create web forms
'''

class NameForm(forms.Form):
    sterm = forms.CharField(label='Your name', max_length=100)
