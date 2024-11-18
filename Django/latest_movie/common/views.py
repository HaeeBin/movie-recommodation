# authenticate() 함수는 사용자 인증을 수행합니다. 즉, 제공된 자격 증명이 올바른지 
# 확인하고, 올바른 경우 해당 사용자 객체를 반환
# login() 함수는 사용자를 로그인 상태로 만듭니다. 이는 Django 세션에 사용자 ID를 저장하여
# 사용자를 인증된 상태로 유지하는 데 사용
from django.contrib.auth import authenticate, login
# render() 함수는 특정 템플릿을 사용하여 HTML 페이지를 렌더링하는 데 사용됩니다. 
# redirect() 함수는 클라이언트를 다른 URL로 리디렉션하는 데 사용됨
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import JsonResponse
from common.forms import UserForm, LoginForm
from django.contrib.auth.views import ( 
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)                                      
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)

INTERNAL_RESET_URL_TOKEN = 'set-password'
INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'

def signup(request):
    # urls에서 signup/으로의 주소가 나오면 이 view를 연다. 
    # 이게 열린 상태에서(회원가입 폼에서) POST 입력이 들어오면
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # 정제된(cleaned) 데이터에서 사용자 이름과 비밀번호를 추출
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2') 

            if User.objects.filter(username=username).exists():
                return JsonResponse({'message': 'USERNAME_ALREADY_EXISTS'}, status=422)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EMAIL_ALREADY_EXISTS'}, status=422)

            if password1 != password2:
                return JsonResponse({'message': 'PASSWORD_MISMATCH_ERROR'}, status=422)
            
            form.save()
            # 인증후 로그인 (회원가입 후 자동 로그인되게 설정한것)
            user = authenticate(username=username, password=password1) 
            if user is not None:
                login(request, user)
                return redirect('djan:main')
            # 'main'라는 이름의 URL(메인페이지)로 리다이렉트
    # 사용자가 회원가입 페이지에 처음 접근했을 때(GET 요청) 빈 회원가입 폼 생성
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # User is valid, log them in
                login(request, user)
                return redirect('djan:main')
            else:
                # Invalid credentials
                form.add_error(None, '사용자명 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = LoginForm()

    return render(request, 'common/login.html', {'form': form})
            
# 비밀번호 잃어버렸을 때
class UserPasswordResetView(PasswordResetView):
    template_name = 'common/password_reset.html'

    # 성공 시 호출할 url
    success_url = reverse_lazy('password_reset_done')
    form_class = PasswordResetForm
    
    def form_valid(self, form):
        # 이메일이 존재해야 발송
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            return render(self.request, 'common/password_reset_done_fail.html')

# 비밀번호 재설정 링크 보내기 성공           
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'common/password_reset_done.html'

# 
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url=reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'

    def form_valid(self, form):
        return super().form_valid(form)

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


                
