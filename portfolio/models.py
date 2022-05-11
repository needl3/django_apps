from django.db import models
import uuid

# Create your models here.
class Me(models.Model):
    name=models.CharField(max_length=100, default='Anish Chapagai')

    # This image link will contain 3 image links seperated by commas
    # Can't make it list here because default python list type is not supported
    # So will make list in views by splitting
    image_link = models.TextField(default="")

    def __str__(self):
        return self.name

class Projects(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    priority = models.IntegerField(default=uuid.uuid1)
    tools = models.CharField(max_length=300, default="")
    description = models.TextField(default="")
    image = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.name

class Events(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    description = models.TextField(default="")
    image_link = models.CharField(max_length=300, default="")
    def __str__(self):
        return self.name