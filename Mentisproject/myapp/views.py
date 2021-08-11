
from django.shortcuts import redirect, render,HttpResponse
from .models import User_info,Menti_info,Cash
from mentoringapp.models import FavouriteLecture,Mentor_info,LectureList,DetailLecture,Lecture
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


def class_upload(request):
    #현재 로그인 한 사람이 누구인지 체크
    user_temp = request.session.get('temp') # 'tony'
    user = User_info.objects.get(user_id='123') 
    #만약에 멘토 --> 이 조건은 class_upload.html 안에서 if문으로 구현하기.
    mento =  Mentor_info.objects.get(user_info_id = user.pk) #멘토를 찾는다.

    #멘토가 등록한 강의중 데이터베이스 라는 강의를 가져온다. 
    #이 부분은 따로 변경해야된다. 세부 강의의 정보를 매게변수로 받아야함.
    print('멘토의 pk = ',mento.pk)
    lec = Lecture.objects.get(mentor_id = mento.pk,lecture_title='데이터베이스')
    print('lec = ',lec)
    if request.method == "POST": #제출하기 버튼을 눌렀을 때
        total_input_data = int(request.POST.get('total'))
        for i in range(1,total_input_data+1):
            detail_lec = DetailLecture( #데이터베이스 라는 강좌의 전체 강의를 업로드.
            lecture_title = lec,
            video_title = request.POST.get('title'+str(i)),
            url = request.POST.get('youtube_iframe'+str(i))
            )
            detail_lec.save()
        print('DB에 저장이 완료되었습니다.')
        return HttpResponse('DB에 저장이 완료되었습니다')
    else:
        return render(request,'class_upload.html')



def class_view(request):
    data = {}

    user = User_info.objects.get(user_id='123')  #아이디 123 인 멘토
    #아이디 123 인 멘토가 올린 강의를 모두 가져온다.

    # 그 중 사람이 '데이터베이스' 라는 강의를 클릭하면 
    temp_class_name = '데이터베이스'
    lec = Lecture.objects.get(lecture_title='데이터베이스')
    lecture_detail_list =  DetailLecture.objects.filter(lecture_title=lec).values()
    print('쿼리로 찾은 데이터셋 ->',lecture_detail_list)
    
    url_list = []
    title_list = []
    data['test'] = lecture_detail_list
    data['total_num'] = len(lecture_detail_list)
    for lecture_detail in lecture_detail_list:
        url_src = lecture_detail['url'].split(" ")[3]
        temp_data = url_src[5:-1]
        print(url_src[5:-1])
        url_list.append(temp_data)
        title_list.append(lecture_detail['video_title'])

    data['url_list'] = url_list
    data['title_list'] = title_list
    #데이터베이스 의 세부 강의 DB에 접근해서 url 를 몽땅 가져온다.
    return render(request,'class_list_page.html',data)


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