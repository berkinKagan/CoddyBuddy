from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("logIn", views.logIn, name="logIn"),
    path("logOut", views.logOut, name="logOut"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("editProfile", views.editProfile, name="editProfile"),
    path("activate<uid>/<token>/", views.activate, name="activate"),
    path("changePassword", views.changePassword, name="changePassword"),
    path("confirmPsw<uid>/<token>/", views.confirmPsw, name="confirmPsw"),
    path("createPost", views.createPost, name="createPost"),
    path("createNotification/<str:pk>", views.createNotification, name="createNotification"),
    
]
