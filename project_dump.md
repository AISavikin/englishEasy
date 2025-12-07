# 📁 Дерево проекта

```
- ./
    - get_project_dump.py
    - manage.py
    - words_aisav.json
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
    - exercises/
        - admin.py
        - forms.py
        - models.py
        - urls.py
        - utils.py
        - views.py
        - templates/
            - exercises/
                - create.html
                - delete_confirm.html
                - detail.html
                - drag_and_drop.html
                - letter_soup.html
                - list.html
                - my.html
                - progress.html
                - spelling.html
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
    - vocabulary/
        - admin.py
        - apps.py
        - forms.py
        - models.py
        - tests.py
        - urls.py
        - views.py
        - views_api.py
        - __init__.py
        - management/
            - commands/
                - add_words_interactive.py
                - list_students.py
        - templates/
            - vocabulary/
                - select_student.html
                - student_words.html
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

## `words_aisav.json`

```text
[
  {
    "russian": "яблоко",
    "english": "apple",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "банан",
    "english": "banana",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "апельсин",
    "english": "orange",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "виноград",
    "english": "grape",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "клубника",
    "english": "strawberry",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "помидор",
    "english": "tomato",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "огурец",
    "english": "cucumber",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "морковь",
    "english": "carrot",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "картофель",
    "english": "potato",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "лук",
    "english": "onion",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "рис",
    "english": "rice",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "хлеб",
    "english": "bread",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "сыр",
    "english": "cheese",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "молоко",
    "english": "milk",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "вода",
    "english": "water",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "чай",
    "english": "tea",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "кофе",
    "english": "coffee",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "мясо",
    "english": "meat",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "рыба",
    "english": "fish",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "курица",
    "english": "chicken",
    "topic": "Еда",
    "topic_color": "#FF6B6B"
  },
  {
    "russian": "собака",
    "english": "dog",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "кошка",
    "english": "cat",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "лошадь",
    "english": "horse",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "корова",
    "english": "cow",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "свинья",
    "english": "pig",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "овца",
    "english": "sheep",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "коза",
    "english": "goat",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "кролик",
    "english": "rabbit",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "мышь",
    "english": "mouse",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "птица",
    "english": "bird",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "утка",
    "english": "duck",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "гусь",
    "english": "goose",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "тигр",
    "english": "tiger",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "лев",
    "english": "lion",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "слон",
    "english": "elephant",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "жираф",
    "english": "giraffe",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "медведь",
    "english": "bear",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "волк",
    "english": "wolf",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "лиса",
    "english": "fox",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "заяц",
    "english": "hare",
    "topic": "Животные",
    "topic_color": "#4ECDC4"
  },
  {
    "russian": "мама",
    "english": "mother",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "папа",
    "english": "father",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "брат",
    "english": "brother",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "сестра",
    "english": "sister",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "сын",
    "english": "son",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "дочь",
    "english": "daughter",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "дедушка",
    "english": "grandfather",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "бабушка",
    "english": "grandmother",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "дядя",
    "english": "uncle",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "тётя",
    "english": "aunt",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "племянник",
    "english": "nephew",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "племянница",
    "english": "niece",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "внук",
    "english": "grandson",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "внучка",
    "english": "granddaughter",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "муж",
    "english": "husband",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "жена",
    "english": "wife",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "родители",
    "english": "parents",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "дети",
    "english": "children",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "семья",
    "english": "family",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "родственник",
    "english": "relative",
    "topic": "Семья",
    "topic_color": "#FFD166"
  },
  {
    "russian": "красный",
    "english": "red",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "синий",
    "english": "blue",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "зелёный",
    "english": "green",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "жёлтый",
    "english": "yellow",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "чёрный",
    "english": "black",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "белый",
    "english": "white",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "оранжевый",
    "english": "orange",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "фиолетовый",
    "english": "purple",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "розовый",
    "english": "pink",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "коричневый",
    "english": "brown",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "серый",
    "english": "grey",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "голубой",
    "english": "light blue",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "золотой",
    "english": "gold",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "серебряный",
    "english": "silver",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "бирюзовый",
    "english": "turquoise",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "бордовый",
    "english": "burgundy",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "бежевый",
    "english": "beige",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "салатовый",
    "english": "lime",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "сиреневый",
    "english": "lilac",
    "topic": "Цвета",
    "topic_color": "#06D6A0"
  },
  {
    "russian": "счастье",
    "english": "happiness",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "грусть",
    "english": "sadness",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "радость",
    "english": "joy",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "гнев",
    "english": "anger",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "страх",
    "english": "fear",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "удивление",
    "english": "surprise",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "любовь",
    "english": "love",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "ненависть",
    "english": "hate",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "спокойствие",
    "english": "calm",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "волнение",
    "english": "excitement",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "разочарование",
    "english": "disappointment",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "надежда",
    "english": "hope",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "гордость",
    "english": "pride",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "стыд",
    "english": "shame",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "ревность",
    "english": "jealousy",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "зависть",
    "english": "envy",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "смущение",
    "english": "embarrassment",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "облегчение",
    "english": "relief",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "удовлетворение",
    "english": "satisfaction",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  },
  {
    "russian": "благодарность",
    "english": "gratitude",
    "topic": "Эмоции",
    "topic_color": "#118AB2"
  }
]
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
from datetime import timedelta, date

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from users.models import User
from vocabulary.models import StudentWord, Topic
from exercises.models import Exercise  # Добавляем импорт


@login_required
def home(request):
    if request.user.is_teacher():
        return redirect('dashboard:teacher')
    return redirect('dashboard:student')


@login_required
def teacher_dashboard(request):
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    students = User.objects.filter(role='student')

    # Подсчитываем общее количество слов для статистики
    total_words = 0
    active_today_count = 0
    today = date.today()

    for student in students:
        total_words += student.assigned_words.count()
        if student.last_login and student.last_login.date() == today:
            active_today_count += 1

    context = {
        'students': students,
        'total_words': total_words,
        'active_today_count': active_today_count,
        'today': today,
    }

    return render(request, 'dashboard/teacher.html', context)


@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('dashboard:home')

    assigned_words = StudentWord.objects.filter(student=request.user)

    recent_words = assigned_words.order_by('-assigned_at')[:10]
    # Статистика по словам
    stats = {
        'total': assigned_words.count(),
        'new': assigned_words.filter(status='new').count(),
        'learning': assigned_words.filter(status='learning').count(),
        'review': assigned_words.filter(status='review').count(),
        'completed': assigned_words.filter(status='completed').count(),
    }


    # Активные задания (не выполненные и не проверенные)
    assignments = Exercise.objects.filter(
        student=request.user
    ).exclude(
        status__in=['completed', 'graded']
    ).order_by('due_date', '-created_at')[:5]  # Ограничиваем 5 заданиями

    # Прогресс по темам
    topics_with_progress = []
    for topic in Topic.objects.all():
        words_in_topic = assigned_words.filter(word__topic=topic)
        if words_in_topic.exists():
            total_words = words_in_topic.count()
            learned_words = words_in_topic.filter(status='completed').count()

            topics_with_progress.append({
                'id': topic.id,
                'name': topic.name,
                'color': topic.color,
                'total': total_words,
                'learned': learned_words,
                'percent': int((learned_words / total_words) * 100) if total_words > 0 else 0
            })



    context = {
        'stats': stats,
        'assignments': assignments,
        'topics_with_progress': topics_with_progress,
        'recent_words': recent_words,
    }
    return render(request, 'dashboard/student.html', context)
```
---

## `dashboard\__init__.py`

```text

```
---

## `dashboard\templates\dashboard\student.html`

```text
{% extends 'base.html' %}
{% block title %}Мой кабинет{% endblock %}

{% block extra_style %}
    <style>
        .stat-card {
            border-radius: 15px;
            transition: transform 0.2s;
            border: none;
        }

        .stat-card:hover {
            transform: translateY(-5px);
        }

        .progress-circle {
            width: 120px;
            height: 120px;
            margin: 0 auto;
        }

        .word-card {
            border-left: 4px solid;
            transition: all 0.2s;
        }

        .word-card:hover {
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        .status-new {
            border-left-color: #3B82F6;
        }

        .status-learning {
            border-left-color: #10B981;
        }

        .status-review {
            border-left-color: #F59E0B;
        }

        .status-completed {
            border-left-color: #8B5CF6;
        }
    </style>
{% endblock %}

{% block content %}
    <div class="container-fluid">
        <!-- Приветствие -->
        <div class="row mb-4">
            <div class="col">
                <h1 class="h2 mb-1">Привет, {{ user.first_name|default:"Ученик" }}!</h1>
                <p class="text-muted">Вот твой прогресс в изучении английских слов</p>
            </div>

        </div>

        <!-- Статистика -->
        <div class="row mb-4">
            <div class="col-md-2 mb-3">
                <div class="card stat-card bg-primary text-white">
                    <div class="card-body text-center">
                        <div class="h1 mb-0">{{ stats.total }}</div>
                        <p class="mb-0">Всего слов</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card stat-card bg-info text-white">
                    <div class="card-body text-center">
                        <div class="h1 mb-0">{{ assignments.count }}</div>
                        <p class="mb-0">Заданий</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card stat-card bg-warning text-white">
                    <div class="card-body text-center">
                        <div class="h1 mb-0">{{ stats.new }}</div>
                        <p class="mb-0">Новых слов</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card stat-card bg-warning text-white">
                    <div class="card-body text-center">
                        <div class="h1 mb-0">{{ stats.learning }}</div>
                        <p class="mb-0">В изучении</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card stat-card bg-success text-white">
                    <div class="card-body text-center">
                        <div class="h1 mb-0">{{ stats.completed }}</div>
                        <p class="mb-0">Изучено</p>
                    </div>
                </div>
            </div>
            <div class="col-md-2 mb-3">
                <div class="card stat-card bg-danger text-white">
                    <div class="card-body text-center">
                        <div class="h1 mb-0">{{ assignments|length }}</div>
                        <p class="mb-0">Активных заданий</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Две колонки -->
        <div class="row">
            <!-- Левая колонка: Повторение и задания -->
            <div class="col-lg-4">


                <!-- Активные задания -->
                {% if assignments %}
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-info text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-journal-check me-2"></i>
                                Активные задания
                            </h5>
                        </div>
                        <div class="card-body">
                            {% for assignment in assignments %}
                                <div class="card mb-2 border-info">
                                    <div class="card-body py-2">
                                        <h6 class="card-title mb-1">{{ assignment.get_exercise_type_display }}</h6>
                                        <small class="text-muted d-block">
                                            <i class="bi bi-calendar me-1"></i>
                                            {% if assignment.due_date %}
                                                До {{ assignment.due_date|date:"d.m.Y" }}
                                            {% else %}
                                                Без срока
                                            {% endif %}
                                        </small>
                                        <small class="text-muted d-block">
                                            <i class="bi bi-list-ul me-1"></i>
                                            Тип: {{ assignment.get_exercise_type_display }}
                                        </small>
                                        <a href="{% url 'exercises:do_exercise' assignment.id %}"
                                           class="btn btn-sm btn-info mt-2">Начать задание</a>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                {% endif %}
            </div>

            <!-- Правая колонка: Все слова и прогресс -->
            <div class="col-lg-8">
                <!-- Прогресс по темам -->
                {% if topics_with_progress %}
                    <div class="card shadow-sm mb-4">
                        <div class="card-header">
                            <h5 class="mb-0">Прогресс по темам</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                {% for topic in topics_with_progress %}
                                    <div class="col-md-6 mb-3">
                                        <div class="d-flex justify-content-between mb-1">
                                            <span><i class="bi bi-circle-fill me-2"
                                                     style="color: {{ topic.color }}"></i>{{ topic.name }}</span>
                                            <span>{{ topic.learned }}/{{ topic.total }}</span>
                                        </div>
                                        <div class="progress" style="height: 8px;">
                                            <div class="progress-bar" role="progressbar"
                                                 style="width: {{ topic.percent }}%; background: {{ topic.color }}"></div>
                                        </div>
                                        <small class="text-muted d-block mt-1">{{ topic.percent }}% изучено</small>
                                    </div>
                                {% endfor %}
                            </div>
                        </div>
                    </div>
                {% endif %}

                <!-- Недавние слова -->
                <div class="card shadow-sm">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Недавние слова</h5>
                        <a href="{% url 'vocabulary:student_words' %}" class="btn btn-sm btn-outline-primary">
                            Все слова
                        </a>
                    </div>
                    <div class="card-body">
                        <div class="row" id="wordsList">
                            {% for sw in recent_words %}
                                <div class="col-md-6 col-lg-4 mb-3">
                                    <div class="card word-card status-{{ sw.status }}">
                                        <div class="card-body">
                                            <div class="d-flex justify-content-between align-items-start">
                                                <div>
                                                    <h6 class="card-title mb-1">{{ sw.word.russian }}</h6>
                                                    <p class="card-text text-primary mb-2">{{ sw.word.english }}</p>
                                                </div>
                                                <div class="dropdown">
                                                    <button class="btn btn-sm btn-outline-secondary"
                                                            type="button" data-bs-toggle="dropdown">
                                                        <i class="bi bi-three-dots"></i>
                                                    </button>
                                                    <ul class="dropdown-menu">
                                                        <li><a class="dropdown-item change-status"
                                                               data-status="new" data-word-id="{{ sw.id }}">Новое</a>
                                                        </li>
                                                        <li><a class="dropdown-item change-status"
                                                               data-status="learning" data-word-id="{{ sw.id }}">Изучается</a>
                                                        </li>
                                                        <li><a class="dropdown-item change-status"
                                                               data-status="completed" data-word-id="{{ sw.id }}">Изучено</a>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </div>

                                            {% if sw.word.topic %}
                                                <span class="badge mb-2" style="background: {{ sw.word.topic.color }}">
                                        {{ sw.word.topic.name }}
                                    </span>
                                            {% endif %}

                                            <div class="d-flex justify-content-between align-items-center mt-2">

                                                <span class="badge bg-{{ sw.status }}">
                                            {{ sw.get_status_display }}
                                        </span>
                                            </div>


                                        </div>
                                    </div>
                                </div>
                            {% empty %}
                                <div class="col-12 text-center py-5">
                                    <i class="bi bi-journal-x display-1 text-muted mb-3"></i>
                                    <h4>Нет назначенных слов</h4>
                                    <p class="text-muted">Ваш учитель ещё не добавил слова для изучения</p>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            // Изменение статуса слова
            document.querySelectorAll('.change-status').forEach(btn => {
                btn.addEventListener('click', function () {
                    const wordId = this.getAttribute('data-word-id');
                    const status = this.getAttribute('data-status');

                    fetch('{% url "vocabulary:update_word_status" %}', {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': '{{ csrf_token }}',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({word_id: wordId, status: status})
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                location.reload();
                            } else {
                                alert('Ошибка: ' + data.error);
                            }
                        })
                        .catch(error => {
                            alert('Ошибка сети');
                        });
                });
            });
        });
    </script>
{% endblock %}
```
---

## `dashboard\templates\dashboard\teacher.html`

```text
{% extends 'base.html' %}
{% block title %}Кабинет учителя{% endblock %}
{% block extra_style %}
	<style>
.avatar-circle {
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.avatar-text {
    color: white;
    font-weight: bold;
}

#studentsTable tbody tr:hover {
    background-color: rgba(0, 0, 0, 0.02);
    cursor: pointer;
}

#studentsTable tbody tr {
    transition: background-color 0.2s;
}
</style>

{% endblock %}
{% block content %}
<div class="container-fluid mt-4">
    <div class="row mb-4">
        <div class="col">
            <h1 class="h2 mb-1">Кабинет учителя</h1>
            <p class="text-muted">Управление учениками и отслеживание их прогресса</p>
        </div>
        <div class="col-auto">
            <a href="{% url 'vocabulary:select_student' %}" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i>Добавить слова ученику
            </a>
        </div>
    </div>

    {% if students %}
    <div class="row">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">
                        <i class="bi bi-people-fill me-2"></i>
                        Мои ученики
                        <span class="badge bg-primary ms-2">{{ students.count }}</span>
                    </h5>
                    <div class="dropdown">
                        <button class="btn btn-sm btn-outline-secondary dropdown-toggle" type="button"
                                data-bs-toggle="dropdown">
                            <i class="bi bi-sort-down me-1"></i>Сортировка
                        </button>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" onclick="sortStudents('name')">По имени</a></li>
                            <li><a class="dropdown-item" href="#" onclick="sortStudents('date')">По дате регистрации</a></li>
                            <li><a class="dropdown-item" href="#" onclick="sortStudents('words')">По количеству слов</a></li>
                        </ul>
                    </div>
                </div>

                <div class="card-body">
                    <div class="table-responsive">
                        <table class="table table-hover" id="studentsTable">
                            <thead>
                                <tr>
                                    <th>Ученик</th>
                                    <th>Дата регистрации</th>
                                    <th>Назначено слов</th>
                                    <th>Последний вход</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for student in students %}
                                <tr>
                                    <td>
                                        <div class="d-flex align-items-center">
                                            <div class="avatar-circle me-3" style="background-color: {% cycle '#3B82F6' '#10B981' '#F59E0B' '#EF4444' '#8B5CF6' %}; width: 40px; height: 40px;">
                                                <span class="avatar-text" style="font-size: 1rem;">
                                                    {{ student.first_name|first|default:"У" }}{{ student.last_name|first|default:"Ч" }}
                                                </span>
                                            </div>
                                            <div>
                                                <strong>{{ student.get_full_name|default:student.username }}</strong>
                                                <div class="text-muted small">@{{ student.username }}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td>{{ student.date_joined|date:"d.m.Y" }}</td>
                                    <td>
                                        <span class="badge bg-primary">
                                            {{ student.assigned_words.count }} слов
                                        </span>
                                    </td>
                                    <td>
                                        {% if student.last_login %}
                                            {{ student.last_login|date:"d.m.Y H:i" }}
                                        {% else %}
                                            <span class="text-muted">Еще не входил</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <div class="btn-group btn-group-sm">
                                            <a href="{% url 'vocabulary:teacher_panel' student.id %}"
                                               class="btn btn-outline-primary" title="Управление словами">
                                                <i class="bi bi-journal-text"></i>
                                            </a>
                                            <a href="{% url 'exercises:create_exercise_for_student' student.id %}"
                                               class="btn btn-outline-success" title="Создать задание">
                                                <i class="bi bi-journal-plus"></i>
                                            </a>
                                            <a href="{% url 'exercises:teacher_exercises_for_student' student.id %}"
                                               class="btn btn-outline-info" title="Просмотр заданий">
                                                <i class="bi bi-list-check"></i>
                                            </a>
                                        </div>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <!-- Быстрая статистика -->
            <div class="card shadow mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">
                        <i class="bi bi-graph-up me-2"></i>Статистика
                    </h5>
                </div>
                <div class="card-body">
                    <div class="list-group list-group-flush">
                        <div class="list-group-item d-flex justify-content-between align-items-center px-0">
                            <span>Всего учеников</span>
                            <strong class="text-primary">{{ students.count }}</strong>
                        </div>
                        <div class="list-group-item d-flex justify-content-between align-items-center px-0">
                            <span>Активных сегодня</span>
                            <strong class="text-success">{{ active_today_count }}</strong>
                        </div>
                        <div class="list-group-item d-flex justify-content-between align-items-center px-0">
                            <span>Всего назначено слов</span>
                            <strong>{{ total_words }}</strong>
                        </div>
                        <div class="list-group-item d-flex justify-content-between align-items-center px-0">
                            <span>Создано заданий</span>
                            <strong class="text-info">
                                {{ request.user.created_exercises.count }}
                            </strong>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Быстрые действия -->
            <div class="card shadow">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">
                        <i class="bi bi-lightning-fill me-2"></i>Быстрые действия
                    </h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{% url 'vocabulary:select_student' %}" class="btn btn-primary">
                            <i class="bi bi-journal-plus me-2"></i>Добавить слова ученику
                        </a>
                        <a href="{% url 'exercises:create_exercise' %}" class="btn btn-success">
                            <i class="bi bi-journal-check me-2"></i>Создать упражнение
                        </a>
                        <a href="{% url 'exercises:teacher_exercises' %}" class="btn btn-info">
                            <i class="bi bi-list-task me-2"></i>Все упражнения
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% else %}
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow text-center py-5">
                <div class="card-body">
                    <i class="bi bi-people display-1 text-muted mb-4"></i>
                    <h3>Пока нет учеников</h3>
                    <p class="text-muted mb-4">
                        В системе еще не зарегистрированы ученики.
                        Как только ученики зарегистрируются, они появятся здесь.
                    </p>
                    <div class="d-grid gap-2 col-md-8 mx-auto">
                        <a href="{% url 'users:home' %}" class="btn btn-primary">
                            <i class="bi bi-house me-2"></i>На главную
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    {% endif %}
</div>


