from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
    path("genrelist",views.Genrelist,name="genrelist"),
    path("creategenre/",views.Creategenre,name="creategenre"),
    path("editgenre/<int:genre_id>/", views.Editgenre,name="editgenre"),
    path("deletegenre/<int:genre_id>/", views.Deletegenre,name="deletegenre"),


    path("movieslist/",views.listmovies,name="movieslist"),
    path("createmovies/",views.createmovies,name="createmovies"),
    path("editmovies/<int:movie_id>/", views.Editmovies,name="editmovies"),
    path("deletemovies/<int:movie_id>/", views.Deletemovies,name="deletemovies"),
]

