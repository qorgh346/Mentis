from django.urls import path
from . import views
urlpatterns = [
    path('mentoring', views.mentoring, name='mentoring'),
]