<script>
document.addEventListener('DOMContentLoaded', function() {
    // Сортировка таблицы
    function sortStudents(criteria) {
        const table = document.getElementById('studentsTable');
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const aCells = a.querySelectorAll('td');
            const bCells = b.querySelectorAll('td');

            switch(criteria) {
                case 'name':
                    const aName = aCells[0].querySelector('strong').textContent.toLowerCase();
                    const bName = bCells[0].querySelector('strong').textContent.toLowerCase();
                    return aName.localeCompare(bName);
                case 'date':
                    const aDate = new Date(aCells[1].textContent.split('.').reverse().join('-'));
                    const bDate = new Date(bCells[1].textContent.split('.').reverse().join('-'));
                    return aDate - bDate;
                case 'words':
                    const aWords = parseInt(aCells[2].querySelector('.badge').textContent);
                    const bWords = parseInt(bCells[2].querySelector('.badge').textContent);
                    return bWords - aWords;
                default:
                    return 0;
            }
        });

        // Очищаем и добавляем отсортированные строки
        tbody.innerHTML = '';
        rows.forEach(row => tbody.appendChild(row));
    }

    // Экспортируем функцию в глобальную область видимости
    window.sortStudents = sortStudents;

    // Клик по строке ведет на страницу ученика
    document.querySelectorAll('#studentsTable tbody tr').forEach(row => {
        const link = row.querySelector('a[href*="teacher_panel"]');
        if (link) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(e) {
                if (!e.target.closest('a, button')) {
                    window.location.href = link.href;
                }
            });
        }
    });
});
</script>
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
    'exercises'
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
    path('exercises/', include('exercises.urls')),
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

## `exercises\admin.py`

```text
from django.contrib import admin
from .models import Exercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise_type', 'student', 'teacher', 'assignment_type', 'status', 'due_date')
    list_filter = ('assignment_type', 'exercise_type', 'status', 'teacher', 'student')
    search_fields = ('description', 'student__username', 'teacher__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('description', 'student', 'teacher')
        }),
        ('Типы и статус', {
            'fields': ('assignment_type', 'exercise_type', 'status')
        }),
        ('Попытки', {
            'fields': ('attempts',)
        }),
        ('Даты', {
            'fields': ('due_date', 'completed_at', 'created_at', 'updated_at')
        }),
        ('Данные', {
            'fields': ('exercise_data', 'teacher_comment')
        }),
    )
```
---

## `exercises\forms.py`

```text
from django import forms
from .models import Exercise
from users.models import User
from vocabulary.models import Word
from .utils import generate_letter_soup
import json


class ExerciseCreateForm(forms.ModelForm):
    # Поле для выбора слов (множественный выбор)
    word_selection = forms.MultipleChoiceField(
        choices=[],
        widget=forms.MultipleHiddenInput(),
        required=True,
        error_messages={'required': 'Выберите хотя бы одно слово'}
    )

    class Meta:
        model = Exercise
        fields = [
            'description', 'student',
            'assignment_type', 'exercise_type',
            'due_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Например: Найдите слова в буквенном супе'
            }),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'exercise_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        if teacher:
            # Ограничиваем выбор учеников только теми, кто связан с этим учителем
            self.fields['student'].queryset = User.objects.filter(role='student')

        # Динамически установим choices для word_selection
        if 'student' in self.initial and self.initial['student']:
            self.set_word_choices(self.initial['student'])

    def set_word_choices(self, student):
        """Установить choices для поля word_selection"""
        if isinstance(student, int):
            student_id = student
        else:
            student_id = student.id

        # Получаем слова, назначенные ученику
        assigned_words = Word.objects.filter(
            studentword__student_id=student_id
        ).distinct()

        # Формируем choices
        choices = [(word.id, f"{word.russian} - {word.english}")
                   for word in assigned_words]
        self.fields['word_selection'].choices = choices

    def clean(self):
        cleaned_data = super().clean()

        # Проверяем, что выбраны слова
        word_selection = cleaned_data.get('word_selection')
        if not word_selection:
            self.add_error('word_selection', 'Выберите хотя бы одно слово')

        return cleaned_data

    def save(self, commit=True):
        exercise = super().save(commit=False)
        teacher = self.initial.get('teacher')
        if teacher:
            exercise.teacher = teacher

        # Формируем данные упражнения из выбранных слов
        selected_word_ids = self.cleaned_data.get('word_selection', [])

        # Получаем объекты слов
        words = Word.objects.filter(id__in=selected_word_ids)

        # Формируем пары слов
        pairs = []
        english_words = []

        for word in words:
            pairs.append({
                'russian': word.russian,
                'english': word.english.lower()
            })
            english_words.append(word.english.lower())

        # Формируем exercise_data в зависимости от типа упражнения
        exercise_type = self.cleaned_data['exercise_type']

        if exercise_type in ['spelling', 'drag_and_drop']:
            exercise.exercise_data = {
                'pairs': pairs,
                'instructions': self.cleaned_data.get('description', '')
            }
        elif exercise_type == 'letter_soup':
            # Генерируем буквенный суп с автоматическим расчетом размера сетки
            grid, placed_words = generate_letter_soup(english_words)  # grid_size=None по умолчанию

            exercise.exercise_data = {
                'pairs': pairs,
                'english_words': english_words,
                'grid': grid,
                'placed_words': placed_words,
                'grid_size': len(grid),  # динамический размер
                'instructions': self.cleaned_data.get('description', '') or 'Найдите английские слова в сетке'
            }

        if commit:
            exercise.save()

        return exercise
```
---

## `exercises\models.py`

```text
from django.db import models
from django.conf import settings
from django.utils import timezone

import json


class Exercise(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [
        ('homework', 'Домашняя работа'),
        ('classwork', 'Работа на уроке'),
        ('test', 'Контрольная работа'),
    ]

    EXERCISE_TYPE_CHOICES = [
        ('spelling', 'Правописание (Spelling)'),
        ('drag_and_drop', 'Перетаскивание (Drag and Drop)'),
        ('letter_soup', 'Буквенный суп (Letter Soup)'),
    ]

    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('graded', 'Проверено'),
    ]

    # Основные поля (без title)
    description = models.TextField('Описание', blank=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exercises',
        limit_choices_to={'role': 'student'},
        verbose_name='Ученик'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_exercises',
        limit_choices_to={'role': 'teacher'},
        verbose_name='Учитель'
    )

    # Типы
    assignment_type = models.CharField(
        'Тип задания',
        max_length=20,
        choices=ASSIGNMENT_TYPE_CHOICES,
        default='homework'
    )
    exercise_type = models.CharField(
        'Вид упражнения',
        max_length=20,
        choices=EXERCISE_TYPE_CHOICES,
        default='spelling'
    )

    # Статус и попытки
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )
    attempts = models.IntegerField('Количество попыток', default=0)

    # Данные упражнения
    exercise_data = models.JSONField('Данные упражнения', default=dict)

    # Даты
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    completed_at = models.DateTimeField('Завершено', null=True, blank=True)

    # Результаты
    teacher_comment = models.TextField('Комментарий учителя', blank=True)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_exercise_type_display()} - {self.student} ({self.created_at.date()})"

    def is_overdue(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False

    def start_attempt(self):
        """Начать новую попытку выполнения"""
        if self.status == 'not_started':
            self.attempts += 1
            self.status = 'in_progress'
            self.save()

    def complete_attempt(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
```
---

## `exercises\urls.py`

```text
from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    # Создание упражнения
    path('create/', views.create_exercise, name='create_exercise'),
    path('create/<int:student_id>/', views.create_exercise, name='create_exercise_for_student'),

    # Просмотр списков
    path('teacher/', views.teacher_exercises_list, name='teacher_exercises'),
    path('teacher/<int:student_id>/', views.teacher_exercises_list, name='teacher_exercises_for_student'),
    path('my/', views.student_exercises_list, name='my_exercises'),

    # Детали упражнения
    path('detail/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),

    # Действия с упражнением
    path('do/<int:exercise_id>/', views.do_exercise, name='do_exercise'),
    path('complete/<int:exercise_id>/', views.complete_exercise, name='complete_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('update_status/<int:exercise_id>/', views.update_exercise_status, name='update_exercise_status'),
]
```
---

## `exercises\utils.py`

```text
import random
import string
from typing import List, Tuple, Dict, Set


def calculate_grid_size(words: List[str]) -> int:
    """
    Автоматически рассчитывает оптимальный размер сетки на основе слов.

    Args:
        words: Список английских слов

    Returns:
        int: Оптимальный размер сетки
    """
    if not words:
        return 10  # минимальный размер по умолчанию

    # Параметры для расчета
    max_word_length = max(len(word) for word in words)
    word_count = len(words)
    total_letters = sum(len(word) for word in words)

    # Базовый расчет на основе самой длинного слова
    base_size = max(max_word_length + 2, 8)  # +2 для отступов, минимум 8

    # Учитываем количество слов
    if word_count > 10:
        base_size += 2
    if word_count > 20:
        base_size += 3
    if word_count > 30:
        base_size += 2

    # Учитываем общее количество букв
    density_factor = total_letters / (base_size ** 2)
    if density_factor > 0.25:  # слишком плотно
        base_size = int(base_size * 1.2)

    # Ограничиваем диапазоном
    min_size = 8
    max_size = 25

    # Особые случаи
    if max_word_length > 15:
        base_size = max(base_size, max_word_length + 3)

    # Округляем до ближайшего нечетного числа (для центрирования)
    base_size = int(base_size)
    if base_size % 2 == 0:
        base_size += 1

    # Применяем ограничения
    return max(min_size, min(base_size, max_size))

def generate_letter_soup(words: List[str], grid_size = None) -> Tuple[List[List[str]], List[Dict]]:
    """
    Генерирует буквенный суп (сетку с словами).

    Args:
        words: Список английских слов
        grid_size: Размер сетки (grid_size x grid_size)

    Returns:
        Tuple[grid, placed_words]:
            grid: Двумерный список букв
            placed_words: Информация о размещенных словах
    """
    if grid_size is None:
        grid_size = calculate_grid_size(words)

    # Инициализируем пустую сетку
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

    # Преобразуем слова в верхний регистр
    words_upper = [word.upper() for word in words]

    # Сортируем слова по длине (от самых длинных к самым коротким)
    words_upper.sort(key=len, reverse=True)

    placed_words = []

    # Преобразуем слова в верхний регистр
    words = [word.upper() for word in words]

    # Сортируем слова по длине (от самых длинных к самым коротким)
    words.sort(key=len, reverse=True)

    for word in words:
        placed = False
        attempts = 0
        max_attempts = 100

        while not placed and attempts < max_attempts:
            attempts += 1

            # Выбираем случайное направление: горизонтальное или вертикальное
            direction = random.choice(['horizontal', 'vertical'])

            if direction == 'horizontal':
                # Для горизонтального слова
                max_row = grid_size
                max_col = grid_size - len(word) + 1
                if max_col <= 0:
                    continue  # Слово слишком длинное

                row = random.randint(0, max_row - 1)
                col = random.randint(0, max_col - 1)

                # Проверяем, можно ли разместить слово
                can_place = True
                for i, letter in enumerate(word):
                    current_cell = grid[row][col + i]
                    if current_cell != '' and current_cell != letter:
                        can_place = False
                        break

                if can_place:
                    # Размещаем слово
                    for i, letter in enumerate(word):
                        grid[row][col + i] = letter

                    placed_words.append({
                        'word': word,
                        'row': row,
                        'col': col,
                        'direction': direction,
                        'length': len(word)
                    })
                    placed = True

            else:  # vertical
                # Для вертикального слова
                max_row = grid_size - len(word) + 1
                max_col = grid_size
                if max_row <= 0:
                    continue  # Слово слишком длинное

                row = random.randint(0, max_row - 1)
                col = random.randint(0, max_col - 1)

                # Проверяем, можно ли разместить слово
                can_place = True
                for i, letter in enumerate(word):
                    current_cell = grid[row + i][col]
                    if current_cell != '' and current_cell != letter:
                        can_place = False
                        break

                if can_place:
                    # Размещаем слово
                    for i, letter in enumerate(word):
                        grid[row + i][col] = letter

                    placed_words.append({
                        'word': word,
                        'row': row,
                        'col': col,
                        'direction': direction,
                        'length': len(word)
                    })
                    placed = True

        if not placed:
            print(f"Не удалось разместить слово: {word}")

    # Заполняем пустые клетки случайными буквами
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid, placed_words


def validate_word_in_grid(word: str, grid: List[List[str]], placed_words: List[Dict]) -> bool:
    """
    Проверяет, есть ли слово в сетке.

    Args:
        word: Слово для проверки (в верхнем регистре)
        grid: Сетка букв
        placed_words: Информация о размещенных словах

    Returns:
        True если слово есть в сетке, иначе False
    """
    word = word.upper()

    # Проверяем по списку размещенных слов
    for placed_word in placed_words:
        if placed_word['word'] == word:
            return True

    # Также проверяем, можно ли найти слово в сетке (на случай, если алгоритм размещения не записал его)
    grid_size = len(grid)

    # Проверяем горизонтально
    for i in range(grid_size):
        for j in range(grid_size - len(word) + 1):
            found = True
            for k in range(len(word)):
                if grid[i][j + k] != word[k]:
                    found = False
                    break
            if found:
                return True

    # Проверяем вертикально
    for i in range(grid_size - len(word) + 1):
        for j in range(grid_size):
            found = True
            for k in range(len(word)):
                if grid[i + k][j] != word[k]:
                    found = False
                    break
            if found:
                return True

    return False


def get_grid_preview(grid: List[List[str]]) -> str:
    """
    Возвращает текстовое представление сетки.
    """
    return '\n'.join([' '.join(row) for row in grid])
```
---

## `exercises\views.py`

```text
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from .models import Exercise
from .forms import ExerciseCreateForm
from users.models import User
import json


@login_required
def create_exercise(request, student_id=None):
    """Создание упражнения для ученика"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    # Если передан student_id, получаем ученика
    student = None
    if student_id:
        student = get_object_or_404(User, id=student_id, role='student')

    if request.method == 'POST':
        print("=" * 50)
        print("POST запрос получен")
        print(f"POST данные: {dict(request.POST)}")
        print("=" * 50)

        form = ExerciseCreateForm(
            request.POST,
            teacher=request.user,
            initial={'teacher': request.user}
        )

        # Если выбран ученик, устанавливаем choices для слов
        if 'student' in request.POST and request.POST['student']:
            form.set_word_choices(int(request.POST['student']))

        if form.is_valid():
            print("Форма валидна!")
            exercise = form.save(commit=False)
            exercise.teacher = request.user
            exercise.save()

            messages.success(request, f'Упражнение типа "{exercise.get_exercise_type_display()}" создано!')

            # Редирект на панель учителя для этого ученика
            return redirect('vocabulary:teacher_panel', student_id=exercise.student.id)
        else:
            print("Форма невалидна!")
            print(f"Ошибки формы: {form.errors}")
            print(f"Ошибки полей: {form.errors.as_data()}")
            # Если форма не валидна, показываем ошибки
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        initial = {'teacher': request.user}
        if student:
            initial['student'] = student

        form = ExerciseCreateForm(initial=initial, teacher=request.user)

        # Если есть ученик, устанавливаем choices для его слов
        if student:
            form.set_word_choices(student)

    return render(request, 'exercises/create.html', {
        'form': form,
        'student': student,
        'students': User.objects.filter(role='student')
    })

@login_required
def teacher_exercises_list(request, student_id=None):
    """Список упражнений для учителя"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    # Фильтруем упражнения, созданные текущим учителем
    exercises = Exercise.objects.filter(teacher=request.user)

    # Если указан ученик, фильтруем по нему
    if student_id:
        student = get_object_or_404(User, id=student_id, role='student')
        exercises = exercises.filter(student=student)
    else:
        student = None

    # Группируем по ученикам для общего списка
    students_with_exercises = []
    if not student_id:
        students = User.objects.filter(
            role='student',
            exercises__teacher=request.user
        ).distinct()

        for s in students:
            student_exercises = exercises.filter(student=s)
            students_with_exercises.append({
                'student': s,
                'exercises': student_exercises,
                'count': student_exercises.count(),
                'completed': student_exercises.filter(status='completed').count(),
                'graded': student_exercises.filter(status='graded').count(),
            })

    return render(request, 'exercises/list.html', {
        'exercises': exercises,
        'student': student,
        'students_with_exercises': students_with_exercises,
        'show_student_column': not student_id,
    })


@login_required
def student_exercises_list(request):
    """Список упражнений для ученика"""
    if not request.user.is_student():
        return redirect('dashboard:home')

    exercises = Exercise.objects.filter(student=request.user)

    return render(request, 'exercises/my.html', {
        'exercises': exercises,
        'now': timezone.now(),
    })


@login_required
def exercise_detail(request, exercise_id):
    """Детальная страница упражнения"""
    exercise = get_object_or_404(Exercise, id=exercise_id)

    # Проверка прав доступа
    if not (request.user == exercise.student or request.user == exercise.teacher):
        messages.error(request, 'У вас нет доступа к этому упражнению')
        return redirect('dashboard:home')

    return render(request, 'exercises/detail.html', {
        'exercise': exercise,
        'is_teacher': request.user.is_teacher(),
        'is_student': request.user.is_student(),
    })


# Добавим новую функцию для выполнения упражнения
# В функции do_exercise добавим обработку drag_and_drop
@login_required
def do_exercise(request, exercise_id):
    """Выполнение упражнения (объединенная функция)"""
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if not request.user == exercise.student:
        messages.error(request, 'Только ученик может выполнять это упражнение')
        return redirect('dashboard:home')

    # Проверяем статус
    if exercise.status in ['completed', 'graded']:
        messages.warning(request, 'Задание уже выполнено или проверено')
        return redirect('exercises:my_exercises')

    # Если упражнение еще не начато, начинаем попытку
    if exercise.status == 'not_started':
        exercise.start_attempt()

    # Далее отображаем форму в зависимости от типа упражнения
    exercise_data = exercise.exercise_data

    if exercise.exercise_type == 'spelling':
        pairs = exercise_data.get('pairs', [])
        words = [{'russian': p['russian'], 'english': p['english']} for p in pairs]
        return render(request, 'exercises/spelling.html', {
            'exercise': exercise,
            'words': words,
        })

    elif exercise.exercise_type == 'drag_and_drop':
        pairs = exercise_data.get('pairs', [])
        words = [{'russian': p['russian'], 'english': p['english']} for p in pairs]
        return render(request, 'exercises/drag_and_drop.html', {
            'exercise': exercise,
            'words': words,
        })

    elif exercise.exercise_type == 'letter_soup':
        pairs = exercise_data.get('pairs', [])
        english_words = exercise_data.get('english_words', [])
        grid = exercise_data.get('grid', [])
        placed_words = exercise_data.get('placed_words', [])
        grid_size = exercise_data.get('grid_size', 15)

        return render(request, 'exercises/letter_soup.html', {
            'exercise': exercise,
            'pairs': pairs,
            'english_words': english_words,
            'grid': grid,
            'placed_words': placed_words,
            'grid_size': grid_size,
        })

    messages.error(request, 'Этот тип упражнения пока не поддерживается')
    return redirect('exercises:exercise_detail', exercise_id=exercise.id)


# Обновим функцию start_exercise


# Добавим функцию для завершения упражнения
@login_required
def complete_exercise(request, exercise_id):
    """Завершить упражнение"""
    if request.method == 'POST':
        exercise = get_object_or_404(Exercise, id=exercise_id)

        if not request.user == exercise.student:
            return JsonResponse({'success': False, 'error': 'Только ученик может завершать упражнение'})

        exercise.complete_attempt()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})

@login_required
def delete_exercise(request, exercise_id):
    """Удаление упражнения"""
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if not request.user == exercise.teacher:
        messages.error(request, 'Только создавший учитель может удалить упражнение')
        return redirect('dashboard:home')

    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'Упражнение удалено')
        return redirect('exercises:teacher_exercises')

    # Для GET запроса - просто редиректим на список упражнений
    return redirect('exercises:teacher_exercises')


@login_required
def update_exercise_status(request, exercise_id):
    """AJAX обновление статуса упражнения"""
    if request.method == 'POST' and request.user.is_teacher():
        exercise = get_object_or_404(Exercise, id=exercise_id)

        if request.user != exercise.teacher:
            return JsonResponse({'success': False, 'error': 'Нет прав'})

        new_status = request.POST.get('status')
        if new_status in dict(Exercise.STATUS_CHOICES).keys():
            exercise.status = new_status
            exercise.save()
            return JsonResponse({'success': True, 'new_status': exercise.get_status_display()})

    return JsonResponse({'success': False, 'error': 'Неверный запрос'})
```
---

