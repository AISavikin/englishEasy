# 📁 Дерево проекта

```
- ./
    - get_project_dump.py
    - manage.py
    - dashboard/
        - admin.py
        - apps.py
        - models.py
        - tests.py
        - urls.py
        - views.py
        - __init__.py
        - templates/
            - dashboard/
                - student.html
                - teacher.html
    - englishEasy/
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
        - __init__.py
    - static/
    - templates/
        - base.html
    - users/
        - admin.py
        - apps.py
        - forms.py
        - models.py
        - tests.py
        - urls.py
        - views.py
        - __init__.py
        - templates/
            - registration/
                - logged_out.html
            - users/
                - home.html
                - login.html
                - register_student.html
                - register_teacher.html
    - vocabulary/
        - admin.py
        - apps.py
        - forms.py
        - models.py
        - tests.py
        - urls.py
        - views.py
        - __init__.py
        - templates/
            - vocabulary/
                - select_student.html
                - teacher_panel.html
                - word_create.html
```

# 📄 Содержимое файлов

## `get_project_dump.py`

```text
import os
import fnmatch

def ask_path(prompt, default="."):
    value = input(f"{prompt} [{default}]: ").strip()
    return value if value else default

def ask_yes_no(prompt, default="n"):
    value = input(f"{prompt} (y/n) [{default}]: ").strip().lower()
    if value == "":
        value = default
    return value == "y"

def ask_list(prompt, default=""):
    value = input(f"{prompt} (через запятую) [{default}]: ").strip()
    if not value:
        value = default
    return [v.strip() for v in value.split(",") if v.strip()]

def is_excluded(path: str, exclude_masks):
    filename = os.path.basename(path)
    for mask in exclude_masks:
        if fnmatch.fnmatch(filename, mask):
            return True
    return False

def build_tree(start_path: str, include_hidden: bool, exclude_masks) -> str:
    tree_lines = []

    for root, dirs, files in os.walk(start_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

        dirs[:] = [d for d in dirs if not is_excluded(d, exclude_masks)]
        files = [f for f in files if not is_excluded(f, exclude_masks)]

        level = root.replace(start_path, "").count(os.sep)
        indent = "    " * level
        tree_lines.append(f"{indent}- {os.path.basename(root)}/")

        sub_indent = "    " * (level + 1)
        for file in files:
            tree_lines.append(f"{sub_indent}- {file}")

    return "\n".join(tree_lines)

def collect_files(start_path: str, include_hidden: bool, exclude_masks) -> str:
    combined = []

    for root, dirs, files in os.walk(start_path):
        if not include_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]

        dirs[:] = [d for d in dirs if not is_excluded(d, exclude_masks)]
        files = [f for f in files if not is_excluded(f, exclude_masks)]

        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), start_path)
            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"<<Ошибка чтения файла: {e}>>"

            combined.append(
                f"## `{rel_path}`\n\n"
                f"```text\n{content}\n```\n"
                f"---\n\n"
            )

    return "".join(combined)

def save_markdown(start_path: str, output_file: str, include_hidden: bool, exclude_masks):
    tree = build_tree(start_path, include_hidden, exclude_masks)
    files_content = collect_files(start_path, include_hidden, exclude_masks)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 📁 Дерево проекта\n\n")
        f.write("```\n" + tree + "\n```\n\n")
        f.write("# 📄 Содержимое файлов\n\n")
        f.write(files_content)

    print(f"\nГотово! Markdown сохранён: {output_file}")

if __name__ == "__main__":
    print("=== Проектовый дампер в Markdown ===\n")

    start_path = ask_path("Введите путь к проекту", ".")
    output_file = ask_path("Введите имя выходного файла", "project_dump.md")
    include_hidden = ask_yes_no("Включать скрытые файлы?")
    exclude_masks = ask_list("Маски исключения", "*.pyc, __pycache__, *.sqlite3, migrations")

    print("\nСобираю данные...\n")
    save_markdown(start_path, output_file, include_hidden, exclude_masks)
```
---

## `manage.py`

```text
#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishEasy.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```
---

## `dashboard\admin.py`

```text
from django.contrib import admin

# Register your models here.

```
---

## `dashboard\apps.py`

```text
from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

```
---

## `dashboard\models.py`

```text
from django.db import models

# Create your models here.

```
---

## `dashboard\tests.py`

```text
from django.test import TestCase

# Create your tests here.

```
---

## `dashboard\urls.py`

```text
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('teacher/', views.teacher_dashboard, name='teacher'),
    path('student/', views.student_dashboard, name='student'),
]
```
---

## `dashboard\views.py`

```text
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from users.models import User
from vocabulary.models import StudentWord, Assignment


@login_required
def home(request):
    if request.user.is_teacher():
        return redirect('dashboard:teacher')
    return redirect('dashboard:student')


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    students = User.objects.filter(role='student')  # ДОБАВИТЬ

    return render(request, 'dashboard/teacher.html', {'students': students})

@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('dashboard:home')

    assigned_words = StudentWord.objects.filter(student=request.user)

    return render(request, 'dashboard/student.html', {
        'assigned_words': assigned_words  # ДОБАВИТЬ
    })
```
---

## `dashboard\__init__.py`

```text

```
---

## `dashboard\templates\dashboard\student.html`

```text
{% extends 'base.html' %}
{% block title %}Мои слова{% endblock %}

{% block content %}
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Мои слова для изучения</h1>
        <div class="text-muted">
            Всего: <strong>{{ assigned_words.count }}</strong>
        </div>

    </div>


{% endblock %}
```
---

## `dashboard\templates\dashboard\teacher.html`

```text
{% extends 'base.html' %}
{% block content %}
    <div class="text-center py-5">
        <h1>Кабинет учителя</h1>
        <!-- Исправленная строка: добавлен правильный URL -->
        <a href="{% url 'vocabulary:select_student' %}" class="btn btn-primary btn-lg px-5">
            <i class="bi bi-people me-2"></i>
            Перейти к ученикам
        </a>
    </div>
{% endblock %}
```
---

## `englishEasy\asgi.py`

```text
"""
ASGI config for englishEasy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishEasy.settings')

application = get_asgi_application()

```
---

## `englishEasy\settings.py`

```text
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-change-me-in-production'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'vocabulary',
    'dashboard',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'englishEasy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'englishEasy.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = 'dashboard:home'
LOGOUT_REDIRECT_URL = 'users:home'
LOGIN_URL = 'users:login'
```
---

## `englishEasy\urls.py`

```text
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('vocabulary/', include('vocabulary.urls')),
]

```
---

## `englishEasy\wsgi.py`

```text
"""
WSGI config for englishEasy project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'englishEasy.settings')

application = get_wsgi_application()

```
---

## `englishEasy\__init__.py`

```text

```
---

## `templates\base.html`

```text
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}English Easy{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        body { background: #f8f9fa; }
        .navbar-brand { font-weight: 800; }
    </style>
{% block extra_style %}
	
{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="{% url 'dashboard:home' %}">English Easy</a>
            
            <div class="navbar-nav ms-auto align-items-center">
                {% if user.is_authenticated %}
                    <span class="text-white me-4">
                        <i class="bi bi-person-circle"></i>
                        {{ user.get_full_name|default:user.username }}
                        {% if user.is_teacher %}<small class="badge bg-light text-dark ms-2">Учитель</small>{% endif %}
                        {% if user.is_student %}<small class="badge bg-success text-white ms-2">Ученик</small>{% endif %}
                    </span>
                    
                    <!-- Правильный logout через POST -->
                    <form method="post" action="{% url 'users:logout' %}" class="d-inline">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-outline-light btn-sm">
                            <i class="bi bi-box-arrow-right"></i> Выйти
                        </button>
                    </form>
                {% else %}
                    <a class="btn btn-outline-light btn-sm" href="{% url 'users:login' %}">
                        <i class="bi bi-box-arrow-in-right"></i> Войти
                    </a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="container mt-4 mb-5">
        {% if messages %}
            <div class="row">
                <div class="col">
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                </div>
            </div>
        {% endif %}

        {% block content %}
        {% endblock %}
    </main>

    <footer class="bg-dark text-white py-4 mt-auto">
        <div class="container text-center">
            <small>© 2025 English Easy — простая платформа для изучения слов</small>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```
