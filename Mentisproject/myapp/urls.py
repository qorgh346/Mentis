from os import name
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('temp/',views.temp,name='temp'), #호비 로그인하기.
    path('mypage/',views.mypage,name='mypage'),

]