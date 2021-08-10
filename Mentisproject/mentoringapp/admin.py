from django.contrib import admin
from .models import *

# Register your models here.

# 참고 https://wayhome25.github.io/django/2017/03/22/django-ep8-django-admin/

# 멘토 DB
@admin.register(Mentor_info)
class Mentor_infoAdmin(admin.ModelAdmin):
    list_display = ('pk','user_info_id','contents')
# 강의 DB
@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title', 'mentor_id', 'mentor_description', 'description', 'price', 'field')

# 세부 강의 DB
@admin.register(DetailLecture)
class DetailLecutreAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title', 'video_title', 'url')

# My 강의 DB
@admin.register(LectureList)
class LectureListAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title','user_id')

# 즐겨찾기 강의 DB
@admin.register(FavouriteLecture)
class FavAdmin(admin.ModelAdmin):
    list_display = ('pk','lecture_title','user_id')

# 스펙 DB
admin.site.register(Qualification)


# 댓글 DB
# admin.site.register(Comment)