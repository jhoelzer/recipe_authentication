
# -*- coding: utf-8 -*-

from django.shortcuts import render
from recipe_authentication.models import Recipes, Author
from django.contrib.auth.models import User
from recipe_authentication.forms import AuthorsForm, RecipesForm

def index(request):
    html = 'index.html'
    stuff = Recipes.objects.all().order_by('title')
    return render(request, html, {'recipes': stuff})

def recipe_stuff(request, recipe_id):
    html = 'recipe.html'
    stuff = Recipes.objects.all().filter(id=recipe_id)
    return render(request, html, {'recipes': stuff})

def author_stuff(request, author_id):
    html = "author.html"
    stuff = Recipes.objects.all().filter(id=author_id)
    author = Author.objects.all().filter(id=author_id)
    return render(request, html, {'author': author, 'recipes': stuff})

def add_recipe(request):
    html = 'add_recipe.html'
    form = None
    if request.method == "POST":
        form = RecipesForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Recipes.objects.create(
                title=data["title"],
                author=data["author"],
                description=data["description"],
                time_req=data["time_req"],
                instructions=data["instructions"],
        )
        return render(request, "added_recipe.html")
    else:
        form = RecipesForm()
    return render(request, html, {"form": form})

def add_author(request):
    html = 'add_author.html'
    form = None
    if request.method == "POST":
        form = AuthorsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create(username=data["name"])
            Author.objects.create(
            name=data["name"],
            bio=data["bio"],
            user=user
        )
        return render(request, "added_author.html")
    else:
        form = AuthorsForm()
    return render(request, html, {"form": form})