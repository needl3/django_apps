from django.db import models
import uuid

class Video(models.Model):
    name = models.CharField(max_length=200, unique=True, default=uuid.uuid1)
    image_link = models.CharField(max_length=200, default="#")
    url = models.CharField(max_length=200, default="#")
    summary = models.TextField(default="")
    genre = models.CharField(max_length=200, default="")
    status = models.CharField(max_length=100, default="")
    episodes = models.IntegerField(default=1)
    released = models.IntegerField(default=1)
    anime_type = models.CharField(max_length=100, default="")
    def __str__(self):
        return self.name

class Recents(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    def __str__(self):
        return self.name

class NewReleases(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    last_ep = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Recommended(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    def __str__(self):
        return self.name
class Hot(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    def __str__(self):
        return self.name
class Popular(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    def __str__(self):
        return self.name
