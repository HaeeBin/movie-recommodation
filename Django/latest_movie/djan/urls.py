from django.urls import path

from . import views

#다른 프로젝트와 꼬이지 않게 이름지정
app_name='djan'

urlpatterns = [
    # '' 요청이 들어오면, view.py 의 main 메서드 연결
    path('', views.main, name='main'),

    # /숫자/ 링크를 입력하면, view.py 의 detail 메서드 연결
    path('<str:movie_code>/', views.detail ,name='detail'),

    # /숫자/vote/ 링크를 입력하면, view.py 의 vote 메서드 연결
    path('<str:movie_code>/vote/', views.vote, name='vote'),
    
    # /answer/create/숫자/ 링크를 입력하면, view.py 의 answer_create 메서드 연결
    # 이건 보통 링크를 입력해 접속하지 않고 투표하면 자동으로 이동한다. 
    path('answer/create/<str:movie_code>/', views.answer_create, name='answer_create'),
]