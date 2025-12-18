from django.urls import path
from . import views

urlpatterns = [
    path('view-songs', views.view_songs, name='main'),
    path('api/songs/', views.songs_api, name='songs_api')
]
