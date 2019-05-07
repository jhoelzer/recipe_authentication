"""recipe_forms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""


from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from recipe_authentication.models import Author, Recipes
from recipe_authentication import views

admin.site.register(Author)
admin.site.register(Recipes)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('error/', views.error_view, name='error'),
    path("", views.index, name='homepage'),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('signup/', views.signup_view),
    path('author/<int:author_id>/', views.author_stuff),
    path('recipes/<int:recipe_id>/', views.recipe_stuff),
    path('addrecipe/', views.add_recipe),
    path('addauthor/', views.add_author),
]
