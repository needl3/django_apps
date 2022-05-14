from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Video)
admin.site.register(models.Recents)
admin.site.register(models.NewReleases)
admin.site.register(models.Recommended)
admin.site.register(models.Hot)
admin.site.register(models.Popular)