from django.db import models

# Create your models here.

# 멘토 DB
class Mentor_info(models.Model):
    user_info_id = models.ForeignKey('myapp.User_info', on_delete=models.CASCADE, db_column="user_info_id", verbose_name='멘토 이름',db_constraint=False,null=True)
    contents = models.TextField(blank=True, null=True, verbose_name='멘토 이력')

    class Meta:
        db_table = 'mentor_table'
        verbose_name = '멘토'
        verbose_name_plural = '멘토'

    def __str__(self):
        return str(self.user_info_id)

# 강의 DB: 기본키(아마 알아서 들어가는 걸로 알고 있음), 강의 이름, 멘토ID(외래키 -> 왜??), 강의 설명서, 강의 가격, 강사 설명, 강의 분야(복수 개 -> 대체 어떻게? 하려면 분야 DB를 따로 빼야 하지 않을까?)
class Lecture(models.Model):
    lecture_title = models.CharField(max_length=256,
                                     verbose_name='강의 이름')
    mentor_id = models.ForeignKey(Mentor_info, on_delete=models.CASCADE, db_column="mentor_id", verbose_name='멘토') # 멘토가 강의를 올리고 자신을 설명함
    mentor_description = models.CharField(max_length=64,
                                          verbose_name='멘토 설명') # 강사 설명? 강사 이름? 뭐지?
    description = models.CharField(max_length=1000,
                                   verbose_name='설명')
    price = models.CharField(max_length=64,
                             verbose_name='가격') # IntegerField? CharField?
    LECTURE_FIELD = ( # 강의 분야 고르는 것에서 여러 개 중 하나 선택으로 만듦, 여러 분야를 선택하고 싶으면 DB를 추가로 만들어야 함 (프론트에 물어 볼까..?)
        ('A', '개발·프로그래밍'),
        ('B', '보안·네트워크'),
        ('C', '데이터 사이언스'),
        ('D', '크리에이티브'),
        ('E', '직무·마케팅'),
        ('F', '학문·외국어'),
        ('G', '커리어'),
        ('H', '교양')
    ) # 분야는 인프런을 참고함
    field = models.CharField(max_length=64,
                             choices=LECTURE_FIELD,
                             verbose_name='분야',
                             blank=True,
                             null=True)
    
    def __str__(self):
        return self.lecture_title

    class Meta:
        db_table = 'lecture_table'
        verbose_name = '전체 강의'
        verbose_name_plural = '전체 강의'

# 세부 강의 DB: 기본키, 강의 ID(외래키), 영상 제목, 영상 URL
class DetailLecture(models.Model):
    lecture_title = models.ForeignKey(Mentor_info,
                                on_delete=models.CASCADE,
                                db_column="lecture_title",
                                verbose_name='강의 이름')
    video_title = models.CharField(max_length=256,
                                   verbose_name='영상 제목')
    url = models.CharField(max_length=256,
                           verbose_name='url')
    
    def __str__(self):
        return self.video_title

    class Meta:
        db_table = 'detail_lecture_table'
        verbose_name = '세부 강의'
        verbose_name_plural = '세부 강의'

# My 강의 -> 수정 필요
class LectureList(models.Model):
    lecture_title = models.ForeignKey(Lecture, verbose_name='강의 이름', on_delete=models.CASCADE)
    user_id = models.ForeignKey('myapp.Menti_info', verbose_name='신청한 사람', db_column="user_id", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.lecture_title)

    class Meta:
        db_table = 'lecturelist_table'
        verbose_name = 'My 강의'
        verbose_name_plural = 'My 강의'

# 즐겨찾기 강의 DB
class FavouriteLecture(models.Model):
    lecture_title = models.ForeignKey(Lecture, db_column="lecture_title", verbose_name='강의 이름', on_delete=models.CASCADE)
    user_id = models.ForeignKey('myapp.Menti_info',related_name="fav_user",db_column="user_id", verbose_name='즐겨찾기한 사람', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.lecture_title)

    class Meta:
        db_table = 'favourite_lecture_table'
        verbose_name = '즐겨찾기 강의'
        verbose_name_plural = '즐겨찾기 강의'

# 스펙 DB(토익, 토스 등): 유저 ID(외래키), 이미지(ImageField)
class Qualification(models.Model):
    user_id = models.ForeignKey('myapp.User_info', # User는 임의로 설정한 것 -> 이름 맞춰야 함 !
                                on_delete=models.CASCADE,
                                db_column="user_id",
                                verbose_name='유저 ID')
    certificate = models.ImageField(upload_to="",
                                    verbose_name='관련 이미지',
                                    blank=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'qualification_table'
        verbose_name = '스펙'
        verbose_name_plural = '스펙'

'''
# 댓글 DB: 공통 ID(외래키..?), User ID(외래키), 날짜/시간, 내용 
class Comment(models.Model):
    # 공통 ID -> 게시글 & 칼럼 & 강의를 모두 포함 가능한가?? 어떻게??
    user_id = models.ForeignKey(User_info, # User는 임의로 설정한 것 -> 이름 맞춰야 함 !
                                on_delete=models.CASCADE,
                                verbose_name='유저 ID')
    commented_at = models.DateTimeField(auto_now_add=True,
                                        verbose_name='작성 날짜/시간')
    
    def __str__(self):
        return self.user_id
    
    class Meta:
        db_table = 'comment_table'
        verbose_name = '댓글'
        verbose_name_plural = '댓글'
'''