from django.db import models


class Type(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=70, blank=False, unique=True)

    def __str__(self):
        return self.name