---

## `users\admin.py`

```text
from django.contrib import admin

# Register your models here.

```
---

## `users\apps.py`

```text
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

```
---

## `users\forms.py`

```text
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
        return user

class TeacherRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'teacher'
        if commit:
            user.save()
        return user
```
---

## `users\models.py`

```text
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('teacher', 'Учитель'),
        ('student', 'Ученик'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def is_teacher(self):
        return self.role == 'teacher'

    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        return self.get_full_name() or self.username
```
---

## `users\tests.py`

```text
from django.test import TestCase

# Create your tests here.

```
---

## `users\urls.py`

```text
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
]
```
---

## `users\views.py`

```text
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import StudentRegisterForm, TeacherRegisterForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    return render(request, 'users/home.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать, ученик!')
            return redirect('dashboard:home')
    else:
        form = StudentRegisterForm()
    return render(request, 'users/register_student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Добро пожаловать, учитель!')
            return redirect('dashboard:home')
    else:
        form = TeacherRegisterForm()
    return render(request, 'users/register_teacher.html', {'form': form})
```
---

## `users\__init__.py`

```text

```
---

## `users\templates\registration\logged_out.html`

```text
{% extends 'base.html' %}
{% block title %}Вы вышли{% endblock %}

{% block content %}
<div class="text-center py-5">
    <h1>Вы успешно вышли из системы</h1>
    <a href="{% url 'users:home' %}" class="btn btn-primary btn-lg mt-4">На главную</a>
</div>
{% endblock %}
```
---

## `users\templates\users\home.html`

```text
{% extends 'base.html' %}
{% block title %}English Easy — Главная{% endblock %}

{% block content %}
<div class="text-center py-5">
    <h1 class="display-3 fw-bold text-primary mb-4">English Easy</h1>
    <p class="lead mb-5">Простая и эффективная платформа для изучения английских слов</p>

    {% if user.is_authenticated %}
        <div class="alert alert-success">
            Добро пожаловать, {{ user.get_full_name|default:user.username }}!
        </div>
        <a href="{% url 'dashboard:home' %}" class="btn btn-primary btn-lg px-5">
            Перейти в личный кабинет
        </a>
    {% else %}
        <div class="row justify-content-center g-4">
            <div class="col-md-5">
                <div class="card h-100 shadow-lg border-0">
                    <div class="card-body text-center p-5">
                        <i class="bi bi-person-fill display-1 text-primary mb-4"></i>
                        <h3>Я ученик</h3>
                        <p class="text-muted">Учу слова, делаю упражнения, вижу прогресс</p>
                        <a href="{% url 'users:register_student' %}" class="btn btn-outline-primary btn-lg">
                            Зарегистрироваться
                        </a>
                        <div class="mt-3">
                            <small>Уже есть аккаунт? <a href="{% url 'users:login' %}">Войти</a></small>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-5">
                <div class="card h-100 shadow-lg border-0">
                    <div class="card-body text-center p-5">
                        <i class="bi bi-person-badge-fill display-1 text-success mb-4"></i>
                        <h3>Я учитель</h3>
                        <p class="text-muted">Назначаю слова, вижу прогресс учеников</p>
                        <a href="{% url 'users:register_teacher' %}" class="btn btn-success btn-lg">
                            Зарегистрироваться
                        </a>
                        <div class="mt-3">
                            <small>Уже есть аккаунт? <a href="{% url 'users:login' %}">Войти</a></small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {% endif %}
</div>
{% endblock %}
```
---

## `users\templates\users\login.html`

```text
{% extends 'base.html' %}
{% block title %}Вход{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 col-lg-5">
        <div class="card shadow-lg">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Вход в систему</h2>
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label">Логин</label>
                        <input type="text" name="username" class="form-control form-control-lg" required>
                    </div>
                    <div class="mb-4">
                        <label class="form-label">Пароль</label>
                        <input type="password" name="password" class="form-control form-control-lg" required>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg w-100">Войти</button>
                </form>
                <div class="text-center mt-4">
                    <p>Нет аккаунта? 
                        <a href="{% url 'users:register_student' %}">Ученик</a> • 
                        <a href="{% url 'users:register_teacher' %}">Учитель</a>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---

## `users\templates\users\register_student.html`

```text
{% extends 'base.html' %}
{% block title %}Регистрация ученика{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-body p-5">
                <h3 class="text-center mb-4">Регистрация ученика</h3>
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-success btn-lg w-100">Создать аккаунт</button>
                </form>
                <div class="text-center mt-3">
                    <a href="{% url 'users:login' %}">Уже есть аккаунт? Войти</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---

## `users\templates\users\register_teacher.html`

```text
{% extends 'base.html' %}
{% block title %}Регистрация учителя{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-body p-5">
                <h3 class="text-center mb-4">Регистрация учителя</h3>
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-primary btn-lg w-100">Создать аккаунт</button>
                </form>
                <div class="text-center mt-3">
                    <a href="{% url 'users:login' %}">Уже есть аккаунт? Войти</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---

## `vocabulary\admin.py`

```text
from django.contrib import admin

# Register your models here.

```
---

## `vocabulary\apps.py`

```text
from django.apps import AppConfig


class VocabularyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vocabulary'

```
---

## `vocabulary\forms.py`

```text
from django import forms
from .models import Word, Topic
from users.models import User


class WordCreateForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        label="Ученик",
        required=True
    )

    class Meta:
        model = Word
        fields = ['russian', 'english', 'topic']
        widgets = {
            'russian': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: собака'
            }),
            'english': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: dog'
            }),
            'topic': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'russian': 'Русское слово',
            'english': 'Английский перевод',
            'topic': 'Тема'
        }
```
---

## `vocabulary\models.py`

```text
from django.db import models
from django.conf import settings

from users.models import User


class Topic(models.Model):
    name = models.CharField("Название темы", max_length=100)
    color = models.CharField("Цвет (HEX)", max_length=7, default="#3B82F6")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.name


class Word(models.Model):
    russian = models.CharField("Русский", max_length=100)
    english = models.CharField("English", max_length=100)
    topic = models.ForeignKey(
        Topic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='words'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('russian', 'english')
        ordering = ['russian']
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def save(self, *args, **kwargs):
        self.english = self.english.strip().lower()
        self.russian = self.russian.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.russian} → {self.english}"

