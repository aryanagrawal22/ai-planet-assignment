from django.urls import path
import submissions.views as views 

urlpatterns = [
    path('create_submission', views.create_submission),
    path('get_submissions', views.get_submissions),
]