## `exercises\templates\exercises\create.html`

```text
{% extends 'base.html' %}
{% block title %}Создание упражнения{% endblock %}

{% block extra_style %}
<style>
    /* Стили для выбора слов */
    #words-container {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 10px;
        background-color: #f8f9fa;
    }

    .word-checkbox {
        margin-right: 8px;
    }

    .word-item {
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 5px;
        background-color: white;
        border: 1px solid #e9ecef;
        transition: all 0.2s;
        cursor: pointer;
    }

    .word-item:hover {
        background-color: #f8f9fa;
        border-color: #0d6efd;
    }

    .word-item.selected {
        background-color: rgba(13, 110, 253, 0.1);
        border-color: #0d6efd;
    }

    .word-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .word-text {
        font-size: 1rem;
    }

    .word-topic {
        font-size: 0.8rem;
        padding: 2px 8px;
        border-radius: 10px;
    }

    /* Заголовок с количеством выбранных слов */
    #selected-count {
        font-size: 0.9rem;
        color: #0d6efd;
        font-weight: bold;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="bi bi-plus-circle me-2"></i>
                        Создать новое упражнение
                        {% if student %}
                            для {{ student.get_full_name|default:student.username }}
                        {% endif %}
                    </h4>
                </div>

                <div class="card-body">
                    <form method="post" id="exerciseForm">
                        {% csrf_token %}

                        <!-- Основные поля формы -->
                        {{ form.non_field_errors }}

                        <div class="row g-3">
                            <!-- Левая колонка: Основная информация -->
                            <div class="col-md-6">
                                <h5 class="mb-3 text-primary">Основная информация</h5>

                                <div class="mb-3">
                                    <label class="form-label">Описание</label>
                                    {{ form.description }}
                                    {% if form.description.errors %}
                                        <div class="text-danger small">{{ form.description.errors }}</div>
                                    {% endif %}
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Ученик *</label>
                                    {{ form.student }}
                                    {% if form.student.errors %}
                                        <div class="text-danger small">{{ form.student.errors }}</div>
                                    {% endif %}
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Тип задания *</label>
                                    {{ form.assignment_type }}
                                    {% if form.assignment_type.errors %}
                                        <div class="text-danger small">{{ form.assignment_type.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>

                            <!-- Правая колонка: Дополнительные параметры -->
                            <div class="col-md-6">
                                <h5 class="mb-3 text-primary">Дополнительные параметры</h5>

                                <div class="mb-3">
                                    <label class="form-label">Вид упражнения *</label>
                                    {{ form.exercise_type }}
                                    {% if form.exercise_type.errors %}
                                        <div class="text-danger small">{{ form.exercise_type.errors }}</div>
                                    {% endif %}
                                    <div class="form-text">
                                        <small id="exercise-type-hint"></small>
                                    </div>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Срок выполнения</label>
                                    {{ form.due_date }}
                                    <div class="form-text">Оставьте пустым, если срок не ограничен</div>
                                    {% if form.due_date.errors %}
                                        <div class="text-danger small">{{ form.due_date.errors }}</div>
                                    {% endif %}
                                </div>

                                <div class="mb-3 form-check">
                                    {{ form.use_assigned_words }}
                                    <label class="form-check-label" for="{{ form.use_assigned_words.id_for_label }}">
                                        {{ form.use_assigned_words.label }}
                                    </label>
                                </div>
                            </div>
                        </div>

                        <!-- Выбор слов -->
                        <div class="mt-4">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h5 class="mb-0 text-primary">Выбор слов *</h5>
                                <span id="selected-count" class="badge bg-primary">Выбрано: 0 слов</span>
                            </div>

                            <!-- Кнопки управления выбором -->
                            <div class="mb-3">
                                <div class="btn-group" role="group">
                                    <button type="button" class="btn btn-outline-primary btn-sm" id="select-all">
                                        <i class="bi bi-check-all me-1"></i>Выбрать все
                                    </button>
                                    <button type="button" class="btn btn-outline-secondary btn-sm" id="deselect-all">
                                        <i class="bi bi-x-circle me-1"></i>Снять все
                                    </button>
                                </div>
                            </div>

                            <!-- Контейнер для слов -->
                            <div id="words-container">
                                <div class="text-center py-5" id="loading-words">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Загрузка...</span>
                                    </div>
                                    <p class="mt-2">Загружаем слова...</p>
                                </div>

                                <div id="words-list" style="display: none;">
                                    <!-- Слова будут загружены через AJAX -->
                                </div>

                                <div id="no-words-message" class="text-center py-5" style="display: none;">
                                    <i class="bi bi-journal-x display-4 text-muted mb-3"></i>
                                    <h5>Нет слов</h5>
                                    <p class="text-muted">
                                        {% if student %}
                                            У этого ученика пока нет назначенных слов.
                                            <br>
                                            <a href="{% url 'vocabulary:teacher_panel' student.id %}" class="btn btn-sm btn-primary mt-2">
                                                Добавить слова
                                            </a>
                                        {% else %}
                                            Выберите ученика, чтобы увидеть его слова.
                                        {% endif %}
                                    </p>
                                </div>

                                <div id="error-message" class="alert alert-danger" style="display: none;">
                                    <!-- Сообщения об ошибках -->
                                </div>
                            </div>

                            <!-- Скрытые поля для выбранных слов -->
                            <div id="selected-words-input">
                                <!-- JavaScript добавит скрытые поля здесь -->
                            </div>

                            {% if form.word_selection.errors %}
                                <div class="alert alert-danger mt-2">
                                    {{ form.word_selection.errors }}
                                </div>
                            {% endif %}

                            <div class="form-text mt-2">
                                <small>
                                    <i class="bi bi-info-circle me-1"></i>
                                    Выберите слова для упражнения. Минимум 1 слово.
                                </small>
                            </div>
                        </div>

                        <!-- Статистика выбранных слов -->
                        <div class="mt-4" id="words-stats" style="display: none;">
                            <h6 class="mb-3">Статистика выбранных слов:</h6>
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="stats-card">
                                        <div class="h5 mb-1" id="stats-total">0</div>
                                        <small class="text-muted">Всего слов</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="stats-card" style="border-left-color: #198754;">
                                        <div class="h5 mb-1" id="stats-unique-topics">0</div>
                                        <small class="text-muted">Тем</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="stats-card" style="border-left-color: #fd7e14;">
                                        <div class="h5 mb-1" id="stats-letters">0</div>
                                        <small class="text-muted">Средняя длина</small>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Кнопки отправки -->
                        <div class="mt-4">
                            <button type="submit" class="btn btn-primary btn-lg" id="submit-btn">
                                <i class="bi bi-save me-2"></i> Создать упражнение
                            </button>
                            <a href="{% if student %}{% url 'vocabulary:teacher_panel' student.id %}{% else %}{% url 'dashboard:teacher' %}{% endif %}"
                               class="btn btn-secondary btn-lg ms-2">
                                Отмена
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
// Глобальные переменные
let allWords = [];
let selectedWordIds = new Set();

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM загружен');

    // Получаем элемент выбора ученика
    const studentSelect = document.getElementById('{{ form.student.id_for_label }}');

    // Если есть ученик по умолчанию, загружаем его слова
    const defaultStudentId = studentSelect.value;
    if (defaultStudentId) {
        loadStudentWords(defaultStudentId);
    }

    // Обработчик изменения ученика
    studentSelect.addEventListener('change', function() {
        console.log('Ученик изменен:', this.value);
        const studentId = this.value;
        if (studentId) {
            loadStudentWords(studentId);
        } else {
            showNoWordsMessage();
            disableSubmitButton();
        }
    });

    // Обработчик изменения типа упражнения
    const exerciseTypeSelect = document.getElementById('{{ form.exercise_type.id_for_label }}');
    updateExerciseTypeHint(exerciseTypeSelect.value);
    exerciseTypeSelect.addEventListener('change', function() {
        updateExerciseTypeHint(this.value);
    });

    // Кнопки управления выбором
    document.getElementById('select-all').addEventListener('click', selectAllWords);
    document.getElementById('deselect-all').addEventListener('click', deselectAllWords);

    // Обработчик отправки формы
    document.getElementById('exerciseForm').addEventListener('submit', function(e) {
        console.log('Форма отправляется');
        console.log('Выбранные слова:', Array.from(selectedWordIds));

        // Проверяем, что выбраны слова
        if (selectedWordIds.size === 0) {
            e.preventDefault();
            showError('Пожалуйста, выберите хотя бы одно слово для упражнения');
            return false;
        }

        // Проверяем, что выбран ученик
        if (!studentSelect.value) {
            e.preventDefault();
            showError('Пожалуйста, выберите ученика');
            return false;
        }

        // Обновляем скрытые поля перед отправкой
        updateSelectedWordsInput();

        // Проверяем, что скрытые поля добавлены
        const hiddenInputs = document.querySelectorAll('input[name="word_selection"]');
        console.log('Скрытые поля перед отправкой:', hiddenInputs.length);

        return true;
    });

    // Включаем кнопку отправки изначально
    enableSubmitButton();
});

function loadStudentWords(studentId) {
    console.log('Загрузка слов для ученика:', studentId);

    // Показываем индикатор загрузки
    document.getElementById('loading-words').style.display = 'block';
    document.getElementById('words-list').style.display = 'none';
    document.getElementById('no-words-message').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';

    // Очищаем текущий выбор
    allWords = [];
    selectedWordIds.clear();
    updateSelectedCount();
    updateSelectedWordsInput(); // Очищаем скрытые поля

    // Загружаем слова ученика через AJAX
    fetch(`/vocabulary/api/student/${studentId}/words/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            console.log('Данные получены:', data);
            document.getElementById('loading-words').style.display = 'none';

            if (data.success && data.words && data.words.length > 0) {
                allWords = data.words;
                renderWordsList();
                showWordsList();
                enableSubmitButton();
            } else {
                showNoWordsMessage();
                disableSubmitButton();
            }
        })
        .catch(error => {
            console.error('Ошибка загрузки слов:', error);
            document.getElementById('loading-words').style.display = 'none';
            showError('Ошибка загрузки слов: ' + error.message);
            disableSubmitButton();
        });
}

function renderWordsList() {
    const wordsList = document.getElementById('words-list');
    wordsList.innerHTML = '';

    allWords.forEach(word => {
        const wordItem = document.createElement('div');
        wordItem.className = 'word-item';
        wordItem.dataset.wordId = word.id;

        // Проверяем, выбрано ли слово
        const isSelected = selectedWordIds.has(word.id.toString());

        // Создаем элемент для слова с меткой (label)
        wordItem.innerHTML = `
            <div class="word-info">
                <div>
                    <input type="checkbox"
                           class="word-checkbox"
                           id="word-${word.id}"
                           value="${word.id}"
                           ${isSelected ? 'checked' : ''}>
                    <label for="word-${word.id}" class="word-text">
                        <strong>${word.russian}</strong> →
                        <span class="text-primary">${word.english}</span>
                    </label>
                </div>
                ${word.topic ? `
                    <span class="word-topic" style="background-color: ${word.topic_color}20; color: ${word.topic_color}">
                        ${word.topic}
                    </span>
                ` : ''}
            </div>
        `;

        // Обработчик изменения чекбокса
        const checkbox = wordItem.querySelector('.word-checkbox');
        checkbox.addEventListener('change', function(e) {
            e.stopPropagation();
            const isChecked = this.checked;
            const wordId = this.value;

            console.log('Чекбокс изменен:', wordId, isChecked);

            if (isChecked) {
                selectedWordIds.add(wordId);
            } else {
                selectedWordIds.delete(wordId);
            }

            // Обновляем стиль элемента
            if (isChecked) {
                wordItem.classList.add('selected');
            } else {
                wordItem.classList.remove('selected');
            }

            updateSelectedCount();
            updateStats();
            updateSelectedWordsInput();

            // Включаем или выключаем кнопку отправки
            if (selectedWordIds.size > 0) {
                enableSubmitButton();
            } else {
                disableSubmitButton();
            }
        });

        // Обработчик клика на весь элемент
        wordItem.addEventListener('click', function(e) {
            if (e.target.type !== 'checkbox') {
                const checkbox = this.querySelector('.word-checkbox');
                checkbox.checked = !checkbox.checked;
                checkbox.dispatchEvent(new Event('change'));
            }
        });

        wordsList.appendChild(wordItem);
    });

    updateSelectedCount();
    updateStats();
    updateSelectedWordsInput();
}

function selectAllWords() {
    console.log('Выбрать все слова');
    allWords.forEach(word => {
        selectedWordIds.add(word.id.toString());
    });
    renderWordsList();
    enableSubmitButton();
}

function deselectAllWords() {
    console.log('Снять все слова');
    selectedWordIds.clear();
    renderWordsList();
    disableSubmitButton();
}

function showWordsList() {
    document.getElementById('words-list').style.display = 'block';
    document.getElementById('no-words-message').style.display = 'none';
    document.getElementById('words-stats').style.display = 'block';
    document.getElementById('error-message').style.display = 'none';
}

function showNoWordsMessage() {
    document.getElementById('words-list').style.display = 'none';
    document.getElementById('no-words-message').style.display = 'block';
    document.getElementById('words-stats').style.display = 'none';
    document.getElementById('error-message').style.display = 'none';
}

function showError(message) {
    const errorElement = document.getElementById('error-message');
    errorElement.innerHTML = `<i class="bi bi-exclamation-triangle me-2"></i> ${message}`;
    errorElement.style.display = 'block';
}

function updateSelectedCount() {
    const count = selectedWordIds.size;
    document.getElementById('selected-count').textContent = `Выбрано: ${count} слов`;

    // Обновляем цвет бейджа в зависимости от количества
    const badge = document.getElementById('selected-count');
    badge.className = 'badge';

    if (count === 0) {
        badge.classList.add('bg-secondary');
    } else if (count <= 5) {
        badge.classList.add('bg-success');
    } else if (count <= 15) {
        badge.classList.add('bg-primary');
    } else if (count <= 30) {
        badge.classList.add('bg-warning');
    } else {
        badge.classList.add('bg-danger');
    }
}

function updateStats() {
    const selectedWords = allWords.filter(word => selectedWordIds.has(word.id.toString()));

    // Общее количество слов
    document.getElementById('stats-total').textContent = selectedWords.length;

    // Уникальные темы
    const topics = new Set(selectedWords.map(word => word.topic).filter(topic => topic));
    document.getElementById('stats-unique-topics').textContent = topics.size;

    // Средняя длина английских слов
    if (selectedWords.length > 0) {
        const totalLetters = selectedWords.reduce((sum, word) => sum + word.english.length, 0);
        const avgLetters = Math.round(totalLetters / selectedWords.length);
        document.getElementById('stats-letters').textContent = avgLetters;
    } else {
        document.getElementById('stats-letters').textContent = '0';
    }
}

function updateSelectedWordsInput() {
    const container = document.getElementById('selected-words-input');
    container.innerHTML = '';

    selectedWordIds.forEach(wordId => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'word_selection';
        input.value = wordId;
        container.appendChild(input);
    });

    console.log('Обновлены скрытые поля:', Array.from(selectedWordIds));
}

function enableSubmitButton() {
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = false;
    submitBtn.classList.remove('btn-secondary');
    submitBtn.classList.add('btn-primary');
}

function disableSubmitButton() {
    const submitBtn = document.getElementById('submit-btn');
    submitBtn.disabled = true;
    submitBtn.classList.remove('btn-primary');
    submitBtn.classList.add('btn-secondary');
}

function updateExerciseTypeHint(type) {
    const hintElement = document.getElementById('exercise-type-hint');

    const hints = {
        'spelling': 'Ученик будет вводить английское слово по буквам, видя русский перевод',
        'drag_and_drop': 'Ученик будет перетаскивать буквы, чтобы составить английское слово',
        'letter_soup': 'Ученик будет искать слова в буквенной сетке'
    };

    hintElement.textContent = hints[type] || '';
}
</script>

