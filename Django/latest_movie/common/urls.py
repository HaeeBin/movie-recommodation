from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'

urlpatterns = [
    # 로그인,LoginView 클래스를 사용하여 사용자 인증을 처리합니다.
    path('login/', views.user_login , name='login'),
    # 로그아웃
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # 회원가입요청시 views의 signup 실행
    path('signup/', views.signup, name='signup'),
    # 비밀번호 초기화
    path('password_reset/', views.UserPasswordResetView.as_view(), name="password_reset"),
    # 비밀번호 초기화 링크 전송 성공
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
]