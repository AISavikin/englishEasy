from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class SimpleRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Имя",
        help_text="Ваше настоящее имя"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Упрощенные подсказки
        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'
        self.fields['username'].label = 'Логин'
        self.fields['password1'].help_text = 'Минимум 8 символов'
        self.fields['password2'].help_text = 'Повторите пароль'

        # Убираем сложные валидаторы паролей
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = ''

    def clean_username(self):
        username = self.cleaned_data['username'].lower()

        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')

        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        # По умолчанию все новые пользователи - ученики
        user.role = 'student'

        if commit:
            user.save()
        return user