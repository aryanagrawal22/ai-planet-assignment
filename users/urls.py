from django.urls import path
import users.views as views 

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('check_profile', views.check_profile)
]
