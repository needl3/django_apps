from django.db import models
import uuid

# Create your models here.
class Projects(models.Model):
    name = models.CharField(max_length=300, unique=True, default=uuid.uuid1)
    priority = models.IntegerField(default=uuid.uuid1)
    tools = models.CharField(max_length=300, default="")
    description = models.TextField(default="")
    image = models.CharField(max_length=200, default="")
    link = models.CharField(max_length=200, default="")
    def __str__(self):
        return self.name
