 #-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField('Recipes', related_name='favorites', symmetrical=False, blank=True)

    def __str__(self):
        return self.name

    
class Recipes(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    time_req = models.CharField(max_length=50)
    instructions = models.TextField()

    def __str__(self):
        return self.title
