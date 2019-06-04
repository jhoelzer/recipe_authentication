# -*- coding: utf-8 -*-

from django import forms
from recipe_authentication.models import Author


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    

class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


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


class RecipeEditForm(forms.Form):
    title = forms.CharField(max_length=50)
    author = forms.ModelChoiceField(queryset=Author.objects.all())
    description = forms.CharField(max_length=1000)
    time_req = forms.CharField(max_length=25)
    instructions = forms.CharField(widget=forms.Textarea)
