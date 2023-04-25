from django.urls import path
import users.views as views 

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('check_profile', views.check_profile),
    path('get_one_reg_user', views.get_atleast_one_registered_users)
]
