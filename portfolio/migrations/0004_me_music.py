# Generated by Django 3.1 on 2022-05-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_events_me'),
    ]

    operations = [
        migrations.AddField(
            model_name='me',
            name='music',
            field=models.FileField(default='', upload_to='portfolio/static/portfolio/assets/'),
        ),
    ]
