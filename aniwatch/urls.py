from django.urls import include, path
from . import views

app_name = 'aniwatch'
urlpatterns = [
    path('', views.index, name='index'),
    path('anime/<str:anime_url>/', views.anime, name='anime'),
    path('anime/<str:anime_url>/<int:episode>', views.anime, name='anime_play'),
    path('query', views.query, name='query'),
    path('upload/', views.MovieUpload.as_view(), name='upload'),

    # Navbar calls
    path('ongoing/', views.ongoing, name='ongoing'),
    path('recently-popular/', views.popular, name='recently-popular'),
    path('hot/', views.hot, name='hot'),
    path('genres/', views.genres, name='genres'),

]