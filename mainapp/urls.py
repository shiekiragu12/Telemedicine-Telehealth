from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
    path("schedule-a-call", call_schedule, name="call_schedule"),
    path("blogs/", blogs, name="blogs"),
    path("blogs/<str:blog_id>/<str:slug>/", single_blog, name="single_blog"),
    path("blogs/<str:blog_id>/", blog_reply, name="blog_reply"),
    path("doctors/search/", doctor_search, name="doctor_search"),
    path("doctors/view/<str:doctor_id>/", single_doctor, name="single-doctor"),

    path('404/', page_not_found, name='page-not-found'),
    path('500/', internal_server_error, name='internal-server-error'),
]
