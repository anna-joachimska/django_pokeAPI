# Generated by Django 4.1.7 on 2023-02-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pokemon', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=70, unique=True)),
                ('pokemons', models.ManyToManyField(blank=True, to='pokemon.pokemon')),
            ],
        ),
    ]
