from django.urls import path
import hackathons.views as views 

urlpatterns = [
    path('create', views.create),
    path('get_hackathons', views.get_hackathons),
    path('hackathon_register', views.hackathon_register),
    path('get_registered_hackathons', views.get_registered_hackathons),
]
