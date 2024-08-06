from django.urls import path
from .views import MyObtainTokenPairView,Registeruser,Userlogout,Userdetails,MoviesCreate,Genrelist,Movieslistuserwise,MovieDetails,MoviesUpdate,MoviesDelete,ApprovedMovielist,Genredetails,Moviedetailslist,ReviewsListCreate,ReviewsList,Usersupdate
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("userdetails/<int:pk>/", Userdetails.as_view(), name='userdetails'),
    path("profileupdate/<int:pk>/",Usersupdate.as_view(),name="profileupdate"),
    path('register/',Registeruser.as_view(), name='register'),
    path('moviecreate/',MoviesCreate.as_view(),name='moviecreate'),
    path("usermovies/",Movieslistuserwise.as_view(), name="usermovies"),
    path("approvalmovies/",ApprovedMovielist.as_view(),name="approvalmovies"),

    path("moviedetails/<int:pk>/",MovieDetails.as_view(), name="moviedetails"),
    path("moviedetaillist/<int:pk>/",Moviedetailslist.as_view(), name="moviedetaillist"),
    path("moviesupdate/<int:pk>/",MoviesUpdate.as_view(), name='booksupdate'),
    path("moviesdelete/<int:pk>/",MoviesDelete.as_view(), name='moviesdelete'),
    path('genrelist/',Genrelist.as_view(),name='genrelist'),
    path('movies/<int:movie_id>/reviews/user/<int:user_id>/',ReviewsListCreate.as_view(),name='moviereviews'),
    path('reviewslist/',ReviewsList.as_view(),name='reviewslist'),
    path('genredetail/<int:pk>',Genredetails.as_view(), name='genredetail'),
    path('logout/',Userlogout.as_view(),name='userlogout')
]