<style>
    .stats-card {
        border-left: 4px solid #0d6efd;
        padding-left: 15px;
        margin-bottom: 20px;
    }
</style>
{% endblock %}
```
---

## `exercises\templates\exercises\delete_confirm.html`

```text
{% extends 'base.html' %}
{% block title %}Удаление упражнения{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">Удаление упражнения</h4>
                </div>
                <div class="card-body">
                    <p>Вы уверены, что хотите удалить это упражнение?</p>
                    
                    <div class="alert alert-info">
                        <h5>Информация об упражнении:</h5>
                        <ul>
                            <li><strong>Тип:</strong> {{ exercise.get_exercise_type_display }}</li>
                            <li><strong>Ученик:</strong> {{ exercise.student.get_full_name|default:exercise.student.username }}</li>
                            <li><strong>Создано:</strong> {{ exercise.created_at|date:"d.m.Y" }}</li>
                            {% if exercise.due_date %}
                                <li><strong>Срок:</strong> {{ exercise.due_date|date:"d.m.Y H:i" }}</li>
                            {% endif %}
                        </ul>
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-danger btn-lg">
                                <i class="bi bi-trash me-2"></i>Удалить упражнение
                            </button>
                            <a href="{% url 'exercises:teacher_exercises_for_student' exercise.student.id %}" 
                               class="btn btn-secondary btn-lg">
                                <i class="bi bi-arrow-left me-2"></i>Отмена
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
---

## `exercises\templates\exercises\detail.html`

```text
{% extends 'base.html' %}
{% block title %}{{ exercise.get_exercise_type_display }}{% endblock %}
{% block extra_style %}
    <style>
        .bg-not_started {
            background-color: #6c757d;
        }

        .bg-in_progress {
            background-color: #ffc107;
            color: #000;
        }

        .bg-completed {
            background-color: #198754;
        }

        .bg-graded {
            background-color: #0d6efd;
        }
    </style>
{% endblock %}
{% block content %}
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="card shadow">
                    <div class="card-header {% if exercise.is_overdue %}bg-danger text-white{% else %}bg-primary text-white{% endif %}">
                        <div class="d-flex justify-content-between align-items-center">
                            <h4 class="mb-0">{{ exercise.get_exercise_type_display }}</h4>
                            <div>
                                {% if is_teacher %}
                                    <span class="badge bg-light text-dark">Учитель</span>
                                {% else %}
                                    <span class="badge bg-success">Ученик</span>
                                {% endif %}
                            </div>
                        </div>
                    </div>

                    <div class="card-body">
                        <!-- Основная информация -->
                        <div class="row mb-4">
                            <div class="col-md-6">
                                <h5>Информация о задании</h5>
                                <table class="table table-sm">
                                    <tr>
                                        <th width="40%">Ученик:</th>
                                        <td>{{ exercise.student.get_full_name|default:exercise.student.username }}</td>
                                    </tr>
                                    <tr>
                                        <th>Учитель:</th>
                                        <td>{{ exercise.teacher.get_full_name|default:exercise.teacher.username }}</td>
                                    </tr>
                                    <tr>
                                        <th>Тип задания:</th>
                                        <td>{{ exercise.get_assignment_type_display }}</td>
                                    </tr>
                                    <tr>
                                        <th>Вид упражнения:</th>
                                        <td>{{ exercise.get_exercise_type_display }}</td>
                                    </tr>
                                    <tr>
                                        <th>Статус:</th>
                                        <td>
                                        <span class="badge bg-{{ exercise.status }}">
                                            {{ exercise.get_status_display }}
                                        </span>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            <div class="col-md-6">
                                <h5>Подробности</h5>
                                <table class="table table-sm">
                                    <tr>
                                        <th width="40%">Попытки:</th>
                                        <td>{{ exercise.attempts }}</td>
                                    </tr>
                                    <tr>
                                        <th>Срок:</th>
                                        <td>
                                            {% if exercise.due_date %}
                                                {{ exercise.due_date|date:"d.m.Y H:i" }}
                                                {% if exercise.is_overdue %}
                                                    <span class="badge bg-danger ms-2">Просрочено</span>
                                                {% endif %}
                                            {% else %}
                                                <span class="text-muted">Нет срока</span>
                                            {% endif %}
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </div>

                        <!-- Описание -->
                        {% if exercise.description %}
                            <div class="mb-4">
                                <h5>Описание задания</h5>
                                <div class="card bg-light">
                                    <div class="card-body">
                                        {{ exercise.description|linebreaks }}
                                    </div>
                                </div>
                            </div>
                        {% endif %}

                        <!-- Данные упражнения -->
                        <div class="mb-4">
                            <h5>Данные упражнения</h5>
                            <div class="card">
                                <div class="card-header bg-light">
                                    <small>JSON структура упражнения (только для просмотра)</small>
                                </div>
                                <div class="card-body">
                                    <pre class="bg-dark text-light p-3 rounded"
                                         style="max-height: 300px; overflow: auto;"><code>{{ exercise.exercise_data|pprint }}</code></pre>
                                </div>
                            </div>
                        </div>

                        <!-- Комментарий учителя -->
                        {% if exercise.teacher_comment %}
                            <div class="mb-4">
                                <h5>Комментарий учителя</h5>
                                <div class="card border-info">
                                    <div class="card-body">
                                        {{ exercise.teacher_comment|linebreaks }}
                                    </div>
                                </div>
                            </div>
                        {% endif %}

                        <!-- Действия -->
                        <div class="mt-4">
                            {% if is_student %}
                                {% if exercise.status == 'not_started' or exercise.status == 'in_progress' %}
                                    <a href="{% url 'exercises:do_exercise' exercise.id %}"
                                       class="btn btn-primary btn-lg">
                                        {% if exercise.status == 'not_started' %}
                                            <i class="bi bi-play-circle me-2"></i>Начать выполнение
                                        {% else %}
                                            <i class="bi bi-arrow-repeat me-2"></i>Продолжить выполнение
                                        {% endif %}
                                    </a>
                                {% else %}
                                    <button class="btn btn-secondary btn-lg" disabled>
                                        {% if exercise.status == 'completed' %}
                                            <i class="bi bi-check-circle me-2"></i>Задание выполнено
                                        {% elif exercise.status == 'graded' %}
                                            <i class="bi bi-star me-2"></i>Задание проверено
                                        {% else %}
                                            <i class="bi bi-x-circle me-2"></i>Задание недоступно
                                        {% endif %}
                                    </button>
                                {% endif %}
                            {% endif %}

                            {% if is_teacher %}
                                <div class="btn-group">
                                    <form method="post"
                                          action="{% url 'exercises:delete_exercise' exercise.id %}"
                                          onsubmit="return confirm('Вы уверены, что хотите удалить это упражнение?')">
                                        {% csrf_token %}
                                        <button type="submit" class="btn btn-danger">
                                            <i class="bi bi-trash me-2"></i>Удалить
                                        </button>
                                    </form>
                                    <a href="{% url 'exercises:teacher_exercises_for_student' exercise.student.id %}"
                                       class="btn btn-secondary">
                                        <i class="bi bi-arrow-left me-2"></i>К списку
                                    </a>
                                </div>
                            {% else %}
                                <a href="{% url 'exercises:my_exercises' %}" class="btn btn-secondary">
                                    <i class="bi bi-arrow-left me-2"></i>К моим упражнениям
                                </a>
                            {% endif %}
                        </div>
                    </div>

                    <div class="card-footer text-muted">
                        <small>
                            Создано: {{ exercise.created_at|date:"d.m.Y H:i" }} |
                            Обновлено: {{ exercise.updated_at|date:"d.m.Y H:i" }}
                            {% if exercise.completed_at %}
                                | Завершено: {{ exercise.completed_at|date:"d.m.Y H:i" }}
                            {% endif %}
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>


{% endblock %}
```
---

## `exercises\templates\exercises\drag_and_drop.html`

```text
{% extends 'base.html' %}
{% block title %}Перетаскивание букв (Drag and Drop){% endblock %}

{% block extra_style %}
<style>
    /* Контейнеры для букв */
    .drop-zone {
        width: 70px;
        height: 80px;
        border: 3px dashed #dee2e6;
        border-radius: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin: 0 10px;
        font-size: 28px;
        font-weight: bold;
        background-color: #f8f9fa;
        transition: all 0.3s;
        user-select: none;
        position: relative;
    }

    .drop-zone.active {
        border-color: #0d6efd;
        background-color: rgba(13, 110, 253, 0.1);
    }

    .drop-zone.filled {
        border-style: solid;
        border-color: #6c757d;
        background-color: white;
    }

    .drop-zone.correct {
        border-color: #198754;
        background-color: rgba(25, 135, 84, 0.1);
    }

    .drop-zone.incorrect {
        border-color: #dc3545;
        background-color: rgba(220, 53, 69, 0.1);
    }

    /* Пул букв */
    .letter-pool {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin: 30px 0;
        padding: 25px;
        background-color: #f8f9fa;
        border-radius: 15px;
        min-height: 100px;
    }

    .draggable-letter {
        width: 70px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        background-color: #0d6efd;
        color: white;
        border-radius: 10px;
        cursor: grab;
        user-select: none;
        transition: all 0.2s;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .draggable-letter:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
        background-color: #0b5ed7;
    }

    .draggable-letter:active {
        cursor: grabbing;
        transform: translateY(0);
    }

    .draggable-letter.used {
        opacity: 0.4;
        cursor: not-allowed;
        background-color: #6c757d;
        box-shadow: none;
    }

    .draggable-letter.used:hover {
        transform: none;
        box-shadow: none;
    }

    /* Буква внутри drop-зоны */
    .letter-in-zone {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        font-weight: bold;
        border-radius: 8px;
    }

    /* Контейнер слова */
    .word-container {
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 30px;
    }

    .russian-word {
        font-size: 2.5rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 40px;
        color: #2c3e50;
        text-align: center;
    }

    .drop-zones-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 15px;
        margin: 30px 0;
        padding: 20px;
    }

    .progress-container {
        position: sticky;
        top: 0;
        background: white;
        z-index: 100;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }

    /* Подсказки */
    .hint {
        font-size: 0.9rem;
        color: #6c757d;
        text-align: center;
        margin-top: 10px;
    }

    /* Анимации */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }

    .shake {
        animation: shake 0.3s ease-in-out;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    .pulse {
        animation: pulse 0.5s ease-in-out;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <!-- Прогресс и управление -->
    <div class="progress-container mb-4">
        <div class="d-flex justify-content-between align-items-center">
            <h4 class="mb-0">Перетаскивание букв (Drag and Drop)</h4>
            <div>
                <span id="current-word" class="badge bg-primary fs-6">1</span> из
                <span id="total-words" class="badge bg-secondary fs-6">{{ words|length }}</span>
            </div>
        </div>
        <div class="progress mt-2" style="height: 8px;">
            <div id="exercise-progress" class="progress-bar" style="width: 0%"></div>
        </div>
    </div>

    <!-- Контейнер для упражнения -->
    <div class="card shadow">
        <div class="card-body">
            <div id="word-container" class="word-container">
                <!-- Русское слово -->
                <div id="current-russian" class="russian-word mb-4"></div>

                <!-- Окошки для букв -->
                <div class="hint">Перетащите буквы в окошки ниже, чтобы составить английское слово</div>
                <div id="drop-zones" class="drop-zones-container mb-4"></div>

                <!-- Пул букв -->
                <div class="hint">Используйте эти буквы:</div>
                <div id="letter-pool" class="letter-pool mb-4"></div>

                <!-- Результат -->
                <div id="result-message" class="alert d-none mb-4"></div>

                <!-- Кнопки управления -->
                <div class="mt-4">
                    <button id="check-btn" class="btn btn-primary btn-lg me-3">
                        <i class="bi bi-check-circle me-2"></i>Проверить
                    </button>
                    <button id="reset-btn" class="btn btn-outline-secondary btn-lg me-3">
                        <i class="bi bi-arrow-clockwise me-2"></i>Сбросить
                    </button>
                    <button id="next-btn" class="btn btn-success btn-lg d-none">
                        <i class="bi bi-arrow-right me-2"></i>Следующее слово
                    </button>
                    <button id="finish-btn" class="btn btn-success btn-lg d-none">
                        <i class="bi bi-check-circle-fill me-2"></i>Завершить упражнение
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Скрытые данные -->
<input type="hidden" id="exercise-id" value="{{ exercise.id }}">
<input type="hidden" id="current-index" value="0">

<script>
let words = {{ words|safe }};
let currentIndex = 0;
let totalWords = words.length;
let draggedLetter = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (words.length === 0) {
        showNoWordsMessage();
        return;
    }

    initDragAndDrop();
    loadWord(0);
    updateProgress();
    updateWordCounter();
});

function showNoWordsMessage() {
    const container = document.getElementById('word-container');
    container.innerHTML = `
        <div class="text-center py-5">
            <i class="bi bi-exclamation-triangle display-1 text-warning mb-3"></i>
            <h3>Нет слов для упражнения</h3>
            <p class="text-muted">В этом упражнении нет слов для выполнения.</p>
            <a href="{% url 'exercises:my_exercises' %}" class="btn btn-primary mt-3">
                Вернуться к списку упражнений
            </a>
        </div>
    `;
}

function initDragAndDrop() {
    // Обработчики для перетаскивания букв
    document.addEventListener('dragstart', function(e) {
        if (e.target.classList.contains('draggable-letter') && !e.target.classList.contains('used')) {
            draggedLetter = e.target;
            e.dataTransfer.setData('text/plain', e.target.id);
            e.dataTransfer.effectAllowed = 'move';
            e.target.style.opacity = '0.5';
        }
    });

    document.addEventListener('dragend', function(e) {
        if (e.target.classList.contains('draggable-letter')) {
            e.target.style.opacity = '1';
            draggedLetter = null;
        }
    });

    // Обработчики для drop-зон
    const dropZonesContainer = document.getElementById('drop-zones');

    dropZonesContainer.addEventListener('dragover', function(e) {
        e.preventDefault();
        if (e.target.classList.contains('drop-zone')) {
            e.target.classList.add('active');
            e.dataTransfer.dropEffect = 'move';
        }
    });

    dropZonesContainer.addEventListener('dragleave', function(e) {
        if (e.target.classList.contains('drop-zone')) {
            e.target.classList.remove('active');
        }
    });

    dropZonesContainer.addEventListener('drop', function(e) {
        e.preventDefault();
        e.target.classList.remove('active');

        if (e.target.classList.contains('drop-zone') && draggedLetter) {
            const dropZone = e.target;
            const letterId = e.dataTransfer.getData('text/plain');
            const letterElement = document.getElementById(letterId);

            if (letterElement && !letterElement.classList.contains('used')) {
                // Если в этой зоне уже есть буква, возвращаем её в пул
                const existingLetter = dropZone.querySelector('.draggable-letter');
                if (existingLetter) {
                    returnLetterToPool(existingLetter);
                }

                // Помещаем новую букву в зону
                placeLetterInZone(letterElement, dropZone);

                // Визуальная обратная связь
                dropZone.classList.add('pulse');
                setTimeout(() => {
                    dropZone.classList.remove('pulse');
                }, 500);

                // Проверяем, все ли зоны заполнены
                checkAllZonesFilled();
            }
        }
    });
}

function loadWord(index) {
    if (index >= words.length) {
        finishExercise();
        return;
    }

    const word = words[index];
    document.getElementById('current-russian').textContent = word.russian.toUpperCase();

    // Очищаем контейнеры
    document.getElementById('drop-zones').innerHTML = '';
    document.getElementById('letter-pool').innerHTML = '';

    // Создаем окошки для букв
    const englishWord = word.english.toUpperCase();
    const dropZonesContainer = document.getElementById('drop-zones');

    for (let i = 0; i < englishWord.length; i++) {
        const dropZone = document.createElement('div');
        dropZone.className = 'drop-zone';
        dropZone.dataset.index = i;
        dropZone.dataset.expected = englishWord[i];
        dropZone.dataset.position = i;
        dropZone.setAttribute('draggable', 'false');
        dropZonesContainer.appendChild(dropZone);

        // Добавляем обработчик двойного клика для удаления буквы
        dropZone.addEventListener('dblclick', function() {
            const letter = this.querySelector('.draggable-letter');
            if (letter) {
                returnLetterToPool(letter);
                checkAllZonesFilled();
            }
        });
    }

    // Создаем перемешанные буквы (включая дополнительные случайные буквы)
    const letters = englishWord.split('');

    // Добавляем несколько случайных букв для усложнения
    const randomLetters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let i = 0; i < Math.min(englishWord.length, 3); i++) {
        const randomLetter = randomLetters[Math.floor(Math.random() * randomLetters.length)];
        letters.push(randomLetter);
    }

    // Перемешиваем буквы
    shuffleArray(letters);

    // Создаем буквы в пуле
    const letterPool = document.getElementById('letter-pool');
    letters.forEach((letter, i) => {
        const letterElement = document.createElement('div');
        letterElement.id = `letter-${index}-${i}`;
        letterElement.className = 'draggable-letter';
        letterElement.draggable = true;
        letterElement.textContent = letter;
        letterElement.dataset.letter = letter;
        letterPool.appendChild(letterElement);
    });

    // Обновляем кнопки
    document.getElementById('check-btn').classList.remove('d-none');
    document.getElementById('reset-btn').classList.remove('d-none');
    document.getElementById('next-btn').classList.add('d-none');
    document.getElementById('finish-btn').classList.add('d-none');
    document.getElementById('result-message').classList.add('d-none');
}

function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

function placeLetterInZone(letterElement, dropZone) {
    // Клонируем букву для помещения в зону
    const clonedLetter = letterElement.cloneNode(true);
    clonedLetter.id = `${letterElement.id}-in-zone`;
    clonedLetter.classList.add('used');
    clonedLetter.classList.remove('draggable-letter');
    clonedLetter.classList.add('letter-in-zone');
    clonedLetter.style.backgroundColor = '#0d6efd';
    clonedLetter.style.opacity = '1';
    clonedLetter.draggable = false;

    // Добавляем обработчик двойного клика для возврата в пул
    clonedLetter.addEventListener('dblclick', function() {
        returnLetterToPool(letterElement);
        dropZone.classList.remove('filled');
        dropZone.innerHTML = '';
        checkAllZonesFilled();
    });

    // Помечаем оригинальную букву как использованную
    letterElement.classList.add('used');
    letterElement.style.opacity = '0.4';
    letterElement.style.cursor = 'not-allowed';

    // Добавляем клонированную букву в drop-зону
    dropZone.innerHTML = '';
    dropZone.appendChild(clonedLetter);
    dropZone.classList.add('filled');
}

function returnLetterToPool(letterElement) {
    const originalLetter = document.getElementById(letterElement.id.replace('-in-zone', ''));
    if (originalLetter) {
        originalLetter.classList.remove('used');
        originalLetter.style.opacity = '1';
        originalLetter.style.cursor = 'grab';
    }
}

function checkAllZonesFilled() {
    const dropZones = document.querySelectorAll('.drop-zone');
    const allFilled = Array.from(dropZones).every(zone => zone.classList.contains('filled'));

    if (allFilled) {
        document.getElementById('check-btn').classList.remove('btn-primary');
        document.getElementById('check-btn').classList.add('btn-success');
    } else {
        document.getElementById('check-btn').classList.remove('btn-success');
        document.getElementById('check-btn').classList.add('btn-primary');
    }
}

function checkWord() {
    const dropZones = document.querySelectorAll('.drop-zone');
    let allCorrect = true;

    // Проверяем каждую зону
    dropZones.forEach(zone => {
        const letterElement = zone.querySelector('.letter-in-zone');
        const userLetter = letterElement ? letterElement.textContent : '';
        const expectedLetter = zone.dataset.expected;

        if (userLetter === expectedLetter) {
            zone.classList.remove('incorrect', 'shake');
            zone.classList.add('correct');
            if (letterElement) {
                letterElement.style.backgroundColor = '#198754';
            }
        } else {
            zone.classList.remove('correct');
            zone.classList.add('incorrect', 'shake');
            if (letterElement) {
                letterElement.style.backgroundColor = '#dc3545';
            }
            allCorrect = false;
        }
    });

    // Убираем анимацию тряски через время
    setTimeout(() => {
        document.querySelectorAll('.shake').forEach(el => el.classList.remove('shake'));
    }, 300);

    // Показываем результат
    const resultMessage = document.getElementById('result-message');
    if (allCorrect) {
        resultMessage.className = 'alert alert-success';
        resultMessage.innerHTML = `
            <i class="bi bi-check-circle-fill me-2"></i>
            <strong>Отлично!</strong> Слово "${words[currentIndex].english.toUpperCase()}" собрано правильно!
        `;

        // Показываем кнопку для следующего слова
        document.getElementById('check-btn').classList.add('d-none');
        document.getElementById('reset-btn').classList.add('d-none');
        document.getElementById('next-btn').classList.remove('d-none');

        // Обновляем статистику на сервере
        updateExerciseProgress(true);
    } else {
        resultMessage.className = 'alert alert-danger';
        resultMessage.innerHTML = `
            <i class="bi bi-x-circle-fill me-2"></i>
            <strong>Попробуйте еще раз!</strong> Слово собрано неправильно.
        `;

        // Обновляем статистику на сервере
        updateExerciseProgress(false);
    }

    resultMessage.classList.remove('d-none');
}

function resetWord() {
    // Возвращаем все буквы в пул
    const dropZones = document.querySelectorAll('.drop-zone');
    const letterPool = document.getElementById('letter-pool');

    dropZones.forEach(zone => {
        const letterElement = zone.querySelector('.letter-in-zone');
        if (letterElement) {
            // Находим оригинальную букву в пуле
            const originalId = letterElement.id.replace('-in-zone', '');
            const originalLetter = document.getElementById(originalId);
            if (originalLetter) {
                originalLetter.classList.remove('used');
                originalLetter.style.opacity = '1';
                originalLetter.style.cursor = 'grab';
            }
        }
        zone.classList.remove('filled', 'correct', 'incorrect', 'active');
        zone.innerHTML = '';
    });
    
    // Перемешиваем буквы в пуле
    const letters = Array.from(letterPool.querySelectorAll('.draggable-letter'));
    letterPool.innerHTML = '';
    shuffleArray(letters);
    letters.forEach(letter => letterPool.appendChild(letter));
    
    // Сбрасываем кнопки
    document.getElementById('check-btn').classList.remove('btn-success');
    document.getElementById('check-btn').classList.add('btn-primary');
    document.getElementById('result-message').classList.add('d-none');
}

function nextWord() {
    currentIndex++;
    loadWord(currentIndex);
    updateProgress();
    updateWordCounter();
}

function finishExercise() {
    const container = document.getElementById('word-container');
    container.innerHTML = `
        <div class="text-center py-5">
            <i class="bi bi-check-circle-fill display-1 text-success mb-3"></i>
            <h3>Упражнение завершено!</h3>
            <p class="text-muted">Вы успешно выполнили все задания.</p>
            
            <div class="row mt-4">
                <div class="col-md-6 offset-md-3">
                    <div class="card bg-light">
                        <div class="card-body">
                            <h5>Статистика</h5>
                            <p>Выполнено слов: <strong>${totalWords}</strong></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <a href="{% url 'exercises:my_exercises' %}" class="btn btn-primary me-2">
                    <i class="bi bi-list me-2"></i>К списку упражнений
                </a>
                <a href="{% url 'dashboard:student' %}" class="btn btn-outline-primary">
                    <i class="bi bi-house me-2"></i>В кабинет
                </a>
            </div>
        </div>
    `;
    
    // Отправляем запрос на завершение упражнения
    completeExercise();
}

function updateExerciseProgress(isCorrect) {
    const exerciseId = document.getElementById('exercise-id').value;
    // AJAX запрос для обновления прогресса на сервере
    // ...
}

function completeExercise() {
    const exerciseId = document.getElementById('exercise-id').value;
    
    fetch(`/exercises/complete/${exerciseId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: 'completed' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Упражнение завершено на сервере');
        }
    })
    .catch(error => {
        console.error('Ошибка при завершении упражнения:', error);
    });
}

