# Generated by Django 2.2.1 on 2019-06-04 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='favorites',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='recipe_authentication.Recipes'),
        ),
    ]