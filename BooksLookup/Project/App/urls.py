from django.urls import path
from App.views import hello,Search
urlpatterns = [
    path('hello/',hello),
    path('',Search)
]
