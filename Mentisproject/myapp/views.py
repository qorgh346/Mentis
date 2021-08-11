from django.shortcuts import redirect, render,HttpResponse
from .models import User_info,Menti_info,Cash
from mentoringapp.models import FavouriteLecture,Mentor_info,LectureList
from django.urls import reverse
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

def cash(request):
    data = {}
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('temp') # 'tony'
    user = User_info.objects.get(user_id=user_temp) 

    if request.method == "POST":
        try:
            cash_money = request.POST.get('cash') #충전 할 금액
            #캐시 DB에 저장
            myCash = Cash(payer=user.user_name, user_id = user,
                                cash_charge = cash_money
                                )
            myCash.save()
            return HttpResponse('충전신청이 완료 되었습니다.')    
        except:
            #캐시 DB를 ManyToMany로 바꿔서 여러번 충전이 가능하도록 해야되지 않나욤?
            #현재는 한번 들어가면 못들어가게 설정.
            #아니면 충전 신청이 완료되서 입금을 확인 후 --> DB를 지우는 방법도 있음 ( 추천^^)
            return HttpResponse('충전 대기중입니다.')
    else:
        data['user'] = user
        return render(request,"cash.html",data)


def certification(request):
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('temp') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)
    
    if request.method == "POST": #인증서를 추가하고 다 놓은것
        try:
            user.user_certification=request.FILES['image']
        except: #이미지가 없어도 그냥 지나가도록-!
            return HttpResponse('파일이 없습니다...')
        user.save()
    else: #GET으로 들어올 때
        if user.user_certification_check: #인증이 완료된 경우에는 인증서를 보여주기.
                return HttpResponse('인증이 완료되었습니다.')
        else: #인증이 완료가 안 된 경우에는 --> 인증서를 추가할 수 있는 기능
                return render(request,'certification.html')

    return render(request,'certification.html')

def profile(request):
    #로그인 한 사용자를 가져오기
    user_temp = request.session.get('temp') # 'tony346'
    user = User_info.objects.get(user_id=user_temp)
    print('profi')
    return render(request,'certification_check.html',{'profile':user})

def certification_create(request):
    pass

def mypage_update(request):
    if request.method == "POST": #변경 버튼을 눌렀을 때
        #로그인 한 사용자를 가져오기
        user_temp = request.session.get('temp') # 'tony346'
        user = User_info.objects.get(user_id=user_temp)
        
        try:
            # user.user_name = request.POST.get('name')
            user.user_email = request.POST.get('email')
            user.user_phone_number = request.POST.get('phoneNumber')
            user.user_certification = request.FILES['image']
        except:
            return HttpResponse('폼 에러 입니다.')
        user.save() #변경ㅋ
    else:
        return render(request,'myinfo_up.html')
    return redirect(reverse('mypage'))
    

def mylecture(request): # My강의
    data = {}
    user_temp = request.session.get('temp') # 'tony'
    print(user_temp)
    user = User_info.objects.get(user_id=user_temp) 
    print(user.pk)
    menti = Menti_info.objects.get(user_info_id = user.pk)
    print(menti.pk)
    myLec = LectureList.objects.filter(user_id = menti.pk)
    print(myLec)
    
    data['user'] = user
    data['myLec'] = myLec

    return render(request,"myclass.html",data)





# def dummy(request):
#     data = {}
#     #로그인 한 사람이 누구인제 체크 ( 예외처리는 아직. )
#     user_temp = request.session.get('temp') # 'tony346' -> 

#     user = User_info.objects.get(user_id=user_temp) 

#     menti =  Menti_info.objects.get(user_info_id = user.pk)
#     #그 사람이 신청한 수강을 가져온다.
#     myLectureList =  LectureList.objects.filter(user_id = menti.pk)
#     sum = 0
#     #신청한 수강들의 price를 가져온다.
#     for lecture in myLectureList:
#         sum += lecture.price
#     print('sum = ',sum)
#     #다 더한 뒤 cash.html에 data로 보내준다.
#     data['price_sum'] = sum
#     return render(request,"cash.html",data)