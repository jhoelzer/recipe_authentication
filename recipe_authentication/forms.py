# -*- coding: utf-8 -*-

from django import forms
from recipe_authentication.models import Author

class AuthorsForm(forms.Form):
    name = forms.CharField(max_length=50)
    bio = forms.CharField(widget=forms.Textarea)
    exclude = ["user"]


class RecipesForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=1000)
    time_req = forms.CharField(max_length=25)
    instructions = forms.CharField(widget=forms.Textarea)