function updateProgress() {
    if (totalWords === 0) return;
    const progress = ((currentIndex) / totalWords) * 100;
    document.getElementById('exercise-progress').style.width = progress + '%';
}

function updateWordCounter() {
    document.getElementById('current-word').textContent = currentIndex + 1;
    document.getElementById('total-words').textContent = totalWords;
}

// Обработчики кнопок
document.getElementById('check-btn').addEventListener('click', checkWord);
document.getElementById('reset-btn').addEventListener('click', resetWord);
document.getElementById('next-btn').addEventListener('click', nextWord);

// Глобальный обработчик Enter
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        // Если кнопка проверки видна, проверяем слово
        if (!document.getElementById('check-btn').classList.contains('d-none')) {
            checkWord();
        }
        // Если видна кнопка следующего слова, переходим к следующему
        else if (!document.getElementById('next-btn').classList.contains('d-none')) {
            nextWord();
        }
    }
});
</script>
{% endblock %}
```
---

## `exercises\templates\exercises\letter_soup.html`

```text
{% extends 'base.html' %}
{% block title %}Буквенный суп (Letter Soup){% endblock %}

{% block extra_style %}
<style>
    /* Стили для сетки букв */
    .letter-grid {
        display: inline-grid;
        grid-template-columns: repeat({{ grid_size }}, 35px);
        grid-gap: 2px;
        margin: 20px 0;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border: 2px solid #dee2e6;
    }
    
    .letter-cell {
        width: 35px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: bold;
        background-color: white;
        border: 1px solid #dee2e6;
        border-radius: 4px;
        text-transform: uppercase;
        transition: all 0.2s;
        user-select: none;
    }
    
    .letter-cell:hover {
        background-color: #f1f3f4;
        transform: scale(1.05);
    }
    
    .letter-cell.found {
        background-color: #d1e7dd;
        border-color: #198754;
        color: #0f5132;
    }
    
    /* Стили для списка слов */
    .word-list-item {
        padding: 8px 12px;
        margin: 5px;
        border-radius: 6px;
        background-color: white;
        border: 1px solid #dee2e6;
        transition: all 0.3s;
    }
    
    .word-list-item.found {
        background-color: #d1e7dd;
        border-color: #198754;
        text-decoration: line-through;
        color: #0f5132;
    }
    
    /* Счетчик */
    .counter-badge {
        font-size: 1.2rem;
        padding: 8px 16px;
    }
    
    /* Анимации */
    @keyframes foundAnimation {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .found-animation {
        animation: foundAnimation 0.5s ease;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <!-- Заголовок и счетчик -->
    <div class="row mb-4">
        <div class="col">
            <h4 class="mb-0">Буквенный суп (Letter Soup)</h4>
            <p class="text-muted mb-0">{{ exercise.description|default:"Найдите английские слова в сетке" }}</p>
        </div>
        <div class="col-auto">
            <div class="counter-badge bg-primary text-white rounded-pill">
                Найдено: <span id="found-count">0</span> из <span id="total-count">{{ english_words|length }}</span>
            </div>
        </div>
    </div>

    <!-- Прогресс -->
    <div class="row mb-4">
        <div class="col">
            <div class="progress" style="height: 10px;">
                <div id="progress-bar" class="progress-bar" style="width: 0%"></div>
            </div>
        </div>
    </div>

    <!-- Основное содержимое -->
    <div class="row">
        <!-- Левая колонка: сетка букв -->
        <div class="col-lg-8">
            <div class="card shadow">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Сетка букв</h5>
                </div>
                <div class="card-body">
                    <div class="text-center">
                        <div class="letter-grid" id="letter-grid">
                            {% for row in grid %}
                                {% for cell in row %}
                                    <div class="letter-cell" 
                                         data-row="{{ forloop.parentloop.counter0 }}" 
                                         data-col="{{ forloop.counter0 }}">
                                        {{ cell }}
                                    </div>
                                {% endfor %}
                            {% endfor %}
                        </div>
                    </div>
                    
                    <div class="mt-3 text-center">
                        <small class="text-muted">
                            <i class="bi bi-info-circle"></i> 
                            Слова могут располагаться по горизонтали (→) или вертикали (↓)
                        </small>
                    </div>
                </div>
            </div>
        </div>

        <!-- Правая колонка: список слов и ввод -->
        <div class="col-lg-4">
            <!-- Список слов для поиска -->
            <div class="card shadow mb-4">
                <div class="card-header bg-success text-white">
                    <h5 class="mb-0">Слова для поиска</h5>
                </div>
                <div class="card-body">
                    <div class="row g-2" id="word-list">
                        {% for pair in pairs %}
                            <div class="col-md-6">
                                <div class="word-list-item" 
                                     id="word-{{ pair.english|lower }}" 
                                     data-english="{{ pair.english|lower }}">
                                    <div class="fw-bold">{{ pair.russian }}</div>
                                    <div class="text-primary small">{{ pair.english|upper }}</div>
                                </div>
                            </div>
                        {% endfor %}
                    </div>
                </div>
            </div>

            <!-- Ввод слова -->
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Ввод найденного слова</h5>
                </div>
                <div class="card-body">
                    <div class="mb-3">
                        <label class="form-label">Введите английское слово:</label>
                        <input type="text" 
                               class="form-control form-control-lg text-uppercase" 
                               id="word-input"
                               placeholder="DOG"
                               autocomplete="off"
                               autofocus>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button class="btn btn-primary btn-lg" id="check-word-btn">
                            <i class="bi bi-check-circle me-2"></i>Проверить
                        </button>
                        <button class="btn btn-outline-secondary" id="hint-btn">
                            <i class="bi bi-lightbulb me-2"></i>Подсказка
                        </button>
                    </div>
                    
                    <!-- Сообщения -->
                    <div id="message-container" class="mt-3"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Скрытые данные -->
<input type="hidden" id="exercise-id" value="{{ exercise.id }}">
<input type="hidden" id="grid-size" value="{{ grid_size }}">

<script>
// Глобальные переменные
let englishWords = {{ english_words|safe }};
let foundWords = new Set();
let totalWords = englishWords.length;
let gridData = {{ grid|safe }};
let placedWords = {{ placed_words|safe }};
let gridSize = {{ grid_size }};

// DOM элементы
const wordInput = document.getElementById('word-input');
const checkBtn = document.getElementById('check-word-btn');
const hintBtn = document.getElementById('hint-btn');
const foundCountEl = document.getElementById('found-count');
const totalCountEl = document.getElementById('total-count');
const progressBar = document.getElementById('progress-bar');

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Letter Soup загружен');
    console.log('Слова для поиска:', englishWords);
    console.log('Размещенные слова:', placedWords);
    
    updateCounter();
    updateProgress();
    
    // Обработчики событий
    checkBtn.addEventListener('click', checkWord);
    hintBtn.addEventListener('click', showHint);
    
    wordInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            checkWord();
        }
    });
    
    // Автоматический фокус на поле ввода
    setTimeout(() => {
        wordInput.focus();
    }, 100);
    
    // Очистка сообщений при вводе
    wordInput.addEventListener('input', function() {
        clearMessages();
    });
});

function checkWord() {
    const word = wordInput.value.trim().toLowerCase();
    
    if (!word) {
        showMessage('Введите слово', 'warning');
        return;
    }
    
    if (word.length < 2) {
        showMessage('Слово должно содержать минимум 2 буквы', 'warning');
        return;
    }
    
    // Проверяем, есть ли такое слово в списке
    if (englishWords.includes(word)) {
        // Проверяем, не было ли слово уже найдено
        if (foundWords.has(word)) {
            showMessage(`Слово "${word.toUpperCase()}" уже было найдено`, 'warning');
            wordInput.value = '';
            wordInput.focus();
            return;
        }
        
        // Проверяем, есть ли слово в сетке
        if (isWordInGrid(word)) {
            // Добавляем слово в найденные
            foundWords.add(word);
            
            // Обновляем интерфейс
            markWordAsFound(word);
            updateCounter();
            updateProgress();
            
            // Показываем успешное сообщение
            showMessage(`Отлично! Слово "${word.toUpperCase()}" найдено!`, 'success');
            
            // Подсвечиваем ячейки в сетке
            highlightWordInGrid(word);
            
            // Проверяем, все ли слова найдены
            if (foundWords.size === totalWords) {
                finishExercise();
            }
        } else {
            showMessage(`Слово "${word.toUpperCase()}" есть в списке, но не найдено в сетке. Попробуйте другое слово.`, 'danger');
        }
    } else {
        showMessage(`Слово "${word.toUpperCase()}" не найдено в списке слов`, 'danger');
    }
    
    // Очищаем поле ввода
    wordInput.value = '';
    wordInput.focus();
}

function isWordInGrid(word) {
    const wordUpper = word.toUpperCase();
    
    // Проверяем по размещенным словам
    for (const placedWord of placedWords) {
        if (placedWord.word === wordUpper) {
            return true;
        }
    }
    
    // Также проверяем вручную (на случай ошибок в алгоритме размещения)
    return checkWordInGridManually(wordUpper);
}

function checkWordInGridManually(word) {
    // Проверяем горизонтально
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col <= gridSize - word.length; col++) {
            let found = true;
            for (let i = 0; i < word.length; i++) {
                if (gridData[row][col + i] !== word[i]) {
                    found = false;
                    break;
                }
            }
            if (found) return true;
        }
    }
    
    // Проверяем вертикально
    for (let row = 0; row <= gridSize - word.length; row++) {
        for (let col = 0; col < gridSize; col++) {
            let found = true;
            for (let i = 0; i < word.length; i++) {
                if (gridData[row + i][col] !== word[i]) {
                    found = false;
                    break;
                }
            }
            if (found) return true;
        }
    }
    
    return false;
}

function highlightWordInGrid(word) {
    const wordUpper = word.toUpperCase();
    
    // Ищем слово в размещенных словах
    for (const placedWord of placedWords) {
        if (placedWord.word === wordUpper) {
            const { row, col, direction, length } = placedWord;
            
            // Подсвечиваем ячейки
            for (let i = 0; i < length; i++) {
                let cellRow = row;
                let cellCol = col;
                
                if (direction === 'horizontal') {
                    cellCol = col + i;
                } else { // vertical
                    cellRow = row + i;
                }
                
                const cell = document.querySelector(`.letter-cell[data-row="${cellRow}"][data-col="${cellCol}"]`);
                if (cell) {
                    cell.classList.add('found', 'found-animation');
                    setTimeout(() => {
                        cell.classList.remove('found-animation');
                    }, 500);
                }
            }
            return;
        }
    }
}

function markWordAsFound(word) {
    const wordElement = document.getElementById(`word-${word}`);
    if (wordElement) {
        wordElement.classList.add('found');
    }
}

function showHint() {
    // Находим первое не найденное слово
    const remainingWords = englishWords.filter(word => !foundWords.has(word));
    
    if (remainingWords.length === 0) {
        showMessage('Все слова уже найдены!', 'info');
        return;
    }
    
    const randomWord = remainingWords[Math.floor(Math.random() * remainingWords.length)];
    const wordElement = document.getElementById(`word-${randomWord}`);
    
    if (wordElement) {
        // Мигаем элементом слова
        wordElement.classList.add('found-animation');
        setTimeout(() => {
            wordElement.classList.remove('found-animation');
        }, 1000);
        
        showMessage(`Подсказка: слово "${randomWord.toUpperCase()}" еще не найдено`, 'info');
    }
}

function updateCounter() {
    foundCountEl.textContent = foundWords.size;
    totalCountEl.textContent = totalWords;
}

function updateProgress() {
    const progress = (foundWords.size / totalWords) * 100;
    progressBar.style.width = `${progress}%`;
}

function showMessage(text, type) {
    clearMessages();
    
    const messageContainer = document.getElementById('message-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${text}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    messageContainer.appendChild(alert);
    
    // Автоматически скрываем через 3 секунды
    setTimeout(() => {
        if (alert.parentNode) {
            alert.classList.remove('show');
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 150);
        }
    }, 3000);
}

function clearMessages() {
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';
}

