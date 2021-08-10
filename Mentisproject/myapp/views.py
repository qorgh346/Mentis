from django.shortcuts import render
from .models import User_info,Menti_info
from mentoringapp.models import FavouriteLecture,Mentor_info
# Create your views here.

def index(request):
    return render(request, "index.html")

def mypage(request):
    data = {}
    user_temp = request.session.get('temp') # 'tony346'
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp) 
    print(user.pk)
    menti =  Menti_info.objects.get(user_info_id = user.pk)
    print(menti)
    fav = FavouriteLecture.objects.filter(user_id=menti.pk)
    print(fav)
   
    data['user'] = user
    data['favLec'] = fav    
    #print(favLecture[1].user_id)
    return render(request,"mypage.html",data)


def temp(request):
    request.session['temp'] = 'tony'
    print('임시 로그인 성공')
    return render(request,"index.html")