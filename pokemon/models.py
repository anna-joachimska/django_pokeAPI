from django.db import models


class Pokemon(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=70, blank=False, unique=True)
    types = models.ManyToManyField('type.Type', blank=True)
    abilities = models.ManyToManyField('ability.Ability', blank=True)
    hp = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    generation = models.CharField(max_length=70, blank=False)

    def __str__(self):
        return self.name