function finishExercise() {
    showMessage('Поздравляем! Вы нашли все слова! Упражнение завершено.', 'success');
    
    // Отключаем элементы управления
    wordInput.disabled = true;
    checkBtn.disabled = true;
    hintBtn.disabled = true;
    
    // Отправляем запрос на завершение упражнения
    const exerciseId = document.getElementById('exercise-id').value;
    
    fetch(`/exercises/complete/${exerciseId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: 'completed' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Упражнение завершено на сервере');
        }
    })
    .catch(error => {
        console.error('Ошибка при завершении упражнения:', error);
    });
}
</script>
{% endblock %}
```
---

## `exercises\templates\exercises\list.html`

```text
{% extends 'base.html' %}
{% block title %}Упражнения - Учитель{% endblock %}
{% block extra_style %}
	<style>
    .bg-not_started { background-color: #6c757d; }
    .bg-in_progress { background-color: #ffc107; }
    .bg-completed { background-color: #198754; }
    .bg-graded { background-color: #0d6efd; }
</style>
{% endblock %}
{% block content %}
<div class="container-fluid">
    <div class="row mb-4">
        <div class="col">
            <h1 class="h2 mb-1">
                <i class="bi bi-journal-text text-primary me-2"></i>
                Управление упражнениями
            </h1>
            <p class="text-muted">Созданные вами упражнения для учеников</p>
        </div>
        <div class="col-auto">
            <a href="{% url 'exercises:create_exercise' %}" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i>Создать упражнение
            </a>
        </div>
    </div>
    
    {% if student %}
        <nav aria-label="breadcrumb" class="mb-4">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="{% url 'exercises:teacher_exercises' %}">Все упражнения</a>
                </li>
                <li class="breadcrumb-item active">
                    Ученик: {{ student.get_full_name|default:student.username }}
                </li>
            </ol>
        </nav>
    {% endif %}
    
    {% if students_with_exercises %}
        <!-- Общий список по ученикам -->
        <div class="row">
            {% for item in students_with_exercises %}
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        <div class="card-header bg-light">
                            <h5 class="mb-0">{{ item.student.get_full_name|default:item.student.username }}</h5>
                        </div>
                        <div class="card-body">
                            <div class="mb-3">
                                <div class="row text-center">
                                    <div class="col-4">
                                        <div class="h3 mb-0">{{ item.count }}</div>
                                        <small class="text-muted">Всего</small>
                                    </div>
                                    <div class="col-4">
                                        <div class="h3 mb-0 text-success">{{ item.completed }}</div>
                                        <small class="text-muted">Выполнено</small>
                                    </div>
                                    <div class="col-4">
                                        <div class="h3 mb-0 text-primary">{{ item.graded }}</div>
                                        <small class="text-muted">Проверено</small>
                                    </div>
                                </div>
                            </div>
                            
                            {% if item.exercises %}
                                <div class="list-group list-group-flush">
                                    {% for exercise in item.exercises|slice:":3" %}
                                        <a href="{% url 'exercises:exercise_detail' exercise.id %}" 
                                           class="list-group-item list-group-item-action">
                                            <div class="d-flex justify-content-between">
                                                <span>{{ exercise.get_exercise_type_display }}</span>
                                                <span class="badge bg-{{ exercise.status }}">
                                                    {{ exercise.get_status_display }}
                                                </span>
                                            </div>
                                        </a>
                                    {% endfor %}
                                </div>
                            {% else %}
                                <p class="text-muted text-center py-3">Нет упражнений</p>
                            {% endif %}
                        </div>
                        <div class="card-footer bg-transparent">
                            <a href="{% url 'exercises:teacher_exercises_for_student' item.student.id %}"
                               class="btn btn-sm btn-outline-primary w-100">
                                Показать все
                            </a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <!-- Список упражнений для конкретного ученика -->
        <div class="card shadow">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                    Упражнения для
                    {% if student %}
                        {{ student.get_full_name|default:student.username }}
                    {% else %}
                        всех учеников
                    {% endif %}
                </h5>
                <span class="badge bg-primary">{{ exercises.count }}</span>
            </div>

            <div class="card-body">
                {% if exercises %}
                    <div class="table-responsive">
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    {% if show_student_column %}
                                        <th>Ученик</th>
                                    {% endif %}
                                    <th>Вид упражнения</th>
                                    <th>Тип задания</th>
                                    <th>Статус</th>
                                    <th>Попытки</th>
                                    <th>Срок</th>
                                    <th>Действия</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for exercise in exercises %}
                                    <tr>
                                        {% if show_student_column %}
                                            <td>
                                                <a href="{% url 'vocabulary:teacher_panel' exercise.student.id %}">
                                                    {{ exercise.student.get_full_name|default:exercise.student.username }}
                                                </a>
                                            </td>
                                        {% endif %}
                                        <td>
                                            <a href="{% url 'exercises:exercise_detail' exercise.id %}">
                                                {{ exercise.get_exercise_type_display }}
                                            </a>
                                        </td>
                                        <td>
                                            <span class="badge bg-info">
                                                {{ exercise.get_assignment_type_display }}
                                            </span>
                                        </td>
                                        <td>
                                            <span class="badge bg-{{ exercise.status }}"
                                                  id="status-{{ exercise.id }}">
                                                {{ exercise.get_status_display }}
                                            </span>
                                        </td>
                                        <td>
                                            {{ exercise.attempts }}
                                        </td>
                                        <td>
                                            {% if exercise.due_date %}
                                                {% if exercise.is_overdue %}
                                                    <span class="text-danger">
                                                        {{ exercise.due_date|date:"d.m.Y H:i" }}
                                                    </span>
                                                {% else %}
                                                    {{ exercise.due_date|date:"d.m.Y H:i" }}
                                                {% endif %}
                                            {% else %}
                                                <span class="text-muted">Нет срока</span>
                                            {% endif %}
                                        </td>
                                        <td>
                                            <div class="btn-group btn-group-sm">
                                                <a href="{% url 'exercises:exercise_detail' exercise.id %}"
                                                   class="btn btn-outline-primary" title="Просмотр">
                                                    <i class="bi bi-eye"></i>
                                                </a>
                                                <form method="post"
                                                      action="{% url 'exercises:delete_exercise' exercise.id %}"
                                                      class="d-inline"
                                                      onsubmit="return confirm('Вы уверены, что хотите удалить это упражнение?')">
                                                    {% csrf_token %}
                                                    <button type="submit"
                                                            class="btn btn-outline-danger"
                                                            title="Удалить">
                                                        <i class="bi bi-trash"></i>
                                                    </button>
                                                </form>
                                            </div>
                                        </td>
                                    </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <div class="text-center py-5">
                        <i class="bi bi-journal-x display-1 text-muted mb-3"></i>
                        <h4>Нет упражнений</h4>
                        <p class="text-muted">
                            {% if student %}
                                У этого ученика ещё нет упражнений
                            {% else %}
                                Вы ещё не создали ни одного упражнения
                            {% endif %}
                        </p>
                        <a href="{% url 'exercises:create_exercise' %}" class="btn btn-primary">
                            <i class="bi bi-plus-circle me-2"></i>Создать первое упражнение
                        </a>
                    </div>
                {% endif %}
            </div>
        </div>
    {% endif %}
</div>



<script>
// Функция для обновления статуса
function updateStatus(exerciseId, newStatus) {
    fetch(`/exercises/update_status/${exerciseId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `status=${newStatus}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const badge = document.getElementById(`status-${exerciseId}`);
            badge.textContent = data.new_status;
            badge.className = `badge bg-${newStatus}`;
        }
    });
}
</script>
{% endblock %}
```
---

## `exercises\templates\exercises\my.html`

```text
{% extends 'base.html' %}
{% block title %}Мои упражнения{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row mb-4">
        <div class="col">
            <h1 class="h2 mb-1">
                <i class="bi bi-journal-check text-primary me-2"></i>
                Мои упражнения
            </h1>
            <p class="text-muted">Задания от учителя</p>
        </div>
    </div>
    
    <!-- Статистика -->
    <div class="row mb-4">
        <div class="col-md-3 mb-3">
            <div class="card bg-primary text-white">
                <div class="card-body text-center">
                    <div class="h1 mb-0">{{ exercises.count }}</div>
                    <p class="mb-0">Всего заданий</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-success text-white">
                <div class="card-body text-center">
                    <div class="h1 mb-0">{{ exercises|length|default:0 }}</div>
                    <p class="mb-0">Доступно сейчас</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-warning text-white">
                <div class="card-body text-center">
                    <div class="h1 mb-0">{{ exercises.count }}</div>
                    <p class="mb-0">В процессе</p>
                </div>
            </div>
        </div>
        <div class="col-md-3 mb-3">
            <div class="card bg-info text-white">
                <div class="card-body text-center">
                    <div class="h1 mb-0">{{ exercises.count }}</div>
                    <p class="mb-0">Выполнено</p>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Список упражнений -->
    <div class="card shadow">
        <div class="card-header">
            <h5 class="mb-0">Список упражнений</h5>
        </div>
        
        <div class="card-body">
            {% if exercises %}
                <div class="row g-3">
                    {% for exercise in exercises %}
                        <div class="col-md-6 col-lg-4">
                            <div class="card h-100 {% if exercise.is_overdue %}border-danger{% endif %}">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between align-items-start mb-2">
                                        <div>
                                            <h5 class="card-title">{{ exercise.get_exercise_type_display }}</h5>
                                            <p class="card-text text-muted small">
                                                {{ exercise.description|truncatechars:100 }}
                                            </p>
                                        </div>
                                        <span class="badge bg-{{ exercise.status }}">
                                            {{ exercise.get_status_display }}
                                        </span>
                                    </div>
                                    
                                    <div class="mb-3">
                                        <span class="badge bg-info me-1">
                                            {{ exercise.get_exercise_type_display }}
                                        </span>
                                        <span class="badge bg-secondary me-1">
                                            {{ exercise.get_assignment_type_display }}
                                        </span>
                                        {% if exercise.is_overdue %}
                                            <span class="badge bg-danger">Просрочено</span>
                                        {% endif %}
                                    </div>
                                    
                                    <div class="mb-3">
                                        <small class="text-muted d-block">
                                            <i class="bi bi-person me-1"></i>
                                            Учитель: {{ exercise.teacher.get_full_name|default:exercise.teacher.username }}
                                        </small>
                                        <small class="text-muted d-block">
                                            <i class="bi bi-calendar me-1"></i>
                                            Создано: {{ exercise.created_at|date:"d.m.Y" }}
                                        </small>
                                        {% if exercise.due_date %}
                                            <small class="{% if exercise.is_overdue %}text-danger{% else %}text-muted{% endif %} d-block">
                                                <i class="bi bi-clock me-1"></i>
                                                Срок: {{ exercise.due_date|date:"d.m.Y H:i" }}
                                            </small>
                                        {% endif %}
                                    </div>
                                    
                                    <div class="d-flex justify-content-between align-items-center">
                                        <div>
                                            <small class="text-muted">
                                                Попытки: {{ exercise.attempts }}/{{ exercise.max_attempts }}
                                            </small>
                                        </div>
                                        <div>
                                            {% if exercise.can_attempt %}
                                                <a href="{% url 'exercises:do_exercise' exercise.id %}"
                                                   class="btn btn-sm btn-primary">
                                                    {% if exercise.status == 'not_started' %}
                                                        Начать
                                                    {% else %}
                                                        Продолжить
                                                    {% endif %}
                                                </a>
                                            {% else %}
                                                <button class="btn btn-sm btn-secondary" disabled>
                                                    Недоступно
                                                </button>
                                            {% endif %}
                                            <a href="{% url 'exercises:exercise_detail' exercise.id %}" 
                                               class="btn btn-sm btn-outline-primary ms-1">
                                                Подробнее
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="bi bi-journal-x display-1 text-muted mb-3"></i>
                    <h4>Нет заданий</h4>
                    <p class="text-muted">Ваш учитель ещё не создал для вас упражнений</p>
                </div>
            {% endif %}
        </div>
    </div>
</div>

<style>
    .bg-not_started { background-color: #6c757d; }
    .bg-in_progress { background-color: #ffc107; color: #000; }
    .bg-completed { background-color: #198754; }
    .bg-graded { background-color: #0d6efd; }
</style>
{% endblock %}
```
---

## `exercises\templates\exercises\progress.html`

```text
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>$Title$</title>
</head>
<body>
$END$
</body>
</html>
```
---

## `exercises\templates\exercises\spelling.html`

```text
{% extends 'base.html' %}
{% block title %}Правописание (Spelling){% endblock %}

{% block extra_style %}
<style>
    .letter-input {
        width: 45px;
        height: 50px;
        font-size: 24px;
        text-align: center;
        text-transform: uppercase;
        margin: 0 5px;
        border: 2px solid #dee2e6;
        border-radius: 5px;
        transition: all 0.2s;
    }
    
    .letter-input:focus {
        border-color: #0d6efd;
        box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
        outline: none;
    }
    
    .letter-input.correct {
        border-color: #198754;
        background-color: rgba(25, 135, 84, 0.1);
    }
    
    .letter-input.incorrect {
        border-color: #dc3545;
        background-color: rgba(220, 53, 69, 0.1);
    }
    
    .word-container {
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 30px;
    }
    
    .russian-word {
        font-size: 2.5rem;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 30px;
        color: #2c3e50;
    }
    
    .progress-container {
        position: sticky;
        top: 0;
        background: white;
        z-index: 100;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <!-- Прогресс и управление -->
    <div class="progress-container mb-4">
        <div class="d-flex justify-content-between align-items-center">
            <h4 class="mb-0">Правописание (Spelling)</h4>
            <div>
                <span id="current-word" class="badge bg-primary fs-6">1</span> из 
                <span id="total-words" class="badge bg-secondary fs-6">{{ words|length }}</span>
            </div>
        </div>
        <div class="progress mt-2" style="height: 8px;">
            <div id="exercise-progress" class="progress-bar" style="width: 0%"></div>
        </div>
    </div>

    <!-- Контейнер для слов -->
    <div class="card shadow">
        <!-- Текущее слово -->
        <div class="card-body">
            <div id="word-container" class="word-container">
                <div id="current-russian" class="russian-word mb-4"></div>
                
                <div id="letters-container" class="mb-4"></div>
                
                <div id="instructions" class="text-muted mb-4 text-center">
                    Введите буквы в ячейки выше. Используйте клавиши для навигации между полями.
                </div>
                
                <div id="result-message" class="alert d-none mb-4"></div>
                
                <div class="mt-4">
                    <button id="check-btn" class="btn btn-primary btn-lg">
                        <i class="bi bi-check-circle me-2"></i>Проверить
                    </button>
                    <button id="next-btn" class="btn btn-success btn-lg d-none">
                        <i class="bi bi-arrow-right me-2"></i>Следующее слово
                    </button>
                    <button id="finish-btn" class="btn btn-success btn-lg d-none">
                        <i class="bi bi-check-circle-fill me-2"></i>Завершить упражнение
                    </button>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Скрытые данные -->
<input type="hidden" id="exercise-id" value="{{ exercise.id }}">
<input type="hidden" id="current-index" value="0">

<script>
let words = {{ words|safe }};
let currentIndex = 0;
let totalWords = words.length;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    if (words.length === 0) {
        showNoWordsMessage();
        return;
    }
    
    loadWord(0);
    updateProgress();
    updateWordCounter();
});

function showNoWordsMessage() {
    const container = document.getElementById('word-container');
    container.innerHTML = `
        <div class="text-center py-5">
            <i class="bi bi-exclamation-triangle display-1 text-warning mb-3"></i>
            <h3>Нет слов для упражнения</h3>
            <p class="text-muted">В этом упражнении нет слов для выполнения.</p>
            <a href="{% url 'exercises:my_exercises' %}" class="btn btn-primary mt-3">
                Вернуться к списку упражнений
            </a>
        </div>
    `;
}

function loadWord(index) {
    if (index >= words.length) {
        finishExercise();
        return;
    }
    
    const word = words[index];
    document.getElementById('current-russian').textContent = word.russian.toUpperCase();
    
    // Очищаем контейнер для букв
    const lettersContainer = document.getElementById('letters-container');
    lettersContainer.innerHTML = '';
    
    // Создаем инпуты для каждой буквы
    for (let i = 0; i < word.english.length; i++) {
        const input = document.createElement('input');
        input.type = 'text';
        input.maxLength = 1;
        input.className = 'letter-input';
        input.dataset.index = i;
        input.dataset.expected = word.english[i].toUpperCase();
        
        // Обработчик ввода
        input.addEventListener('input', function(e) {
            const value = e.target.value.toUpperCase();
            e.target.value = value;
            
            // Автопереход к следующему полю
            if (value && this.nextElementSibling && this.nextElementSibling.classList.contains('letter-input')) {
                this.nextElementSibling.focus();
            }
            
            // Если все поля заполнены, фокус на кнопку проверки
            const allFilled = Array.from(document.querySelectorAll('.letter-input'))
                .every(input => input.value.trim() !== '');
            if (allFilled) {
                document.getElementById('check-btn').focus();
            }
            
            // Очищаем стили ошибок при новом вводе
            input.classList.remove('incorrect', 'correct');
        });
        
        // Обработчик клавиш
        input.addEventListener('keydown', function(e) {
            switch(e.key) {
                case 'Enter':
                    e.preventDefault();
                    checkWord();
                    break;
                    
                case 'Backspace':
                    if (!this.value && this.previousElementSibling) {
                        e.preventDefault();
                        this.previousElementSibling.focus();
                    }
                    break;
                    
                case 'ArrowLeft':
                    if (this.previousElementSibling) {
                        e.preventDefault();
                        this.previousElementSibling.focus();
                    }
                    break;
                    
                case 'ArrowRight':
                    if (this.nextElementSibling) {
                        e.preventDefault();
                        this.nextElementSibling.focus();
                    }
                    break;
            }
        });
        
        lettersContainer.appendChild(input);
    }
    
    // Фокус на первое поле
    setTimeout(() => {
        const firstInput = lettersContainer.querySelector('.letter-input');
        if (firstInput) firstInput.focus();
    }, 100);
    
    // Обновляем кнопки
    document.getElementById('check-btn').classList.remove('d-none');
    document.getElementById('next-btn').classList.add('d-none');
    document.getElementById('finish-btn').classList.add('d-none');
    document.getElementById('result-message').classList.add('d-none');
}

function checkWord() {
    const inputs = document.querySelectorAll('.letter-input');
    const expectedLetters = Array.from(inputs).map(input => input.dataset.expected);
    let allCorrect = true;
    
    // Проверяем каждую букву
    inputs.forEach((input, index) => {
        const userLetter = input.value.toUpperCase();
        const expectedLetter = expectedLetters[index];
        
        if (userLetter === expectedLetter) {
            input.classList.remove('incorrect');
            input.classList.add('correct');
        } else {
            input.classList.remove('correct');
            input.classList.add('incorrect');
            allCorrect = false;
        }
    });
    
    // Показываем результат
    const resultMessage = document.getElementById('result-message');
    if (allCorrect) {
        resultMessage.className = 'alert alert-success';
        resultMessage.innerHTML = `
            <i class="bi bi-check-circle-fill me-2"></i>
            <strong>Отлично!</strong> Слово "${words[currentIndex].english.toUpperCase()}" написано правильно!
        `;
        
        // Показываем кнопку для следующего слова
        document.getElementById('check-btn').classList.add('d-none');
        document.getElementById('next-btn').classList.remove('d-none');
        
        // Обновляем статистику на сервере
        updateExerciseProgress(true);
    } else {
        resultMessage.className = 'alert alert-danger';
        resultMessage.innerHTML = `
            <i class="bi bi-x-circle-fill me-2"></i>
            <strong>Попробуйте еще раз!</strong> Некоторые буквы неверны.
        `;
        
        // Фокус на первое неправильное поле
        const firstIncorrect = document.querySelector('.letter-input.incorrect');
        if (firstIncorrect) {
            firstIncorrect.focus();
        }
        
        // Обновляем статистику на сервере
        updateExerciseProgress(false);
    }
    
    resultMessage.classList.remove('d-none');
}

function nextWord() {
    currentIndex++;
    loadWord(currentIndex);
    updateProgress();
    updateWordCounter();
}

function finishExercise() {
    const container = document.getElementById('word-container');
    container.innerHTML = `
        <div class="text-center py-5">
            <i class="bi bi-check-circle-fill display-1 text-success mb-3"></i>
            <h3>Упражнение завершено!</h3>
            <p class="text-muted">Вы успешно выполнили все задания.</p>
            
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="card bg-light">
                        <div class="card-body">
                            <h5>Статистика</h5>
                            <p>Выполнено слов: <strong>${totalWords}</strong></p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-4">
                <a href="{% url 'exercises:my_exercises' %}" class="btn btn-primary me-2">
                    <i class="bi bi-list me-2"></i>К списку упражнений
                </a>
                <a href="{% url 'dashboard:student' %}" class="btn btn-outline-primary">
                    <i class="bi bi-house me-2"></i>В кабинет
                </a>
            </div>
        </div>
    `;
    
    // Отправляем запрос на завершение упражнения
    completeExercise();
}

function updateExerciseProgress(isCorrect) {
    const exerciseId = document.getElementById('exercise-id').value;
    
    // Здесь можно добавить AJAX запрос для обновления прогресса на сервере
    // fetch(`/exercises/update_word_progress/${exerciseId}/`, {
    //     method: 'POST',
    //     headers: {
    //         'X-CSRFToken': '{{ csrf_token }}',
    //         'Content-Type': 'application/json',
    //     },
    //     body: JSON.stringify({
    //         word_index: currentIndex,
    //         is_correct: isCorrect
    //     })
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Прогресс обновлен:', data);
    // });
}

function completeExercise() {
    const exerciseId = document.getElementById('exercise-id').value;
    
    fetch(`/exercises/complete/${exerciseId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: 'completed' })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Упражнение завершено на сервере');
        }
    })
    .catch(error => {
        console.error('Ошибка при завершении упражнения:', error);
    });
}

