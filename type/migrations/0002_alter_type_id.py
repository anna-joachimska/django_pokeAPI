# Generated by Django 4.1.7 on 2023-02-23 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('type', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='type',
            name='id',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]
