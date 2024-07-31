from django.conf import settings
from django.urls import path

from . import views


urlpatterns = [
     path("",views.adminlogin,name="adminlogin"),
     path("admindashboard",views.admindashboard,name="admindashboard"),
     path("userslist/",views.Userslist,name="userslist"),
     path("createusers/",views.Createusers,name="createusers"),
     path("editusers/<int:user_id>/", views.Editusers,name="editusers"),
     path("deleteusers/<int:user_id>/", views.Deleteusers,name="deleteusers"),
     path("adminlogout/", views.Adminlogout, name="adminlogout"),
]

