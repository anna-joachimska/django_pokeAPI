# Generated by Django 4.1.7 on 2023-02-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ability', '0001_initial'),
        ('pokemon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ability',
            name='pokemons',
            field=models.ManyToManyField(blank=True, to='pokemon.pokemon'),
        ),
    ]