class StudentWord(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_words',
        limit_choices_to={'role': 'student'}
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_words_by_teacher',
        verbose_name="Назначено учителем"
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField("Назначено", auto_now_add=True)

    class Meta:
        unique_together = ('student', 'word')
        ordering = ['-assigned_at']
        verbose_name = "Назначенное слово"
        verbose_name_plural = "Назначенные слова"

    def __str__(self):
        return f"{self.student} ← {self.word}"


class Assignment(models.Model):
    TYPE_CHOICES = (
        ('homework', 'Домашняя работа'),
        ('classwork', 'Классная работа'),
        ('revision', 'Повторение слабых слов'),
    )

    title = models.CharField("Название", max_length=200, default="Домашнее задание")
    type = models.CharField("Тип", max_length=20, choices=TYPE_CHOICES, default='homework')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    words = models.ManyToManyField(Word, related_name='assignments')

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField("Сдать до", null=True, blank=True)
    note = models.TextField("Примечание", blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"
```
---

## `vocabulary\tests.py`

```text
from django.test import TestCase

# Create your tests here.

```
---

## `vocabulary\urls.py`

```text
# vocabulary/urls.py

from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    # Страница выбора ученика
    path('select_student/', views.select_student, name='select_student'),

    # Панель учителя для конкретного ученика
    path('teacher_panel/<int:student_id>/', views.teacher_panel, name='teacher_panel'),

    # AJAX-запросы
    path('word/create/ajax/', views.word_create_ajax, name='word_create_ajax'),
    path('topic/create/ajax/', views.topic_create_ajax, name='topic_create_ajax'),
    path('word/delete/ajax/', views.word_delete_ajax, name='word_delete_ajax'),

    # Другие страницы
    path('word/create/', views.word_create, name='word_create'),
    path('assign/<int:student_id>/', views.assign_words, name='assign_words'),
    path('assignment/create/<int:student_id>/', views.create_assignment, name='create_assignment'),
]
```
---

## `vocabulary\views.py`

```text
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Word, Topic, StudentWord
from .forms import WordCreateForm
from users.models import User
from django.views.decorators.http import require_POST


@login_required
def select_student(request):
    """Страница выбора ученика"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    students = User.objects.filter(role='student')

    return render(request, 'vocabulary/select_student.html', {
        'students': students
    })


@login_required
def word_create(request):
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    # Получаем ID ученика и темы из GET или сессии
    student_id = request.GET.get('student_id') or request.session.get('last_student_id')
    topic_id = request.GET.get('topic_id') or request.session.get('last_topic_id')

    # Если передан student_id, сохраняем в сессии
    if 'student_id' in request.GET:
        request.session['last_student_id'] = request.GET['student_id']
        student_id = request.GET['student_id']

    # Если передан topic_id, сохраняем в сессии
    if 'topic_id' in request.GET:
        request.session['last_topic_id'] = request.GET['topic_id']
        topic_id = request.GET['topic_id']

    # Получаем объекты
    student = None
    topic = None

    if student_id:
        student = get_object_or_404(User, id=student_id, role='student')
    if topic_id:
        topic = get_object_or_404(Topic, id=topic_id)

    # Формируем начальные данные
    initial = {}
    if student:
        initial['student'] = student
    if topic:
        initial['topic'] = topic

    if request.method == 'POST':
        form = WordCreateForm(request.POST, initial=initial)
        if form.is_valid():
            word = form.save(commit=False)
            word.save()

            # Создаем связь с учеником
            student = form.cleaned_data['student']
            StudentWord.objects.create(
                student=student,
                word=word,
                assigned_by=request.user
            )

            messages.success(request, f'Слово "{word.russian} → {word.english}" добавлено')

            # Редирект на ту же страницу с сохраненными параметрами
            redirect_url = f"{request.path}?student_id={student.id}"
            if topic:
                redirect_url += f"&topic_id={topic.id}"

            return redirect(redirect_url)
    else:
        form = WordCreateForm(initial=initial)

    # Получаем последние добавленные слова для этого ученика
    recent_words = []
    if student:
        recent_words = StudentWord.objects.filter(
            student=student
        ).select_related('word', 'word__topic').order_by('-assigned_at')[:10]

    context = {
        'form': form,
        'student': student,
        'topic': topic,
        'recent_words': recent_words,
        'students': User.objects.filter(role='student'),
        'topics': Topic.objects.all(),
    }

    return render(request, 'vocabulary/word_create.html', context)


# vocabulary/views.py - обновляем word_create_ajax

@login_required
def word_create_ajax(request):
    """Добавление слова для конкретного ученика (через AJAX)"""
    if not request.user.is_teacher():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    if request.method == 'POST':
        try:
            russian = request.POST.get('russian', '').strip().lower()
            english = request.POST.get('english', '').strip().lower()
            student_id = request.POST.get('student_id')
            topic_id = request.POST.get('topic_id') or None

            # Проверяем обязательные поля
            if not russian or not english:
                return JsonResponse({
                    'success': False,
                    'error': 'Заполните русское и английское слово'
                })

            if not student_id:
                return JsonResponse({
                    'success': False,
                    'error': 'Не указан ученик'
                })

            # Получаем ученика
            try:
                student = User.objects.get(id=student_id, role='student')
            except User.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Ученик не найден'
                })

            # Создаем или получаем слово
            word_data = {
                'russian': russian,
                'english': english,
            }
            if topic_id:
                word_data['topic_id'] = topic_id

            word, created = Word.objects.get_or_create(**word_data)

            # Создаем связь с учеником
            student_word, sw_created = StudentWord.objects.get_or_create(
                student=student,
                word=word,
                defaults={'assigned_by': request.user}
            )

            # Подготавливаем данные для ответа
            response_data = {
                'success': True,
                'word': {
                    'id': word.id,
                    'russian': word.russian,
                    'english': word.english,
                    'topic': word.topic.name if word.topic else '',
                    'topic_color': word.topic.color if word.topic else '#6c757d'
                },
                'student': {
                    'id': student.id,
                    'name': student.get_full_name() or student.username
                },
                'created': created,
                'assigned': sw_created,
                'message': 'Слово успешно добавлено и назначено ученику'
            }

            if not sw_created:
                response_data['message'] = 'Это слово уже было назначено ученику ранее'

            return JsonResponse(response_data)

        except Exception as e:
            print(f"Ошибка при добавлении слова: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Ошибка сервера: {str(e)}'
            })

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})
# в vocabulary/views.py добавить:
@login_required
def assign_words(request):
    if not request.user.is_teacher():
        return redirect('dashboard:home')
    # Логика массового назначения слов
    return render(request, 'vocabulary/assign_words.html')

@login_required
def create_assignment(request):
    if not request.user.is_teacher():
        return redirect('dashboard:home')
    # Логика создания задания
    return render(request, 'vocabulary/create_assignment.html')


@login_required
@require_POST
def topic_create_ajax(request):
    if not request.user.is_teacher():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    name = request.POST.get('name', '').strip()
    color = request.POST.get('color', '#3B82F6')

    if not name:
        return JsonResponse({'success': False, 'error': 'Введите название темы'})

    topic = Topic.objects.create(name=name, color=color)

    return JsonResponse({
        'success': True,
        'topic': {
            'id': topic.id,
            'name': topic.name,
            'color': topic.color
        }
    })


# vocabulary/views.py - обновляем функцию teacher_panel

@login_required
def teacher_panel(request, student_id):
    """Панель учителя для конкретного ученика"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    # Получаем ученика
    student = get_object_or_404(User, id=student_id, role='student')

    topics = Topic.objects.all()
    student_words = StudentWord.objects.filter(student=student).select_related('word')

    return render(request, 'vocabulary/teacher_panel.html', {
        'topics': topics,
        'student_words': student_words,
        'student': student,
    })


# vocabulary/views.py - добавляем новую функцию

@login_required
@require_POST
def word_delete_ajax(request):
    """Удаление слова для конкретного ученика"""
    if not request.user.is_teacher():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    try:
        word_id = request.POST.get('word_id')
        student_id = request.POST.get('student_id')

        if not word_id or not student_id:
            return JsonResponse({'success': False, 'error': 'Не указано слово или ученик'})

        word = get_object_or_404(Word, id=word_id)
        student = get_object_or_404(User, id=student_id, role='student')

        # Проверяем, сколько учеников имеют это слово
        student_words_count = StudentWord.objects.filter(word=word).count()

        # Проверяем, есть ли связь у этого ученика
        try:
            student_word = StudentWord.objects.get(word=word, student=student)
        except StudentWord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Слово не назначено этому ученику'})

        # Если слово назначено только этому ученику, удаляем полностью
        if student_words_count == 1:
            word.delete()
            message = 'Слово удалено из базы данных'
        else:
            # Если слово назначено нескольким, отвязываем только от этого ученика
            student_word.delete()
            message = 'Слово отвязано от ученика'

        return JsonResponse({
            'success': True,
            'message': message,
            'deleted_from_db': student_words_count == 1
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```
---

## `vocabulary\__init__.py`

```text

```
---

## `vocabulary\templates\vocabulary\select_student.html`

```text
<!-- vocabulary/templates/vocabulary/select_student.html -->
{% extends 'base.html' %}
{% block title %}Выберите ученика • Словарь{% endblock %}
{% block extra_style %}
	<style>
    .avatar-circle {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }

    .avatar-text {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
    }

    .hover-shadow {
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .hover-shadow:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
    }

    .card-title {
        font-weight: 600;
    }
</style>
{% endblock %}
{% block content %}
<div class="container mt-5">
    <div class="card shadow">
        <div class="card-header bg-primary text-white">
            <h2 class="mb-0">
                <i class="bi bi-people-fill"></i>
                Выберите ученика
            </h2>
        </div>
        <div class="card-body">
            <div class="row">
                {% for student in students %}
                    <div class="col-md-6 col-lg-4 mb-4">
                        <div class="card h-100 border-0 shadow-sm hover-shadow">
                            <div class="card-body text-center">
                                <div class="mb-3">
                                    <div class="avatar-circle mb-3" style="background-color: {% cycle '#3B82F6' '#10B981' '#F59E0B' '#EF4444' '#8B5CF6' %}">
                                        <span class="avatar-text">{{ student.first_name|first|default:"У" }}{{ student.last_name|first|default:"Ч" }}</span>
                                    </div>
                                    <h5 class="card-title">{{ student.get_full_name|default:student.username }}</h5>
                                    <p class="text-muted mb-2">@{{ student.username }}</p>
                                </div>

                                <div class="mb-4">
                                    <div class="row">
                                        <div class="col-6">
                                            <div class="text-center">
                                                <div class="h4 mb-0 text-primary">{{ student.assigned_words.count }}</div>
                                                <small class="text-muted">Слов</small>
                                            </div>
                                        </div>
                                        <div class="col-6">
                                            <div class="text-center">
                                                <div class="h4 mb-0 text-success">{{ student.assigned_words.distinct.count }}</div>
                                                <small class="text-muted">Тем</small>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <a href="{% url 'vocabulary:teacher_panel' student.id %}"
                                   class="btn btn-primary w-100">
                                    <i class="bi bi-arrow-right-circle me-2"></i>
                                    Перейти к словам
                                </a>
                            </div>
                            <div class="card-footer bg-transparent border-top-0 text-center">
                                <small class="text-muted">
                                    Зарегистрирован: {{ student.date_joined|date:"d.m.Y" }}
                                </small>
                            </div>
                        </div>
                    </div>
                {% empty %}
                    <div class="col-12">
                        <div class="alert alert-info text-center py-5">
                            <i class="bi bi-person-x display-4 text-info mb-3"></i>
                            <h4>Нет учеников</h4>
                            <p class="mb-0">В системе пока не зарегистрировано ни одного ученика</p>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
</div>


{% endblock %}
```
---

## `vocabulary\templates\vocabulary\teacher_panel.html`

```text
{% extends 'base.html' %}
{% block title %}Словарь • {{ student.get_full_name|default:student.username }}{% endblock %}
{% block extra_style %}
    <style>
        /* Стили для формы добавления слова */
        .field-focused {
            position: relative;
        }

        .field-focused::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #0d6efd, #198754);
            border-radius: 2px;
        }

        #enter-hint {
            font-size: 0.8rem;
            padding: 0.25rem 0.5rem;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                opacity: 1;
            }
            50% {
                opacity: 0.7;
            }
            100% {
                opacity: 1;
            }
        }

        /* Стили для бейджей */
        #current-topic-badge {
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            transition: all 0.3s ease;
        }

        #current-topic-badge:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        /* Анимация для успешного добавления */
        @keyframes successFlash {
            0% {
                background-color: #d1e7dd;
            }
            50% {
                background-color: #198754;
                color: white;
            }
            100% {
                background-color: #d1e7dd;
            }
        }

        .success-flash {
            animation: successFlash 1s ease;
        }

        /* Стили для аватара */
        .avatar-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .avatar-text {
            color: white;
            font-size: 1rem;
            font-weight: bold;
        }

        /* Подсветка активного поля ввода */
        #add-word-form input:focus, #add-word-form select:focus {
            border-color: #0d6efd;
            box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
        }

        /* Стили для кнопок */
        #add-word-btn:hover {
            transform: scale(1.05);
            transition: transform 0.2s;
        }

        #add-word-btn:active {
            transform: scale(0.95);
        }

        .hover-bg:hover {
            background-color: #f8f9fa;
            transition: background-color 0.2s;
        }

        /* Стили для карточек слов */
        .card.h-100 {
            transition: transform 0.2s;
        }

        .card.h-100:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        /* Стили для выпадающих списков */
        .form-select:focus {
            border-color: #198754;
            box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
        }
    </style>
{% endblock %}
{% block content %}
    <div class="container-fluid">
        <!-- Хлебные крошки и навигация -->
        <nav aria-label="breadcrumb" class="mb-4">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="{% url 'dashboard:teacher' %}">Кабинет учителя</a>
                </li>
                <li class="breadcrumb-item">
                    <a href="{% url 'vocabulary:select_student' %}">Выбор ученика</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page">
                    {{ student.get_full_name|default:student.username }}
                </li>
            </ol>
        </nav>

        <!-- Заголовок с информацией об ученике -->
        <div class="row mb-4">
            <div class="col">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h1 class="h2 mb-1">
                            <i class="bi bi-journal-text text-primary me-2"></i>
                            Словарь ученика
                        </h1>
                        <p class="text-muted mb-0">
                            Работа с учеником:
                            <strong>{{ student.get_full_name|default:student.username }}</strong>
                        </p>
                    </div>
                    <div class="btn-group">
                        <a href="{% url 'vocabulary:create_assignment' student.id %}"
                           class="btn btn-success">
                            <i class="bi bi-plus-circle me-2"></i>
                            Создать задание
                        </a>
                        <a href="{% url 'vocabulary:select_student' %}"
                           class="btn btn-outline-secondary">
                            <i class="bi bi-arrow-left me-2"></i>
                            Сменить ученика
                        </a>
                    </div>
                </div>
            </div>
        </div>


        <div class="row">
            <!-- Левая панель: Темы -->
            <div class="col-lg-4">
                <div class="card shadow mb-4">
                    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="bi bi-tags me-2"></i>
                            Темы
                        </h5>
                        <span class="badge bg-light text-dark">{{ topics.count }}</span>
                    </div>
                    <div class="card-body">
                        <div id="topics-list" class="mb-3" style="max-height: 300px; overflow-y: auto;">
                            {% for topic in topics %}
                                <div class="d-flex justify-content-between align-items-center mb-2 p-2 rounded hover-bg"
                                     style="background-color: {{ topic.color }}20; border-left: 4px solid {{ topic.color }}">
                                    <div>
                                        <strong>{{ topic.name }}</strong>
                                        <br>
                                        <small class="text-muted">
                                            Слов: {{ topic.words.count }}
                                        </small>
                                    </div>
                                    <small class="badge" style="background: {{ topic.color }}">
                                        {{ topic.words.count }}
                                    </small>
                                </div>
                            {% empty %}
                                <div class="text-center py-3">
                                    <i class="bi bi-tag text-muted display-6 mb-3"></i>
                                    <p class="text-muted">Нет созданных тем</p>
                                </div>
                            {% endfor %}
                        </div>

                        <div class="border-top pt-3">
                            <h6 class="mb-3">
                                <i class="bi bi-plus-circle me-2"></i>
                                Создать новую тему
                            </h6>
                            <div class="mb-2">
                                <input type="text" id="new-topic-name" class="form-control form-control-sm"
                                       placeholder="Название темы">
                            </div>
                            <div class="input-group">
                                <input type="color" id="new-topic-color" value="#3B82F6"
                                       class="form-control form-control-color" title="Выберите цвет">
                                <button id="add-topic-btn" class="btn btn-success btn-sm">
                                    <i class="bi bi-plus-lg me-1"></i>
                                    Создать
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Информация об ученике -->
                <div class="card shadow">
                    <div class="card-header bg-info text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-person-circle me-2"></i>
                            Ученик
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="d-flex align-items-center mb-3">
                            <div class="avatar-circle me-3" style="background-color: #3B82F6;">
                                <span class="avatar-text">{{ student.first_name|first|default:"У" }}{{ student.last_name|first|default:"Ч" }}</span>
                            </div>
                            <div>
                                <h6 class="mb-1">{{ student.get_full_name|default:student.username }}</h6>
                                <p class="text-muted mb-0 small">@{{ student.username }}</p>
                            </div>
                        </div>

                        <div class="list-group list-group-flush">
                            <div class="list-group-item d-flex justify-content-between px-0">
                                <span>Дата регистрации</span>
                                <strong>{{ student.date_joined|date:"d.m.Y" }}</strong>
                            </div>
                            <div class="list-group-item d-flex justify-content-between px-0">
                                <span>Назначено слов</span>
                                <strong class="text-primary">{{ student_words.count }}</strong>
                            </div>
                            <div class="list-group-item d-flex justify-content-between px-0">
                                <span>Последний вход</span>
                                <strong>{{ student.last_login|date:"d.m.Y"|default:"Еще не входил" }}</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Правая панель: Слова -->
            <div class="col-lg-8">
                <!-- Добавление слова -->
                <div class="card shadow mb-4">
                    <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="bi bi-plus-circle me-2"></i>
                            Добавить новое слово
                        </h5>
                        <span class="badge bg-light text-dark" id="enter-hint">
            <i class="bi bi-keyboard"></i> Нажмите Enter для добавления
        </span>
                    </div>
                    <div class="card-body">
                        <!-- Скрытое поле с student_id -->
                        <input type="hidden" id="student_id" value="{{ student.id }}">

                        <div class="row g-3" id="add-word-form">
                            <div class="col-md-4">
                                <label class="form-label">Русское слово</label>
                                <input type="text" id="word-russian" class="form-control"
                                       placeholder="Например: собака" required
                                       data-next="word-english">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Английский перевод</label>
                                <input type="text" id="word-english" class="form-control"
                                       placeholder="Например: dog" required
                                       data-next="word-topic">
                            </div>
                            <div class="col-md-4">
                                <label class="form-label">Тема</label>
                                <select id="word-topic" class="form-select" required>
                                    <option value="">Выберите тему</option>
                                    {% for topic in topics %}
                                        <option value="{{ topic.id }}">{{ topic.name }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                        </div>

                        <!-- Информация о текущем выборе -->
                        <div class="row mt-3">
                            <div class="col-12">
                                <div class="form-text" id="current-selections">
                                    <small>
                                        <span id="current-topic-badge" class="badge bg-info me-2"></span>
                                        <span class="badge bg-primary">Ученик: {{ student.get_full_name|default:student.username }}</span>
                                    </small>
                                </div>
                            </div>
                        </div>

                        <div class="mt-2">
                            <span id="form-status" class="text-muted small">
                                Заполните русское и английское слово, выберите тему, затем нажмите Enter.
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Список слов ученика -->
                <div class="card shadow">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="bi bi-list-ul me-2"></i>
                            Слова ученика
                            <span class="badge bg-primary ms-2">{{ student_words.count }}</span>
                        </h5>
                        <div class="dropdown">
                            <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button"
                                    data-bs-toggle="dropdown">
                                <i class="bi bi-filter me-1"></i>
                                Сортировка
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="#" onclick="sortWords('russian')">По русскому</a>
                                </li>
                                <li><a class="dropdown-item" href="#" onclick="sortWords('english')">По английскому</a>
                                </li>
                                <li><a class="dropdown-item" href="#" onclick="sortWords('date')">По дате</a></li>
                            </ul>
                        </div>
                    </div>

                    <div class="card-body">
                        {% if student_words %}
                            <div class="row g-3" id="student-words-list">
                                {% for student_word in student_words %}
                                    <div class="col-md-6 col-lg-4" id="word-{{ student_word.word.id }}">
                                        <div class="card h-100 border">
                                            <div class="card-body">
                                                <div class="d-flex justify-content-between align-items-start mb-2">
                                                    <div>
                                                        <h6 class="card-title mb-1">{{ student_word.word.russian }}</h6>
                                                        <p class="card-text text-primary mb-2">{{ student_word.word.english }}</p>
                                                    </div>
                                                    <button class="btn btn-sm btn-outline-danger delete-word-btn"
                                                            data-word-id="{{ student_word.word.id }}"
                                                            data-student-id="{{ student.id }}"
                                                            title="Удалить слово">
                                                        <i class="bi bi-trash"></i>
                                                    </button>
                                                </div>

                                                {% if student_word.word.topic %}
                                                    <span class="badge mb-2"
                                                          style="background: {{ student_word.word.topic.color }}">
                                                        {{ student_word.word.topic.name }}
                                                    </span>
                                                {% else %}
                                                    <span class="badge bg-secondary mb-2">Без темы</span>
                                                {% endif %}

                                                <div class="text-muted small">
                                                    <i class="bi bi-calendar me-1"></i>
                                                    Добавлено: {{ student_word.assigned_at|date:"d.m.Y" }}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                {% endfor %}
                            </div>
                        {% else %}
                            <div class="text-center py-5">
                                <i class="bi bi-journal-x display-1 text-muted mb-3"></i>
                                <h4>Нет назначенных слов</h4>
                                <p class="text-muted">Добавьте слова для этого ученика с помощью формы выше</p>
                            </div>
                        {% endif %}
                    </div>

                    {% if student_words %}
                        <div class="card-footer bg-transparent">
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">
                                    Показано <strong>{{ student_words.count }}</strong> слов
                                </small>
                                <div>
                                    <button class="btn btn-sm btn-outline-primary" onclick="exportWords()">
                                        <i class="bi bi-download me-1"></i>
                                        Экспорт
                                    </button>
                                </div>
                            </div>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно с результатом удаления -->
    <div class="modal fade" id="deleteResultModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Результат удаления</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="deleteResultMessage">
                    <!-- Сообщение будет вставлено сюда -->
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal">OK</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Получаем ID ученика из скрытого поля
        const STUDENT_ID = document.getElementById('student_id').value;

        // Глобальная функция добавления слова
        function addWord() {
            const russian = document.getElementById('word-russian').value.trim();
            const english = document.getElementById('word-english').value.trim();
            const topic_id = document.getElementById('word-topic').value;

            // Валидация
            if (!russian || !english) {
                showToast('error', 'Ошибка!', 'Заполните русское и английское слово');
                document.getElementById('word-russian').focus();
                return false;
            }
            // Проверка темы
            if (!topic_id) {
                showToast('error', 'Ошибка!', 'Выберите тему для слова');
                document.getElementById('word-topic').focus();
                return false;
            }

            // Показываем индикатор загрузки в статусе формы
            const originalStatus = document.getElementById('form-status').innerHTML;
            document.getElementById('form-status').innerHTML =
                '<span class="text-primary">Добавляем слово...</span>';

            fetch("{% url 'vocabulary:word_create_ajax' %}", {
                method: 'POST',
                headers: {'X-CSRFToken': '{{ csrf_token }}', 'Content-Type': 'application/x-www-form-urlencoded'},
                body: new URLSearchParams({russian, english, topic_id, student_id: STUDENT_ID})
            })
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        // Очищаем только русское и английское поле, ТЕМУ ОСТАВЛЯЕМ!
                        document.getElementById('word-russian').value = '';
                        document.getElementById('word-english').value = '';
                        // Тему НЕ очищаем! Она остается выбранной

                        // Фокус на первое поле
                        document.getElementById('word-russian').focus();

                        // Показываем уведомление
                        showToast('success', 'Успешно!', data.message);

                        // Обновляем статус формы
                        document.getElementById('form-status').innerHTML =
                            `<span class="text-success">Слово успешно добавлено!
                     <br>Тема: ${getSelectedTopicText()}
                     <br>Ученик: {{ student.get_full_name|default:student.username }}</span>`;

                        // Добавляем новое слово в список
                        addWordToList(data.word);

                        // Обновляем счетчик слов
                        updateWordCount();

                        // Через 3 секунды возвращаем стандартный статус
                        setTimeout(() => {
                            updateFormStatus();
                        }, 3000);
                    } else {
                        showToast('error', 'Ошибка!', data.error);
                        document.getElementById('form-status').innerHTML =
                            `<span class="text-danger">Ошибка: ${data.error}</span>`;

                        // Через 3 секунды возвращаем стандартный статус
                        setTimeout(() => {
                            document.getElementById('form-status').innerHTML = originalStatus;
                        }, 3000);
                    }
                })
                .catch(error => {
                    showToast('error', 'Ошибка!', 'Произошла ошибка при отправке');
                    document.getElementById('form-status').innerHTML =
                        '<span class="text-danger">Ошибка сети</span>';

                    // Через 3 секунды возвращаем стандартный статус
                    setTimeout(() => {
                        document.getElementById('form-status').innerHTML = originalStatus;
                    }, 3000);
                });

            return false;
        }

        // Функция для получения текста выбранной темы
        function getSelectedTopicText() {
            const topicSelect = document.getElementById('word-topic');
            const selectedOption = topicSelect.options[topicSelect.selectedIndex];
            return selectedOption ? selectedOption.text : 'Не выбрана';
        }

        // Обработчик нажатия Enter
        function handleEnterKey(e, currentFieldId) {
            if (e.key === 'Enter') {
                e.preventDefault();

                // Проверяем заполненность всех обязательных полей
                const russian = document.getElementById('word-russian').value.trim();
                const english = document.getElementById('word-english').value.trim();
                const topic_id = document.getElementById('word-topic').value;

                if (russian && english && topic_id) {
                    addWord();
                } else {
                    // Если не все заполнено, переходим к следующему полю
                    const currentField = document.getElementById(currentFieldId);
                    const nextFieldId = currentField.getAttribute('data-next');

                    if (nextFieldId) {
                        const nextField = document.getElementById(nextFieldId);
                        if (nextField) {
                            nextField.focus();

                            // Если это select, открываем список
                            if (nextField.tagName === 'SELECT') {
                                nextField.click();
                            }
                        }
                    } else {
                        // Если нет следующего поля, показываем, что нужно заполнить
                        if (!russian) {
                            document.getElementById('word-russian').focus();
                            showToast('warning', 'Внимание!', 'Введите русское слово');
                        } else if (!english) {
                            document.getElementById('word-english').focus();
                            showToast('warning', 'Внимание!', 'Введите английский перевод');
                        } else if (!topic_id) {
                            document.getElementById('word-topic').focus();
                            showToast('warning', 'Внимание!', 'Выберите тему');
                        }
                    }
                }
            }
        }

        function updateFormStatus() {
            const russian = document.getElementById('word-russian').value.trim();
            const english = document.getElementById('word-english').value.trim();
            const topic_id = document.getElementById('word-topic').value;

            if (russian && english && topic_id) {
                document.getElementById('enter-hint').innerHTML =
                    '<i class="bi bi-keyboard-fill"></i> Нажмите Enter для добавления';
                document.getElementById('form-status').innerHTML =
                    `Все поля заполнены, нажмите Enter для добавления
         <br>Тема: ${getSelectedTopicText()}
         <br>Ученик: {{ student.get_full_name|default:student.username }}`;
            } else {
                document.getElementById('enter-hint').innerHTML =
                    '<i class="bi bi-keyboard"></i> Enter для перехода между полями';
                const missingFields = [];
                if (!russian) missingFields.push('русское слово');
                if (!english) missingFields.push('английское слово');
                if (!topic_id) missingFields.push('тему');

                document.getElementById('form-status').innerHTML =
                    `Заполните: ${missingFields.join(', ')}
         <br>Тема: ${getSelectedTopicText()}
         <br>Ученик: {{ student.get_full_name|default:student.username }}`;
            }
        }

        // Функция для обновления бейджей текущих настроек
        function updateSelectionBadges() {
            const topicBadge = document.getElementById('current-topic-badge');
            const topicSelect = document.getElementById('word-topic');

            // Тема
            const selectedTopic = topicSelect.options[topicSelect.selectedIndex];
            if (selectedTopic && selectedTopic.value) {
                topicBadge.textContent = `Тема: ${selectedTopic.text}`;
                topicBadge.className = 'badge bg-info me-2';
                topicBadge.style.display = 'inline';
            } else {
                topicBadge.textContent = 'Тема не выбрана';
                topicBadge.className = 'badge bg-secondary me-2';
                topicBadge.style.display = 'inline';
            }
        }

        // Вешаем обработчики на поля ввода
        document.getElementById('word-russian').addEventListener('keydown', function (e) {
            handleEnterKey(e, 'word-russian');
        });

        document.getElementById('word-english').addEventListener('keydown', function (e) {
            handleEnterKey(e, 'word-english');
        });

        document.getElementById('word-topic').addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                addWord();
            }
        });

        // Горячие клавиши
        document.addEventListener('keydown', function (e) {
            // Escape - очистка всех полей формы
            if (e.key === 'Escape' && document.activeElement.matches('#word-russian, #word-english, #word-topic')) {
                e.preventDefault();
                document.getElementById('word-russian').value = '';
                document.getElementById('word-english').value = '';
                document.getElementById('word-topic').value = '';
                document.getElementById('word-russian').focus();

                // Показываем уведомление
                showToast('info', 'Форма очищена', 'Все поля сброшены');

                // Обновляем статус
                updateFormStatus();
                updateSelectionBadges();
            }

            // Ctrl + Enter - принудительное добавление (пропуская валидацию)
            if (e.ctrlKey && e.key === 'Enter' && document.activeElement.matches('#word-russian, #word-english, #word-topic')) {
                e.preventDefault();
                addWord();
            }
        });

        // Вспомогательные функции
        function addWordToList(wordData) {
            const wordsList = document.getElementById('student-words-list');
            if (!wordsList) return;

            const wordHtml = `
        <div class="col-md-6 col-lg-4" id="word-${wordData.id}">
            <div class="card h-100 border">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <h6 class="card-title mb-1">${wordData.russian}</h6>
                            <p class="card-text text-primary mb-2">${wordData.english}</p>
                        </div>
                        <button class="btn btn-sm btn-outline-danger delete-word-btn"
                                data-word-id="${wordData.id}"
                                data-student-id="${STUDENT_ID}"
                                title="Удалить слово">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>

                    ${wordData.topic ? `<span class="badge mb-2" style="background: ${wordData.topic_color}">${wordData.topic}</span>` : '<span class="badge bg-secondary mb-2">Без темы</span>'}

                    <div class="text-muted small">
                        <i class="bi bi-calendar me-1"></i>
                        Только что добавлено
                    </div>
                </div>
            </div>
        </div>
    `;

            wordsList.insertAdjacentHTML('afterbegin', wordHtml);
        }

        function updateWordCount() {
            const wordsCount = document.querySelectorAll('#student-words-list .col-md-6').length;
            const counter = document.querySelector('.card-header h5 .badge');
            if (counter) {
                counter.textContent = wordsCount;
            }

            // Обновляем статистику
            const statCard = document.querySelector('.card.border-primary .card-body h3');
            if (statCard) {
                statCard.textContent = wordsCount;
            }
        }

        // Функция для показа уведомлений
        function showToast(type, title, message) {
            // Создаем элемент тоста
            const toastHTML = `
        <div class="toast show align-items-center text-bg-${type} border-0 position-fixed"
             style="top: 20px; right: 20px; z-index: 1050;">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${type === 'success' ? 'bi-check-circle' : type === 'error' ? 'bi-x-circle' : type === 'warning' ? 'bi-exclamation-triangle' : 'bi-info-circle'} me-2"></i>
                    <strong>${title}</strong>: ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto"
                        onclick="this.closest('.toast').remove()"></button>
            </div>
        </div>
    `;

            // Удаляем старые тосты
            document.querySelectorAll('.toast').forEach(toast => toast.remove());

            // Добавляем новый тост
            document.body.insertAdjacentHTML('beforeend', toastHTML);

            // Автоматически скрываем через 3 секунды
            setTimeout(() => {
                document.querySelector('.toast')?.remove();
            }, 3000);
        }

        // Обработчик для удаления слов
        document.addEventListener('click', function (e) {
            if (e.target.closest('.delete-word-btn')) {
                const button = e.target.closest('.delete-word-btn');
                const wordId = button.getAttribute('data-word-id');
                const studentId = button.getAttribute('data-student-id');

                if (confirm('Удалить это слово у ученика?')) {
                    fetch("{% url 'vocabulary:word_delete_ajax' %}", {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': '{{ csrf_token }}',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        body: `word_id=${wordId}&student_id=${studentId}`
                    })
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                // Удаляем элемент из DOM
                                document.getElementById(`word-${wordId}`).remove();
                                showToast('success', 'Успешно!', data.message);
                                updateWordCount();
                            } else {
                                showToast('error', 'Ошибка!', data.error);
                            }
                        });
                }
            }
        });
        // Инициализация при загрузке страницы
        document.addEventListener('DOMContentLoaded', function () {
            // Инициализируем бейджи и статус
            updateSelectionBadges();
            updateFormStatus();

            // Автофокус на поле русского слова
            setTimeout(() => {
                const russianField = document.getElementById('word-russian');
                if (russianField) russianField.focus();
            }, 100);
        });
        // Обработчик для создания новой темы
        document.getElementById('add-topic-btn').addEventListener('click', function () {
            const name = document.getElementById('new-topic-name').value.trim();
            const color = document.getElementById('new-topic-color').value;

            if (!name) {
                showToast('error', 'Ошибка!', 'Введите название темы');
                return;
            }

            // Показываем индикатор загрузки
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            this.disabled = true;

            fetch("{% url 'vocabulary:topic_create_ajax' %}", {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `name=${encodeURIComponent(name)}&color=${encodeURIComponent(color)}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showToast('success', 'Успешно!', 'Тема создана');

                        // Очищаем поле ввода
                        document.getElementById('new-topic-name').value = '';

                        // Добавляем тему в список тем в левой панели
                        addTopicToList(data.topic);

                        // Добавляем тему в выпадающий список формы
                        addTopicToSelect(data.topic);

                        // Выбираем новую тему в форме
                        document.getElementById('word-topic').value = data.topic.id;

                        // Обновляем статус формы
                        updateFormStatus();
                        updateSelectionBadges();
                    } else {
                        showToast('error', 'Ошибка!', data.error);
                    }
                })
                .catch(error => {
                    showToast('error', 'Ошибка!', 'Ошибка сети');
                })
                .finally(() => {
                    // Восстанавливаем кнопку
                    this.innerHTML = originalText;
                    this.disabled = false;
                });
        });

        // Функция для добавления темы в список в левой панели
        function addTopicToList(topic) {
            const topicsList = document.getElementById('topics-list');

            // Если есть сообщение "Нет созданных тем", удаляем его
            const emptyMessage = topicsList.querySelector('.text-center');
            if (emptyMessage) {
                emptyMessage.remove();
            }

            const topicElement = document.createElement('div');
            topicElement.className = 'd-flex justify-content-between align-items-center mb-2 p-2 rounded hover-bg';
            topicElement.style = `background-color: ${topic.color}20; border-left: 4px solid ${topic.color}`;
            topicElement.innerHTML = `
            <div>
                <strong>${topic.name}</strong>
                <br>
                <small class="text-muted">
                    Слов: 0
                </small>
            </div>
            <small class="badge" style="background: ${topic.color}">
                0
            </small>
        `;

            topicsList.appendChild(topicElement);
        }

        // Функция для добавления темы в выпадающий список формы
        function addTopicToSelect(topic) {
            const select = document.getElementById('word-topic');
            const option = document.createElement('option');
            option.value = topic.id;
            option.textContent = topic.name;
            select.appendChild(option);
        }

        // Также обновим форму для создания тем - добавим обработчик Enter
        document.getElementById('new-topic-name').addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('add-topic-btn').click();
            }
        });
    </script>


{% endblock %}
```
---

## `vocabulary\templates\vocabulary\word_create.html`

```text
{% extends 'base.html' %}
{% block title %}Добавить слово{% endblock %}

{% block content %}
    <div class="container-fluid">
        <div class="row">
            <!-- Левая панель: быстрый выбор ученика и темы -->
            <div class="col-lg-3">
                <div class="card shadow mb-4">
                    <div class="card-header bg-primary text-white">
                        <h5 class="mb-0">Быстрый выбор</h5>
                    </div>
                    <div class="card-body">
                        <!-- Выбор ученика -->
                        <div class="mb-4">
                            <label class="form-label fw-bold">Ученик</label>
                            <div class="list-group">
                                {% for s in students %}
                                    <a href="?student_id={{ s.id }}{% if topic %}&topic_id={{ topic.id }}{% endif %}"
                                       class="list-group-item list-group-item-action {% if student and student.id == s.id %}active{% endif %}">
                                        {{ s.get_full_name|default:s.username }}
                                    </a>
                                {% endfor %}
                            </div>
                        </div>

                        <!-- Выбор темы -->
                        <div class="mb-4">
                            <label class="form-label fw-bold">Тема</label>
                            <div class="list-group">
                                <a href="?{% if student %}student_id={{ student.id }}{% endif %}"
                                   class="list-group-item list-group-item-action {% if not topic %}active{% endif %}">
                                    Без темы
                                </a>
                                {% for t in topics %}
                                    <a href="?{% if student %}student_id={{ student.id }}&{% endif %}topic_id={{ t.id }}"
                                       class="list-group-item list-group-item-action {% if topic and topic.id == t.id %}active{% endif %}"
                                       style="border-left: 4px solid {{ t.color }};">
                                        {{ t.name }}
                                    </a>
                                {% endfor %}
                            </div>
                        </div>

                        <!-- Создать новую тему -->
                        <div class="mt-4">
                            <button class="btn btn-outline-primary w-100" data-bs-toggle="modal"
                                    data-bs-target="#newTopicModal">
                                + Новая тема
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Быстрая статистика -->
                {% if student %}
                    <div class="card shadow">
                        <div class="card-header bg-info text-white">
                            <h6 class="mb-0">Статистика</h6>
                        </div>
                        <div class="card-body">
                            <p class="mb-1">
                                <strong>{{ student.get_full_name|default:student.username }}</strong>
                            </p>
                            <p class="mb-0 text-muted">
                                Слов назначено: <strong>{{ student.assigned_words.count }}</strong>
                            </p>
                        </div>
                    </div>
                {% endif %}
            </div>

            <!-- Правая панель: добавление слов -->
            <div class="col-lg-9">
                <div class="card shadow">
                    <div class="card-header bg-success text-white d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Добавить новое слово</h5>
                        {% if student %}
                            <span class="badge bg-light text-dark fs-6">
                            Ученик: {{ student.get_full_name|default:student.username }}
                        </span>
                        {% endif %}
                    </div>
                    <div class="card-body">
                        {% if not student %}
                            <div class="alert alert-warning">
                                <strong>Выберите ученика</strong> в левой панели, чтобы начать добавлять слова.
                            </div>
                        {% else %}
                            <!-- Форма быстрого добавления -->
                            <form id="quickAddForm" method="post" class="mb-4">
                                {% csrf_token %}
                                <div class="row g-3 align-items-end">
                                    <div class="col-md-4">
                                        <label class="form-label">Русское слово</label>
                                        <input type="text"
                                               name="russian"
                                               class="form-control form-control-lg"
                                               placeholder="собака"
                                               required
                                               autofocus>
                                    </div>
                                    <div class="col-md-4">
                                        <label class="form-label">Английский перевод</label>
                                        <input type="text"
                                               name="english"
                                               class="form-control form-control-lg"
                                               placeholder="dog"
                                               required>
                                    </div>
                                    <div class="col-md-3">
                                        <label class="form-label">Тема (опционально)</label>
                                        <select name="topic_id" class="form-select">
                                            <!-- ИЗМЕНИТЬ: topic → topic_id -->
                                            <option value="">Без темы</option>
                                            {% for t in topics %}
                                                <option value="{{ t.id }}"
                                                        {% if topic and topic.id == t.id %}selected{% endif %}>
                                                    {{ t.name }}
                                                </option>
                                            {% endfor %}
                                        </select>
                                    </div>
                                    <div class="col-md-1">
                                        <button type="submit" class="btn btn-primary btn-lg w-100">
                                            <i class="bi bi-plus-lg"></i>
                                        </button>
                                    </div>
                                </div>
                                <input type="hidden" name="student_id" value="{{ student.id }}">
                                <!-- ИЗМЕНИТЬ: student → student_id -->
                            </form>

                            <!-- Последние добавленные слова -->
                            {% if recent_words %}
                                <div class="mt-5">
                                    <h6>Последние добавленные слова для этого ученика:</h6>
                                    <div class="row g-2">
                                        {% for sw in recent_words %}
                                            <div class="col-md-4 col-lg-3">
                                                <div class="border rounded p-2">
                                                    <div class="d-flex justify-content-between">
                                                        <strong>{{ sw.word.russian }}</strong>
                                                        <span class="text-primary">{{ sw.word.english }}</span>
                                                    </div>
                                                    {% if sw.word.topic %}
                                                        <small class="badge"
                                                               style="background: {{ sw.word.topic.color }}">
                                                            {{ sw.word.topic.name }}
                                                        </small>
                                                    {% endif %}
                                                </div>
                                            </div>
                                        {% endfor %}
                                    </div>
                                </div>
                            {% endif %}
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Модальное окно для новой темы -->
    <div class="modal fade" id="newTopicModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Создать новую тему</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <form id="newTopicForm">
                        <div class="mb-3">
                            <label class="form-label">Название темы</label>
                            <input type="text" class="form-control" id="newTopicName" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Цвет темы</label>
                            <input type="color" class="form-control form-control-color" id="newTopicColor"
                                   value="#3B82F6">
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                    <button type="button" class="btn btn-primary" id="createTopicBtn">Создать</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        // AJAX отправка формы
        document.getElementById('quickAddForm').addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;

            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
            submitBtn.disabled = true;

            fetch("{% url 'vocabulary:word_create_ajax' %}", {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Ответ сервера:', data);  // Для отладки
                    if (data.success) {
                        // Очищаем поля ввода
                        this.querySelector('input[name="russian"]').value = '';
                        this.querySelector('input[name="english"]').value = '';
                        this.querySelector('input[name="russian"]').focus();

                        // Показываем уведомление
                        const toastHTML = `
                <div class="toast show align-items-center text-bg-success border-0 position-fixed"
                     style="top: 20px; right: 20px; z-index: 1050;">
                    <div class="d-flex">
                        <div class="toast-body">
                            <i class="bi bi-check-circle me-2"></i>
                            ${data.message}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto"
                                data-bs-dismiss="toast"></button>
                    </div>
                </div>
            `;

                        // Удаляем старые тосты
                        document.querySelectorAll('.toast').forEach(toast => toast.remove());

                        // Добавляем новый тост
                        document.body.insertAdjacentHTML('beforeend', toastHTML);

                        // Автоматически скрываем через 3 секунды
                        setTimeout(() => {
                            document.querySelector('.toast')?.remove();
                        }, 3000);

                        // Обновляем список последних слов, если нужно
                        if (data.word) {
                            // Динамически добавляем новое слово в список последних слов
                            const recentWordsContainer = document.querySelector('.row.g-2');
                            if (recentWordsContainer) {
                                const wordHTML = `
                        <div class="col-md-4 col-lg-3">
                            <div class="border rounded p-2">
                                <div class="d-flex justify-content-between">
                                    <strong>${data.word.russian}</strong>
                                    <span class="text-primary">${data.word.english}</span>
                                </div>
                                ${data.word.topic ? `
                                <small class="badge" style="background: ${data.word.topic_color}">
                                    ${data.word.topic}
                                </small>
                                ` : ''}
                            </div>
                        </div>
                    `;
                                recentWordsContainer.insertAdjacentHTML('afterbegin', wordHTML);
                            }
                        }
                    } else {
                        // Показываем ошибку
                        alert(`Ошибка: ${data.error}`);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Произошла ошибка при отправке');
                })
                .finally(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                });
        });

        // Создание темы через AJAX
        document.getElementById('createTopicBtn').addEventListener('click', function () {
            const name = document.getElementById('newTopicName').value.trim();
            const color = document.getElementById('newTopicColor').value;

            if (!name) {
                alert('Введите название темы');
                return;
            }

            fetch("{% url 'vocabulary:topic_create_ajax' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: `name=${encodeURIComponent(name)}&color=${encodeURIComponent(color)}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Закрываем модальное и обновляем страницу
                        bootstrap.Modal.getInstance(document.getElementById('newTopicModal')).hide();
                        location.reload();
                    } else {
                        alert('Ошибка: ' + (data.error || 'Не удалось создать тему'));
                    }
                });
        });

        // Функция для показа уведомлений
        function showToast(type, title, message) {
            // Простая реализация - можно заменить на Bootstrap Toast
            alert(`${title}: ${message}`);
        }
    </script>
{% endblock %}
```
---

