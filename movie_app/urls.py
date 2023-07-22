from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_all_movie),
    path('movie/<slug:slug_movie>', views.show_one_movie, name='movie-detail'),
    path('director/<slug:slug_director>', views.show_one_director, name='director-detail'),
    path('director/', views.show_all_directors, name='all-director')


]


