from django.urls import include, path
from . import views

app_name = 'portfolio'
urlpatterns = [
    path('', views.index, name='index'),
]