function updateProgress() {
    if (totalWords === 0) return;
    const progress = ((currentIndex) / totalWords) * 100;
    document.getElementById('exercise-progress').style.width = progress + '%';
}

function updateWordCounter() {
    document.getElementById('current-word').textContent = currentIndex + 1;
    document.getElementById('total-words').textContent = totalWords;
}

// Обработчики кнопок
document.getElementById('check-btn').addEventListener('click', checkWord);
document.getElementById('next-btn').addEventListener('click', nextWord);

// Добавляем глобальный обработчик Enter для всей страницы
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && e.target.type !== 'text') {
        e.preventDefault();
        // Если кнопка проверки видна, проверяем слово
        if (!document.getElementById('check-btn').classList.contains('d-none')) {
            checkWord();
        }
        // Если видна кнопка следующего слова, переходим к следующему
        else if (!document.getElementById('next-btn').classList.contains('d-none')) {
            nextWord();
        }
        // Если видна кнопка завершения, завершаем упражнение
        else if (!document.getElementById('finish-btn').classList.contains('d-none')) {
            finishExercise();
        }
    }
});
</script>
{% endblock %}
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
        body {
            background: #f8f9fa;
        }

        .navbar-brand {
            font-weight: 800;
        }
    </style>
    {% block extra_style %}

    {% endblock %}
</head>
<body>
<!-- templates/base.html - обновим navbar -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container">
        <a class="navbar-brand fw-bold" href="{% url 'users:home' %}">
            <i class="bi bi-translate me-2"></i>English Easy
        </a>

        <div class="navbar-nav ms-auto align-items-center">
            {% if user.is_authenticated %}
                <span class="text-white me-3">
                    <i class="bi bi-person-circle me-1"></i>
                    {{ user.username }}
                    {% if user.is_teacher %}
                        <span class="badge bg-light text-dark ms-2">Учитель</span>
                    {% else %}
                        <span class="badge bg-success text-white ms-2">Ученик</span>
                    {% endif %}
                </span>

                <form method="post" action="{% url 'users:logout' %}" class="d-inline">
                    {% csrf_token %}
                    <button type="submit" class="btn btn-outline-light btn-sm">
                        <i class="bi bi-box-arrow-right me-1"></i>Выйти
                    </button>
                </form>
            {% else %}
                <!-- Ссылка на вход уже не нужна, так как на главной -->
                <a href="{% url 'users:home' %}#login" class="btn btn-outline-light btn-sm">
                    <i class="bi bi-box-arrow-in-right me-1"></i>Вход
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
# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User


class SimpleRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Упрощенные подсказки
        self.fields['username'].help_text = 'Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = 'Минимум 8 символов'
        self.fields['password2'].help_text = 'Повторите пароль для подтверждения'

        # Убираем сложные валидаторы паролей для упрощения
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = ''

    def clean_username(self):
        username = self.cleaned_data['username'].lower()

        # Проверяем уникальность
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
# users/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.simple_register, name='register'),  # простая регистрация
]
```
---

## `users\views.py`

```text
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SimpleRegisterForm


def home(request):
    """Главная страница с формами входа и регистрации"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    # Если есть данные POST для входа
    if request.method == 'POST' and 'login-username' in request.POST:
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Неверный логин или пароль')

    # Если есть данные POST для регистрации
    elif request.method == 'POST' and 'register-username' in request.POST:
        # Создаем копию POST данных с правильными именами полей
        post_data = request.POST.copy()
        post_data['username'] = post_data.get('register-username')
        post_data['password1'] = post_data.get('register-password1')
        post_data['password2'] = post_data.get('register-password2')

        form = SimpleRegisterForm(post_data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
            return redirect('dashboard:home')
        else:
            # Сохраняем ошибки формы для отображения
            context = {'register_form': form}
    else:
        context = {}

    return render(request, 'users/home.html', context)


def simple_register(request):
    """Простая регистрация (альтернативный вариант)"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
            return redirect('dashboard:home')
    else:
        form = SimpleRegisterForm()

    return render(request, 'users/register.html', {'form': form})

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
<!-- users/templates/users/home.html -->
{% extends 'base.html' %}
{% block title %}English Easy — Изучение английских слов{% endblock %}
{% block extra_style %}
    <style>
        .nav-tabs .nav-link {
            color: #6c757d;
            font-weight: 500;
            border: none;
            padding: 12px 0;
        }

        .nav-tabs .nav-link.active {
            color: #0d6efd;
            background: none;
            border-bottom: 3px solid #0d6efd;
        }

        .nav-tabs {
            border-bottom: 1px solid #dee2e6;
        }

        .card {
            border-radius: 15px;
        }

        .form-control-lg {
            padding: 12px 16px;
            border-radius: 8px;
        }

        .btn-lg {
            padding: 12px 24px;
            border-radius: 8px;
        }
    </style>
{% endblock %}
{% block content %}
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6">
                <!-- Приветствие -->
                <div class="text-center mb-5">
                    <h1 class="display-4 fw-bold text-primary mb-3">
                        <i class="bi bi-translate"></i> English Easy
                    </h1>
                    <p class="lead text-muted">
                        Простая платформа для изучения английских слов
                    </p>
                </div>

                <!-- Основной блок с формами -->
                <div class="card shadow-lg border-0">
                    <div class="card-body p-5">
                        <!-- Вкладки: Вход / Регистрация -->
                        <ul class="nav nav-tabs nav-fill mb-4" id="authTabs" role="tablist">
                            <li class="nav-item" role="presentation">
                                <button class="nav-link active" id="login-tab" data-bs-toggle="tab"
                                        data-bs-target="#login" type="button" role="tab" aria-controls="login"
                                        aria-selected="true">
                                    <i class="bi bi-box-arrow-in-right me-2"></i>Вход
                                </button>
                            </li>
                            <li class="nav-item" role="presentation">
                                <button class="nav-link" id="register-tab" data-bs-toggle="tab"
                                        data-bs-target="#register" type="button" role="tab"
                                        aria-controls="register" aria-selected="false">
                                    <i class="bi bi-person-plus me-2"></i>Регистрация
                                </button>
                            </li>
                        </ul>

                        <!-- Содержимое вкладок -->
                        <div class="tab-content" id="authTabsContent">
                            <!-- Вкладка входа -->
                            <div class="tab-pane fade show active" id="login" role="tabpanel"
                                 aria-labelledby="login-tab">
                                <form method="post" id="loginForm">
                                    {% csrf_token %}
                                    <input type="hidden" name="form_type" value="login">

                                    <div class="mb-3">
                                        <label for="login-username" class="form-label">Логин</label>
                                        <input type="text" class="form-control form-control-lg"
                                               id="login-username" name="login-username"
                                               placeholder="Введите ваш логин" required autofocus>
                                    </div>

                                    <div class="mb-4">
                                        <label for="login-password" class="form-label">Пароль</label>
                                        <input type="password" class="form-control form-control-lg"
                                               id="login-password" name="login-password"
                                               placeholder="Введите пароль" required>
                                        <div class="form-text text-end">
                                            <a href="#" class="text-decoration-none">Забыли пароль?</a>
                                        </div>
                                    </div>

                                    <div class="d-grid">
                                        <button type="submit" class="btn btn-primary btn-lg">
                                            <i class="bi bi-box-arrow-in-right me-2"></i>Войти в систему
                                        </button>
                                    </div>
                                </form>
                            </div>

                            <!-- Вкладка регистрации -->
                            <div class="tab-pane fade" id="register" role="tabpanel" aria-labelledby="register-tab">
                                <form method="post" id="registerForm">
                                    {% csrf_token %}
                                    <input type="hidden" name="form_type" value="register">

                                    <div class="mb-3">
                                        <label for="register-username" class="form-label">Логин</label>
                                        <input type="text"
                                               class="form-control form-control-lg {% if register_form.errors.username %}is-invalid{% endif %}"
                                               id="register-username" name="register-username"
                                               placeholder="Придумайте логин" required>
                                        {% if register_form.errors.username %}
                                            <div class="invalid-feedback">
                                                {{ register_form.errors.username.0 }}
                                            </div>
                                        {% endif %}
                                        <div class="form-text">
                                            Только буквы, цифры и символы @/./+/-
                                        </div>
                                    </div>

                                    <div class="mb-3">
                                        <label for="register-password1" class="form-label">Пароль</label>
                                        <input type="password"
                                               class="form-control form-control-lg {% if register_form.errors.password2 %}is-invalid{% endif %}"
                                               id="register-password1" name="register-password1"
                                               placeholder="Придумайте пароль" required>
                                        <div class="form-text">
                                            Минимум 8 символов
                                        </div>
                                    </div>

                                    <div class="mb-4">
                                        <label for="register-password2" class="form-label">Повторите пароль</label>
                                        <input type="password"
                                               class="form-control form-control-lg {% if register_form.errors.password2 %}is-invalid{% endif %}"
                                               id="register-password2" name="register-password2"
                                               placeholder="Повторите пароль" required>
                                        {% if register_form.errors.password2 %}
                                            <div class="invalid-feedback">
                                                {{ register_form.errors.password2.0 }}
                                            </div>
                                        {% endif %}
                                    </div>

                                    <div class="form-check mb-4">
                                        <input class="form-check-input" type="checkbox" id="agree-terms" required>
                                        <label class="form-check-label" for="agree-terms">
                                            Я согласен с <a href="#" class="text-decoration-none">правилами
                                            использования</a>
                                        </label>
                                    </div>

                                    <div class="d-grid">
                                        <button type="submit" class="btn btn-success btn-lg">
                                            <i class="bi bi-person-plus me-2"></i>Создать аккаунт
                                        </button>
                                    </div>
                                </form>
                            </div>
                        </div>

                        <!-- Информация о ролях -->
                        <div class="mt-4 pt-4 border-top">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <div class="d-flex align-items-center">
                                        <div class="bg-primary bg-opacity-10 p-3 rounded-circle me-3">
                                            <i class="bi bi-person-fill text-primary fs-4"></i>
                                        </div>
                                        <div>
                                            <h6 class="mb-1">Ученик</h6>
                                            <small class="text-muted">Изучайте слова и выполняйте задания</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <div class="d-flex align-items-center">
                                        <div class="bg-success bg-opacity-10 p-3 rounded-circle me-3">
                                            <i class="bi bi-person-badge-fill text-success fs-4"></i>
                                        </div>
                                        <div>
                                            <h6 class="mb-1">Учитель</h6>
                                            <small class="text-muted">Назначайте слова и задания ученикам</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="alert alert-info mt-3">
                                <small>
                                    <i class="bi bi-info-circle me-1"></i>
                                    Все новые пользователи регистрируются как ученики.
                                    Роль учителя можно получить через администратора.
                                </small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- JavaScript для управления формами -->
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            // Переключение вкладок с сохранением в localStorage
            const authTabs = document.getElementById('authTabs');
            const storedTab = localStorage.getItem('activeAuthTab');

            if (storedTab) {
                const tab = new bootstrap.Tab(document.querySelector(storedTab));
                tab.show();
            }

            authTabs.addEventListener('shown.bs.tab', function (event) {
                localStorage.setItem('activeAuthTab', event.target.getAttribute('data-bs-target'));
            });

            // Очистка ошибок при переключении вкладок
            document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
                tab.addEventListener('click', function () {
                    document.querySelectorAll('.is-invalid').forEach(el => {
                        el.classList.remove('is-invalid');
                    });
                    document.querySelectorAll('.invalid-feedback').forEach(el => {
                        el.style.display = 'none';
                    });
                });
            });

            // Автофокус на активной форме
            const activeTab = document.querySelector('#authTabs .nav-link.active');
            if (activeTab && activeTab.id === 'login-tab') {
                document.getElementById('login-username').focus();
            } else if (activeTab && activeTab.id === 'register-tab') {
                document.getElementById('register-username').focus();
            }
        });
    </script>


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
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('learning', 'Изучается'),
        ('review', 'Повторение'),
        ('completed', 'Изучено'),
    )

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
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='new')

    class Meta:
        unique_together = ('student', 'word')
        ordering = ['-assigned_at']
        verbose_name = "Назначенное слово"
        verbose_name_plural = "Назначенные слова"

    def __str__(self):
        return f"{self.student} ← {self.word}"


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
from . import views_api

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
    # Для студентов
    path('student/words/', views.student_words_list, name='student_words'),
    path('update_word_status/', views.update_word_status, name='update_word_status'),
    path('api/student/<int:student_id>/words/', views_api.get_student_words, name='get_student_words'),
    path('api/all_words/', views_api.get_all_words, name='get_all_words'),
]

```
---

## `vocabulary\views.py`

```text
import json
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

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


# vocabulary/views.py
@login_required
def student_words_list(request):
    """Полный список слов студента с фильтрацией"""
    if not request.user.is_student():
        return redirect('dashboard:home')

    words = StudentWord.objects.filter(student=request.user)

    # Фильтрация по статусу
    status = request.GET.get('status')
    if status and status != 'all':
        words = words.filter(status=status)

    # Сортировка
    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'alphabet':
        words = words.order_by('word__russian')
    elif sort_by == 'topic':
        words = words.order_by('word__topic__name')
    else:
        words = words.order_by('-assigned_at')

    return render(request, 'vocabulary/student_words.html', {'words': words})


@login_required
@require_POST
def update_word_status(request):
    """Обновление статуса слова (AJAX)"""
    if not request.user.is_student():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    try:
        data = json.loads(request.body)
        word_id = data.get('word_id')
        status = data.get('status')

        if not word_id or not status:
            return JsonResponse({'success': False, 'error': 'Не указан ID слова или статус'})

        student_word = StudentWord.objects.get(id=word_id, student=request.user)
        student_word.status = status

        if status == 'completed':
            student_word.review_count = 5  # Помечаем как полностью изученное
            student_word.next_review = None
        elif status == 'new':
            student_word.review_count = 0
            student_word.next_review = timezone.now() + timedelta(days=1)

        student_word.save()

        return JsonResponse({
            'success': True,
            'message': f'Статус слова изменен на "{student_word.get_status_display()}"'
        })
    except StudentWord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Слово не найдено'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



```
---

## `vocabulary\views_api.py`

```text
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import User
from vocabulary.models import StudentWord, Word
import json


