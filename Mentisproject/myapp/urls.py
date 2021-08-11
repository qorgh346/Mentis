from os import name
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('temp/',views.temp,name='temp'), #호비 로그인하기.
    path('mypage/',views.mypage,name='mypage'),
    path('mypage/update',views.mypage_update,name='mypage_update'),
    path('cash/',views.cash,name='cash'),
    path('mypage/certification/',views.certification,name='certification'),
    path('mypage/certification/view/',views.profile,name='profile'),
    path('mypage/mylecture/',views.mylecture,name='mylecture'),
    path('mypage/class_upload',views.class_upload,name='class_upload'),

    path('mypage/class_view',views.class_view,name='class_view'),


]