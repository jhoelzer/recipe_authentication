
# -*- coding: utf-8 -*-

from django.shortcuts import render, reverse, HttpResponseRedirect
from recipe_authentication.models import Recipes, Author
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from recipe_authentication.forms import AuthorsForm, RecipesForm, LoginForm, SignupForm
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
    return render(request, html, {'recipes': stuff})


def author_stuff(request, author_id):
    html = "author.html"
    stuff = Recipes.objects.all().filter(id=author_id)
    author = Author.objects.all().filter(id=author_id)
    return render(request, html, {'author': author, 'recipes': stuff})


# def signup_view(request):

#     html = "signup.html"

#     form = SignupForm(None or request.POST)
#     if form.is_valid():
#         data = form.cleaned_data
#         user = User.objects.create_user(
#             data['username'], 
#             data['email'], 
#             data['password'])
#         login(request, user)
#         Author.objects.create(name=user.username, user=user)

#         return HttpResponseRedirect(reverse('homepage'))
    
        


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
    