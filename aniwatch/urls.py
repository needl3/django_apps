from django.urls import include, path
from . import views

app_name = 'aniwatch'
urlpatterns = [
    path('', views.index, name='index'),
    path('anime/<str:anime_name>/', views.anime, name='anime'),
    path('anime/<str:anime_name>/<int:episode>', views.animePlayer, name='anime_play'),
    path('query', views.query, name='query'),
    path('upload/', views.MovieUpload.as_view(), name='upload'),
]