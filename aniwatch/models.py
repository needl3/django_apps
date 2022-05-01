from django.db import models

class Video(models.Model):
    name = models.CharField(max_length=30)
    image_link = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    summary = models.TextField()
    genre = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    episodes = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Recents(models.Model):
    name = models.CharField(max_length=300, default="")
    def __str__(self):
        return 'Recents Anime Table'

class Trending(models.Model):
    name = models.CharField(max_length=300, default="")
    def __str__(self):
        return 'Trending Anime Table'

class Recommended(models.Model):
    name = models.CharField(max_length=300, default="")
    def __str__(self):
        return 'Recommended Anime Table'