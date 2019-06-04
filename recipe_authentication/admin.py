from django.contrib import admin
from recipe_authentication.models import Author, Recipes


admin.site.register(Author)
admin.site.register(Recipes)
