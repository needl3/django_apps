# Generated by Django 3.1 on 2022-05-07 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='tools',
            field=models.CharField(default='', max_length=300),
        ),
    ]