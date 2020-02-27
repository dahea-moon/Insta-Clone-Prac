# 가입 / 정보수정 / 로그인
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User