@login_required
def get_student_words(request, student_id):
    """Получить слова ученика в формате JSON для AJAX"""
    if not request.user.is_teacher():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    try:
        student = get_object_or_404(User, id=student_id, role='student')

        # Получаем слова, назначенные ученику
        student_words = StudentWord.objects.filter(
            student=student
        ).select_related('word', 'word__topic')

        # Формируем список слов
        words_list = []
        for sw in student_words:
            words_list.append({
                'id': sw.word.id,
                'russian': sw.word.russian,
                'english': sw.word.english,
                'topic': sw.word.topic.name if sw.word.topic else '',
                'topic_color': sw.word.topic.color if sw.word.topic else '#6c757d',
                'status': sw.status,
                'assigned_at': sw.assigned_at.strftime('%d.%m.%Y') if sw.assigned_at else ''
            })

        return JsonResponse({
            'success': True,
            'words': words_list,
            'student': {
                'id': student.id,
                'name': student.get_full_name() or student.username
            },
            'count': len(words_list)
        })

    except Exception as e:
        print(f"Ошибка в get_student_words: {str(e)}")  # Для отладки
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def get_all_words(request):
    """Получить все слова для учителя"""
    if not request.user.is_teacher():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    try:
        # Получаем все слова
        words = Word.objects.all().select_related('topic')

        words_list = []
        for word in words:
            words_list.append({
                'id': word.id,
                'russian': word.russian,
                'english': word.english,
                'topic': word.topic.name if word.topic else '',
                'topic_color': word.topic.color if word.topic else '#6c757d',
                'created_at': word.created_at.strftime('%d.%m.%Y')
            })

        return JsonResponse({
            'success': True,
            'words': words_list,
            'count': len(words_list)
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```
---

## `vocabulary\__init__.py`

```text

```
---

## `vocabulary\management\commands\add_words_interactive.py`

```text
import os
import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from vocabulary.models import Topic, Word, StudentWord
from colorama import Fore, Style, init
import sys

# Инициализация colorama для цветного вывода
init(autoreset=True)


class Command(BaseCommand):
    help = 'Интерактивное добавление слов ученику из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--json-file',
            type=str,
            help='Путь к JSON файлу со словами (опционально)'
        )

    def handle(self, *args, **options):
        self.stdout.write(Fore.CYAN + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ИНТЕРАКТИВНОЕ ДОБАВЛЕНИЕ СЛОВ УЧЕНИКУ')
        self.stdout.write(Fore.CYAN + '=' * 60)

        # Шаг 1: Выбор ученика
        student = self.select_student()
        if not student:
            self.stdout.write(Fore.RED + 'Отмена операции.')
            return

        # Шаг 2: Выбор или указание JSON файла
        json_file = options.get('json_file')
        if not json_file:
            json_file = self.select_json_file()

        # Шаг 3: Загрузка слов из JSON
        words_data = self.load_words_from_json(json_file)
        if not words_data:
            return

        # Шаг 4: Подтверждение
        self.confirm_operation(student, words_data)

        # Шаг 5: Добавление слов
        added_count = self.add_words_to_student(student, words_data)

        # Шаг 6: Итог
        self.show_summary(student, added_count)

    def select_student(self):
        """Выбор ученика из списка существующих"""
        students = User.objects.filter(role='student').order_by('username')

        if not students.exists():
            self.stdout.write(Fore.YELLOW + 'Нет существующих учеников.')
            create_new = input(Fore.WHITE + 'Создать нового ученика? (y/n): ').lower()

            if create_new == 'y':
                return self.create_new_student()
            return None

        self.stdout.write(Fore.GREEN + '\nСписок существующих учеников:')
        self.stdout.write(Fore.GREEN + '-' * 40)

        for i, student in enumerate(students, 1):
            word_count = StudentWord.objects.filter(student=student).count()
            self.stdout.write(
                f"{Fore.CYAN}{i}. {Fore.WHITE}{student.username} "
                f"({student.get_full_name() or 'Без имени'}) - "
                f"{Fore.YELLOW}{word_count} слов"
            )

        self.stdout.write(Fore.GREEN + '-' * 40)
        self.stdout.write(Fore.CYAN + "0. Создать нового ученика")
        self.stdout.write(Fore.CYAN + "q. Отмена")

        while True:
            choice = input(Fore.WHITE + '\nВыберите ученика (номер): ').strip()

            if choice.lower() == 'q':
                return None
            elif choice == '0':
                return self.create_new_student()

            try:
                index = int(choice) - 1
                if 0 <= index < len(students):
                    selected_student = students[index]
                    self.stdout.write(
                        Fore.GREEN + f'Выбран ученик: {selected_student.username}'
                    )
                    return selected_student
                else:
                    self.stdout.write(Fore.RED + 'Неверный номер. Попробуйте снова.')
            except ValueError:
                self.stdout.write(Fore.RED + 'Введите число, 0, или q для отмены.')

    def create_new_student(self):
        """Создание нового ученика"""
        self.stdout.write(Fore.CYAN + '\nСоздание нового ученика:')

        while True:
            username = input(Fore.WHITE + 'Логин: ').strip()
            if not username:
                self.stdout.write(Fore.RED + 'Логин не может быть пустым.')
                continue

            if User.objects.filter(username=username).exists():
                self.stdout.write(Fore.RED + 'Пользователь с таким логином уже существует.')
                continue

            break

        first_name = input(Fore.WHITE + 'Имя (опционально): ').strip()
        last_name = input(Fore.WHITE + 'Фамилия (опционально): ').strip()
        email = input(Fore.WHITE + 'Email (опционально): ').strip()

        # Пароль по умолчанию
        password = 'password123'  # В реальном приложении попросите ввести пароль

        student = User.objects.create(
            username=username,
            first_name=first_name or '',
            last_name=last_name or '',
            email=email or f'{username}@example.com',
            role='student'
        )
        student.set_password(password)
        student.save()

        self.stdout.write(Fore.GREEN + f'Создан новый ученик: {username} (пароль: {password})')
        self.stdout.write(Fore.YELLOW + '⚠️  Не забудьте изменить пароль при первом входе!')

        return student

    def select_json_file(self):
        """Выбор JSON файла"""
        default_file = 'words.json'
        self.stdout.write(Fore.CYAN + '\nВыбор файла со словами:')

        # Проверяем существующие JSON файлы в корне проекта
        json_files = [f for f in os.listdir('.') if f.endswith('.json')]

        if json_files:
            self.stdout.write(Fore.GREEN + 'Найденные JSON файлы:')
            for i, file in enumerate(json_files, 1):
                self.stdout.write(f"{Fore.CYAN}{i}. {Fore.WHITE}{file}")

            choice = input(
                Fore.WHITE + f'\nВыберите файл (1-{len(json_files)}) или укажите свой путь: '
            ).strip()

            try:
                index = int(choice) - 1
                if 0 <= index < len(json_files):
                    return json_files[index]
            except ValueError:
                pass

            # Если ввели путь
            if choice:
                return choice

        # Если нет файлов или выбрано вручную
        while True:
            file_path = input(
                Fore.WHITE + f'Введите путь к JSON файлу [{default_file}]: '
            ).strip() or default_file

            if os.path.exists(file_path):
                return file_path

            self.stdout.write(Fore.RED + f'Файл не найден: {file_path}')
            create_sample = input(
                Fore.WHITE + 'Создать пример файла? (y/n): '
            ).lower()

            if create_sample == 'y':
                self.create_sample_json(file_path)
                return file_path

    def create_sample_json(self, file_path):
        """Создание примера JSON файла"""
        sample_data = [
            {
                "russian": "яблоко",
                "english": "apple",
                "topic": "Еда",
                "topic_color": "#FF6B6B"
            },
            {
                "russian": "собака",
                "english": "dog",
                "topic": "Животные",
                "topic_color": "#4ECDC4"
            },
            {
                "russian": "мама",
                "english": "mother",
                "topic": "Семья",
                "topic_color": "#FFD166"
            },
            {
                "russian": "красный",
                "english": "red",
                "topic": "Цвета",
                "topic_color": "#06D6A0"
            },
            {
                "russian": "счастье",
                "english": "happiness",
                "topic": "Эмоции",
                "topic_color": "#118AB2"
            }
        ]

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)

        self.stdout.write(Fore.GREEN + f'Создан пример файла: {file_path}')
        self.stdout.write(Fore.YELLOW + 'Отредактируйте его перед использованием.')

    def load_words_from_json(self, json_file):
        """Загрузка слов из JSON файла"""
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if not isinstance(data, list):
                self.stdout.write(Fore.RED + 'Ошибка: JSON должен содержать массив объектов.')
                return None

            # Валидация структуры
            validated_data = []
            for i, item in enumerate(data, 1):
                if not isinstance(item, dict):
                    self.stdout.write(Fore.RED + f'Ошибка в строке {i}: должен быть объектом')
                    continue

                # Проверяем обязательные поля
                if 'russian' not in item or 'english' not in item:
                    self.stdout.write(Fore.RED + f'Ошибка в строке {i}: отсутствуют russian или english')
                    continue

                validated_item = {
                    'russian': str(item['russian']).strip().lower(),
                    'english': str(item['english']).strip().lower(),
                    'topic': item.get('topic', 'Общее'),
                    'topic_color': item.get('topic_color', '#3B82F6'),
                    'notes': item.get('notes', '')
                }
                validated_data.append(validated_item)

            self.stdout.write(Fore.GREEN + f'Загружено {len(validated_data)} слов из {json_file}')
            return validated_data

        except json.JSONDecodeError as e:
            self.stdout.write(Fore.RED + f'Ошибка парсинга JSON: {e}')
            return None
        except FileNotFoundError:
            self.stdout.write(Fore.RED + f'Файл не найден: {json_file}')
            return None
        except Exception as e:
            self.stdout.write(Fore.RED + f'Ошибка загрузки файла: {e}')
            return None

    def confirm_operation(self, student, words_data):
        """Подтверждение операции"""
        # Группируем слова по темам
        topics_summary = {}
        for word in words_data:
            topic = word['topic']
            if topic not in topics_summary:
                topics_summary[topic] = []
            topics_summary[topic].append(f"{word['russian']} → {word['english']}")

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ПОДТВЕРЖДЕНИЕ ОПЕРАЦИИ')
        self.stdout.write(Fore.CYAN + '=' * 60)
        self.stdout.write(Fore.WHITE + f'Ученик: {student.username}')
        self.stdout.write(Fore.WHITE + f'Количество слов: {len(words_data)}')
        self.stdout.write(Fore.WHITE + f'Количество тем: {len(topics_summary)}')

        # Показываем краткую статистику по темам
        for topic, words in topics_summary.items():
            self.stdout.write(Fore.GREEN + f'\nТема "{topic}": {len(words)} слов')
            if len(words) <= 5:  # Показываем слова только если их мало
                for word in words[:5]:
                    self.stdout.write(Fore.YELLOW + f'  • {word}')
            else:
                self.stdout.write(Fore.YELLOW + f'  Первые 5 слов:')
                for word in words[:5]:
                    self.stdout.write(Fore.YELLOW + f'  • {word}')

        confirm = input(Fore.WHITE + '\nПродолжить добавление слов? (y/n): ').lower()
        if confirm != 'y':
            self.stdout.write(Fore.YELLOW + 'Операция отменена.')
            sys.exit(0)

    def add_words_to_student(self, student, words_data):
        """Добавление слов ученику"""
        # Получаем учителя для назначения
        teacher = User.objects.filter(role='teacher').first()
        if not teacher:
            # Используем текущего суперпользователя или создаем
            teacher = User.objects.filter(is_superuser=True).first()
            if not teacher:
                teacher = User.objects.create(
                    username='system_teacher',
                    role='teacher',
                    is_staff=True,
                    is_superuser=True
                )
                teacher.set_password('system123')
                teacher.save()

        added_count = 0
        duplicate_count = 0
        topic_created = set()

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ДОБАВЛЕНИЕ СЛОВ')
        self.stdout.write(Fore.CYAN + '=' * 60)

        for i, word_item in enumerate(words_data, 1):
            # Прогресс
            if i % 10 == 0 or i == len(words_data):
                self.stdout.write(Fore.WHITE + f'Обработка: {i}/{len(words_data)}...')

            # Получаем или создаем тему
            topic_name = word_item['topic']
            topic_color = word_item['topic_color']

            topic, created = Topic.objects.get_or_create(
                name=topic_name,
                defaults={'color': topic_color}
            )

            if created and topic_name not in topic_created:
                self.stdout.write(Fore.GREEN + f'Создана тема: {topic_name}')
                topic_created.add(topic_name)

            # Получаем или создаем слово
            word, word_created = Word.objects.get_or_create(
                russian=word_item['russian'],
                english=word_item['english'],
                defaults={'topic': topic}
            )

            # Если слово уже существовало, но без темы - добавляем тему
            if not word_created and not word.topic:
                word.topic = topic
                word.save()

            # Создаем связь с учеником
            student_word, assigned_created = StudentWord.objects.get_or_create(
                student=student,
                word=word,
                defaults={
                    'assigned_by': teacher,
                    'status': 'new',
                    'assigned_at': timezone.now()
                }
            )

            if assigned_created:
                added_count += 1
            else:
                duplicate_count += 1

        return added_count

    def show_summary(self, student, added_count):
        """Показать итоговую статистику"""
        # Получаем актуальную статистику
        total_words = StudentWord.objects.filter(student=student).count()

        # Группировка по темам
        from django.db.models import Count
        topic_stats = StudentWord.objects.filter(
            student=student
        ).select_related('word__topic').values(
            'word__topic__name',
            'word__topic__color'
        ).annotate(count=Count('id')).order_by('-count')

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.CYAN + 'ИТОГОВАЯ СТАТИСТИКА')
        self.stdout.write(Fore.CYAN + '=' * 60)
        self.stdout.write(Fore.GREEN + f'Ученик: {student.username}')
        self.stdout.write(Fore.GREEN + f'Добавлено новых слов: {added_count}')
        self.stdout.write(Fore.GREEN + f'Всего слов у ученика: {total_words}')

        if topic_stats:
            self.stdout.write(Fore.CYAN + '\nРаспределение по темам:')
            for stat in topic_stats:
                topic_name = stat['word__topic__name'] or 'Без темы'
                topic_color = stat['word__topic__color'] or '#6c757d'
                count = stat['count']

                # Создаем цветную полоску прогресса
                bar_length = 20
                filled = int((count / total_words) * bar_length) if total_words > 0 else 0
                bar = '█' * filled + '░' * (bar_length - filled)

                self.stdout.write(
                    f"{Fore.WHITE}{topic_name:15} {Fore.CYAN}{bar} "
                    f"{Fore.YELLOW}{count:3} слов"
                )

        self.stdout.write(Fore.CYAN + '\n' + '=' * 60)
        self.stdout.write(Fore.GREEN + 'Операция успешно завершена! ✓')
```
---

## `vocabulary\management\commands\list_students.py`

```text
from django.core.management.base import BaseCommand
from users.models import User
from vocabulary.models import StudentWord
from django.db.models import Count


class Command(BaseCommand):
    help = 'Показать список учеников со статистикой слов'

    def handle(self, *args, **kwargs):
        students = User.objects.filter(role='student').annotate(
            word_count=Count('assigned_words')
        ).order_by('-word_count')

        print("=" * 60)
        print(f"{'Ученик':20} {'Имя':20} {'Слов':5} {'Темы':10}")
        print("=" * 60)

        for student in students:
            # Получаем статистику по темам
            topic_stats = StudentWord.objects.filter(
                student=student
            ).select_related('word__topic').values(
                'word__topic__name'
            ).annotate(count=Count('id')).order_by('-count')[:3]

            topics_str = ", ".join([f"{stat['word__topic__name'] or 'Без темы'}"
                                    for stat in topic_stats[:2]])
            if topic_stats.count() > 2:
                topics_str += f" (+{topic_stats.count() - 2})"

            print(f"{student.username:20} "
                  f"{student.get_full_name()[:18]:20} "
                  f"{student.word_count:5} "
                  f"{topics_str[:30]:30}")
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

## `vocabulary\templates\vocabulary\student_words.html`

```text
<!-- vocabulary/templates/vocabulary/student_words.html -->
{% extends 'base.html' %}
{% block title %}Мои слова{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row mb-4">
        <div class="col">
            <h1 class="h2 mb-1">Мои слова</h1>
            <p class="text-muted">Все слова, назначенные вам учителем</p>
        </div>
        <div class="col-auto">
            <a href="{% url 'vocabulary:practice' %}" class="btn btn-primary">
                <i class="bi bi-play-circle me-2"></i>Начать тренировку
            </a>
        </div>
    </div>

    <!-- Фильтры и сортировка -->
    <div class="card shadow-sm mb-4">
        <div class="card-body py-3">
            <div class="row align-items-center">
                <div class="col-md-6 mb-2 mb-md-0">
                    <form method="get" class="d-flex">
                        <select name="status" class="form-select me-2" onchange="this.form.submit()">
                            <option value="all" {% if not request.GET.status or request.GET.status == 'all' %}selected{% endif %}>Все статусы</option>
                            <option value="new" {% if request.GET.status == 'new' %}selected{% endif %}>Новые</option>
                            <option value="learning" {% if request.GET.status == 'learning' %}selected{% endif %}>Изучаются</option>
                            <option value="review" {% if request.GET.status == 'review' %}selected{% endif %}>Повторение</option>
                            <option value="completed" {% if request.GET.status == 'completed' %}selected{% endif %}>Изучено</option>
                        </select>

                        <select name="sort" class="form-select" onchange="this.form.submit()">
                            <option value="date" {% if request.GET.sort == 'date' %}selected{% endif %}>По дате добавления</option>
                            <option value="alphabet" {% if request.GET.sort == 'alphabet' %}selected{% endif %}>По алфавиту</option>
                            <option value="topic" {% if request.GET.sort == 'topic' %}selected{% endif %}>По теме</option>
                        </select>
                    </form>
                </div>
                <div class="col-md-6 text-md-end">
                    <span class="text-muted">Найдено слов: {{ words.count }}</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Список слов -->
    {% if words %}
        <div class="row" id="wordsList">
            {% for student_word in words %}
                <div class="col-md-6 col-lg-4 col-xl-3 mb-4">
                    <div class="card word-card border-{% cycle 'primary' 'success' 'warning' 'info' 'danger' as cardcolor %} shadow-sm h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <div>
                                    <h5 class="card-title mb-1">{{ student_word.word.russian }}</h5>
                                    <p class="card-text text-primary fs-5">{{ student_word.word.english }}</p>
                                </div>
                                <div class="dropdown">
                                    <button class="btn btn-sm btn-outline-{{ cardcolor }}" type="button" data-bs-toggle="dropdown">
                                        <i class="bi bi-three-dots"></i>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item change-status"
                                               data-status="new"
                                               data-word-id="{{ student_word.id }}">Новое</a></li>
                                        <li><a class="dropdown-item change-status"
                                               data-status="learning"
                                               data-word-id="{{ student_word.id }}">Изучается</a></li>
                                        <li><a class="dropdown-item change-status"
                                               data-status="review"
                                               data-word-id="{{ student_word.id }}">Повторение</a></li>
                                        <li><a class="dropdown-item change-status"
                                               data-status="completed"
                                               data-word-id="{{ student_word.id }}">Изучено</a></li>
                                    </ul>
                                </div>
                            </div>

                            {% if student_word.word.topic %}
                                <span class="badge mb-3" style="background-color: {{ student_word.word.topic.color }}20; color: {{ student_word.word.topic.color }}; border: 1px solid {{ student_word.word.topic.color }}">
                                    {{ student_word.word.topic.name }}
                                </span>
                            {% endif %}

                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <small class="text-muted">
                                    <i class="bi bi-calendar me-1"></i>
                                    {{ student_word.assigned_at|date:"d.m.Y" }}
                                </small>
                                <span class="badge bg-{{ student_word.status }}">
                                    {{ student_word.get_status_display }}
                                </span>
                            </div>

                            <div class="progress" style="height: 6px;">
                                <div class="progress-bar bg-{{ cardcolor }}"
                                     style="width: {{ student_word.get_mastery_level }}%"></div>
                            </div>
                            <small class="text-muted d-block mt-1">
                                Уровень владения: {{ student_word.get_mastery_level }}%
                                ({{ student_word.correct_answers }}✓/{{ student_word.wrong_answers }}✗)
                            </small>

                            {% if student_word.next_review %}
                                <small class="text-muted d-block mt-2">
                                    <i class="bi bi-arrow-repeat me-1"></i>
                                    Повторить: {{ student_word.next_review|date:"d.m.Y" }}
                                </small>
                            {% endif %}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>

        <!-- Пагинация (если понадобится) -->
        {% if words.paginator %}
            <nav aria-label="Навигация по страницам">
                <ul class="pagination justify-content-center">
                    {% if words.has_previous %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ words.previous_page_number }}&status={{ request.GET.status }}&sort={{ request.GET.sort }}">Назад</a>
                        </li>
                    {% endif %}

                    {% for num in words.paginator.page_range %}
                        <li class="page-item {% if words.number == num %}active{% endif %}">
                            <a class="page-link" href="?page={{ num }}&status={{ request.GET.status }}&sort={{ request.GET.sort }}">{{ num }}</a>
                        </li>
                    {% endfor %}

                    {% if words.has_next %}
                        <li class="page-item">
                            <a class="page-link" href="?page={{ words.next_page_number }}&status={{ request.GET.status }}&sort={{ request.GET.sort }}">Вперед</a>
                        </li>
                    {% endif %}
                </ul>
            </nav>
        {% endif %}
    {% else %}
        <div class="text-center py-5">
            <i class="bi bi-journal-x display-1 text-muted mb-3"></i>
            <h3>Нет слов</h3>
            <p class="text-muted">
                {% if request.GET.status %}
                    Слова с выбранным статусом не найдены
                {% else %}
                    Вам ещё не назначили ни одного слова
                {% endif %}
            </p>
            <a href="{% url 'dashboard:student' %}" class="btn btn-primary">Вернуться в кабинет</a>
        </div>
    {% endif %}
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Изменение статуса слова
    document.querySelectorAll('.change-status').forEach(btn => {
        btn.addEventListener('click', function() {
            const wordId = this.getAttribute('data-word-id');
            const status = this.getAttribute('data-status');

            fetch('{% url "vocabulary:update_word_status" %}', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({word_id: wordId, status: status})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Ошибка: ' + data.error);
                }
            })
            .catch(error => {
                alert('Ошибка сети');
            });
        });
    });
});
</script>

<style>
.word-card {
    transition: transform 0.2s, box-shadow 0.2s;
    border-left: 4px solid;
}

.word-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
}

.bg-new { background-color: #6c757d; color: white; }
.bg-learning { background-color: #ffc107; color: black; }
.bg-review { background-color: #fd7e14; color: white; }
.bg-completed { background-color: #198754; color: white; }
</style>
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

                        <a href="{% url 'exercises:create_exercise_for_student' student.id %}"
                           class="btn btn-warning">
                            <i class="bi bi-journal-plus me-2"></i>
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

