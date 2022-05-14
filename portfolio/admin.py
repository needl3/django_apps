from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Projects)
admin.site.register(models.Me)
admin.site.register(models.Events)