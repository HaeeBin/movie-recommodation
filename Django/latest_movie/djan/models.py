from django.db import models
# 사용자 모델로 회원가입시 데이터 저장 등에 사용
from django.conf import settings
from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from psycopg2 import IntegrityError
from django.contrib.auth.models import User

class movie_all(models.Model):
    movie_code = models.CharField(max_length=255, primary_key=True, default=None)
    rank= models.IntegerField(null=True)
    rank_intensity = models.IntegerField(null=True)
    korean_name = models.CharField(max_length=255, null=True)
    open_date= models.CharField(max_length=255, null=True)
    audiacc=models.CharField(max_length=255, null=True)
    audicnt_showcnt = models.IntegerField(null=True)
    genre = models.CharField(max_length=100)
    running_time = models.CharField(max_length=255, null=True)

class trusted_director(models.Model):
    director= models.CharField(max_length=255, primary_key=True, default=None)
    average_audience=models.IntegerField(null=True)
    audience_showcnt=models.FloatField(null=True)

class trusted_actor(models.Model):
    actor= models.CharField(max_length=255, primary_key=True, default=None)
    number=models.IntegerField(null=True)
    avg_audience=models.IntegerField(null=True)
    audience_showcnt=models.FloatField(null=True)

class music_director(models.Model):
    peoplenm=models.CharField(max_length=255, primary_key=True, default=None)
    work_count=models.IntegerField(null=True)
    average_audiacc=models.IntegerField(null=True)
    audience_showcnt=models.FloatField(null=True)

class comment_worker(models.Model):
    id=models.CharField(max_length=255, primary_key=True, default=None)
    naver_review=models.TextField(null=True)
    same_comment=models.IntegerField(null=True)
    review_score=models.IntegerField(null=True)

# 선택
class choice(models.Model):
    # 선택을 영화와 묶어줌, 영화가 삭제되면 선택도 삭제되게 설정
    movie = models.ForeignKey(movie_all, null=True, on_delete=models.CASCADE)
    # 선택팀 텍스트(토트넘 등등)
    choice_text = models.CharField(max_length=200)
    # 투표수
    votes = models.IntegerField(default=0)

# 댓글
class answer(models.Model):
    # 질문에 해당하는 댓글들을 연결, 질문 지우면 댓글들도 지워짐
    movie = models.ForeignKey(movie_all, null=True, on_delete=models.CASCADE)
    # 댓글 내용 작성 부분
    content = models.TextField()
    # 댓글 작성 날짜
    answer_date = models.DateTimeField(auto_now_add=True)
    # 작성자 속성,기존에 저장된 값들은 null 처리
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

# 유저의 모델 
class user_info(models.Model):
    movie = models.ForeignKey(movie_all, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(choice, null=True, default=None, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # Movie_Ranking 인스턴스가 새로 생성되는 경우에만 choice 인스턴스 생성
        super().save(*args, **kwargs)  # 부모 클래스의 save 메서드 호출로 인스턴스 저장
            # 새로운 Movie_Ranking 인스턴스에 대해 choice 인스턴스 생성
        if not choice.objects.filter(movie=self.movie).exists():
            for i in range(1, 6):  # 1, 2, 3에 대한 choice 인스턴스 생성
                choice.objects.create(movie=self, choice_text=str(i),votes=0)

class movie_info(models.Model):
    movie = models.ManyToManyField(movie_all, related_name='movie_all')
    story = models.TextField(null=True)
    accessible = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    company=models.CharField(max_length=100)
    poster = models.URLField(null=True)

class movie_rating(models.Model):
    movie = models.ForeignKey(movie_all, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(choice, null=True, default=None, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # 새로운 투표 인스턴스가 생성되는 경우에만 choice 인스턴스 생성
        super().save(*args, **kwargs)  # 부모 클래스의 save 메서드 호출로 인스턴스 저장
            # 이미 해당 영화에 대한 choice 인스턴스가 생성되었는지 확인
        if not choice.objects.filter(movie=self.movie).exists():
            for i in range(1, 6):
                    choice.objects.create(movie=self.movie, choice_text=str(i), votes=0)

            