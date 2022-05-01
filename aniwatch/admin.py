from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Video)
admin.site.register(models.Recents)
admin.site.register(models.Trending)
admin.site.register(models.Recommended)