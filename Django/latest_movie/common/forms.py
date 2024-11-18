from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import bcrypt
from django.contrib.auth import authenticate

# 유저 생성 모듈 이용
class UserForm(UserCreationForm):
    # 아래 기본 폼 외에 사용자의 이메일 주소를 입력 받도록 추가로 설정
    email = forms.EmailField(label="이메일")

    class Meta:
        # model은 이 폼이 연결될 사용자 모델을 지정하고, fields는 폼에서 사용할 필드들을 나열
        model = User
        fields = ("username", "password1", "password2", "email")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    # 입력된 데이터를 유효성 검사하기 위해 사용
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise forms.ValidationError("사용자명 또는 비밀번호가 올바르지 않습니다.")

        return cleaned_data

