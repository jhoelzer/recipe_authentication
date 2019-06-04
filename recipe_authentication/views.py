
# -*- coding: utf-8 -*-

from django.shortcuts import render, reverse, HttpResponseRedirect
from recipe_authentication.models import Recipes, Author
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from recipe_authentication.forms import AuthorsForm, RecipesForm, LoginForm, SignupForm, RecipeEditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required


def index(request):
    html = 'index.html'
    stuff = Recipes.objects.all().order_by('title')
    return render(request, html, {'recipes': stuff})


def recipe_stuff(request, recipe_id):
    html = 'recipe.html'
    stuff = Recipes.objects.all().filter(id=recipe_id)
    recipes = Recipes.objects.get(id=recipe_id)
    current = request.user
    fav_button = None
    show_edit_button = None

    if current.is_authenticated:
        if request.user.author == recipes.author or current.is_staff:
            show_edit_button = True
        if recipes not in current.author.favorites.all():
            fav_button = 'Favorite'
        elif recipes in current.author.favorites.all():
            fav_button = 'Un-Favorite'
    else:
        show_edit_button = False
        return render(request, html, {'recipes': stuff, 'show_edit_button': show_edit_button})

    return render(request, html, {'recipes': stuff, 'fav_button': fav_button, 'show_edit_button': show_edit_button})

@login_required()
def favorite_stat(request, recipe_id):
    html = '../templates/favorite_stat.html'
    is_favorite = False
    current = request.user
    recipe = Recipes.objects.filter(id=recipe_id).first()

    if recipe not in current.author.favorites.get_queryset():
        current.author.favorites.add(recipe)
        is_favorite = True
    else:
        current.author.favorites.remove(recipe)
        is_favorite = False

    current.save()
    return render(request, html, {'is_favorite': is_favorite})


def author_stuff(request, author_id):
    html = "author.html"
    stuff = Recipes.objects.all().filter(id=author_id)
    author = Author.objects.all().filter(id=author_id)
    favorites = author.first().favorites.get_queryset()
    return render(request, html, {'author': author, 'recipes': stuff, 'favorites': favorites})


def signup_view(request):

    html = "signup.html"

    form = None

    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'], 
                data['email'], 
                data['password'])
            login(request, user)
            Author.objects.create(name=user.username, user=user)

            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = SignupForm()
    return render(request, html, {'form': form})
    
        


@login_required()
@staff_member_required()
def add_author(request):
    html = "add_author.html"
    form = None
    if request.method == "POST":
        form = AuthorsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data["username"], data["email"], data["password"])
            login(request, user)
            Author.objects.create(
                name=data["name"],
                bio=data["bio"],
                user=user
            )
            return HttpResponseRedirect(reverse("homepage"))
    else:
        form = AuthorsForm()
    return render(request, html, {"form": form})

    #   if request.user.is_staff:
    #     return render(request, html, {'form': form})
    # elif not request.user.is_staff:
    #     return HttpResponseRedirect(reverse('error'))
    # else:
    #     return HttpResponseRedirect(reverse('homepage'))

    #if staff or superuser you can have all the options(extra credit)
    #if I am not staff I want to be served an error
    #if not logged in I want to be be taken to the log in page


@login_required()
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
                instructions=data["instructions"]
            )
        return render(request, "added_recipe.html")
    else:
        form = RecipesForm()
        
    return render(request, html, {"form": form})


@login_required()
def recipe_edit(request, recipe_id):
    html = 'recipe_edit.html'
    form = None
    current = User.objects.get(id=request.user.author_id)
    current_recipe = Recipe.objects.get(id=recipe_id)
    data = { 'title': current_recipe.title, 'description': current_recipe.description, 'time_req': current_recipe.time_req, 'instructions': current_recipe.instructions}

    if request.method == 'POST':
        form = RecipeEditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            current_recipe.title = data['title']
            current_recipe.description = data['description']
            current_recipe.time_req = data['time_req']
            current_recipe.instructions = data['instructions']
            current_recipe.save()
            return render(request, 'edited.html', {'current_recipe': current_recipe})
    else:
        form = RecipeEditForm(initial=data)
    
    return render(request, html, {'form': form})

def login_view(request):
    html = 'login_view.html'
    form = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', '/'))
    else:
        form = LoginForm()
    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    # output = ('You have been logged out!.')
    # messages.success(request, output)
    return HttpResponseRedirect(reverse('homepage'))


def error_view(request):
    return render(request, 'error.html')
    