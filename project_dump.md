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
    - exercises/
        - admin.py
        - forms.py
        - models.py
        - urls.py
        - views.py
        - templates/
            - exercises/
                - create.html
                - detail.html
                - list.html
                - my.html
                - progress.html
                - spelling.html
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
                - practice.html
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

    # Статистика по словам
    stats = {
        'total': assigned_words.count(),
        'new': assigned_words.filter(status='new').count(),
        'learning': assigned_words.filter(status='learning').count(),
        'review': assigned_words.filter(status='review').count(),
        'completed': assigned_words.filter(status='completed').count(),
    }

    # Слова для повторения сегодня (интервальное повторение)
    today = timezone.now()
    words_for_review = assigned_words.filter(
        next_review__lte=today,
        status__in=['new', 'learning', 'review']
    ).order_by('next_review')[:10]

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

    # Последние изученные слова
    recent_words = assigned_words.order_by('-last_reviewed')[:10] if assigned_words.filter(
        last_reviewed__isnull=False).exists() else assigned_words.order_by('-assigned_at')[:5]

    # Общая статистика за неделю
    week_ago = timezone.now() - timedelta(days=7)
    weekly_stats = {
        'words_added': assigned_words.filter(assigned_at__gte=week_ago).count(),
        'words_reviewed': assigned_words.filter(last_reviewed__gte=week_ago).count(),
        'correct_answers': sum(
            assigned_words.filter(last_reviewed__gte=week_ago).values_list('correct_answers', flat=True)),
    }

    context = {
        'stats': stats,
        'words_for_review': words_for_review,
        'assignments': assignments,
        'topics_with_progress': topics_with_progress,
        'recent_words': recent_words,
        'weekly_stats': weekly_stats,
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
            <div class="col-auto">
                <a href="{% url 'vocabulary:practice' %}" class="btn btn-primary btn-lg">
                    <i class="bi bi-play-circle me-2"></i>Начать тренировку
                </a>
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
                <!-- Карточка для повторения -->
                {% if words_for_review %}
                    <div class="card shadow-sm mb-4">
                        <div class="card-header bg-warning text-white">
                            <h5 class="mb-0">
                                <i class="bi bi-arrow-repeat me-2"></i>
                                Повторить сегодня
                            </h5>
                        </div>
                        <div class="card-body">
                            <p class="text-muted">Слова для повторения:</p>
                            <div class="list-group">
                                {% for word in words_for_review %}
                                    <div class="list-group-item border-0 py-2">
                                        <div class="d-flex justify-content-between">
                                            <div>
                                                <strong>{{ word.word.russian }}</strong> →
                                                <span class="text-primary">{{ word.word.english }}</span>
                                            </div>
                                            <span class="badge bg-{{ word.status }}">
                                    {{ word.get_status_display }}
                                </span>
                                        </div>
                                        {% if word.word.topic %}
                                            <small class="badge mt-1" style="background: {{ word.word.topic.color }}">
                                                {{ word.word.topic.name }}
                                            </small>
                                        {% endif %}
                                    </div>
                                {% endfor %}
                            </div>
                            <div class="mt-3">
                                <a href="{% url 'vocabulary:practice' %}" class="btn btn-warning w-100">
                                    Начать повторение ({{ words_for_review|length }})
                                </a>
                            </div>
                        </div>
                    </div>
                {% endif %}

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
                                        <h6 class="card-title mb-1">{{ assignment.title }}</h6>
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
                                        <a href="{% url 'exercises:exercise_detail' assignment.id %}"
                                           class="btn btn-sm btn-info mt-2">Начать задание</a>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                {% endif %}

                <!-- Еженедельная статистика -->
                <div class="card shadow-sm">
                    <div class="card-header bg-secondary text-white">
                        <h5 class="mb-0">
                            <i class="bi bi-graph-up me-2"></i>
                            За неделю
                        </h5>
                    </div>
                    <div class="card-body">
                        <div class="list-group list-group-flush">
                            <div class="list-group-item d-flex justify-content-between px-0">
                                <span>Добавлено слов</span>
                                <strong>{{ weekly_stats.words_added }}</strong>
                            </div>
                            <div class="list-group-item d-flex justify-content-between px-0">
                                <span>Повторено слов</span>
                                <strong>{{ weekly_stats.words_reviewed }}</strong>
                            </div>
                            <div class="list-group-item d-flex justify-content-between px-0">
                                <span>Правильных ответов</span>
                                <strong>{{ weekly_stats.correct_answers }}</strong>
                            </div>
                        </div>
                    </div>
                </div>
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
                                                <small class="text-muted">
                                                    {% if sw.last_reviewed %}
                                                        <i class="bi bi-arrow-repeat me-1"></i>
                                                        Повторено: {{ sw.last_reviewed|date:"d.m.Y" }}
                                                    {% else %}
                                                        <i class="bi bi-calendar me-1"></i>
                                                        Добавлено: {{ sw.assigned_at|date:"d.m.Y" }}
                                                    {% endif %}
                                                </small>
                                                <span class="badge bg-{{ sw.status }}">
                                            {{ sw.get_status_display }}
                                        </span>
                                            </div>

                                            {% if sw.review_count > 0 %}
                                                <div class="progress mt-2" style="height: 4px;">
                                                    <div class="progress-bar bg-success"
                                                         style="width: {{ sw.get_mastery_level }}%"></div>
                                                </div>
                                                <small class="text-muted d-block mt-1">
                                                    Уровень владения: {{ sw.get_mastery_level }}%
                                                </small>
                                            {% endif %}
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
    list_display = ('title', 'student', 'teacher', 'assignment_type', 'exercise_type', 'status', 'score', 'due_date')
    list_filter = ('assignment_type', 'exercise_type', 'status', 'teacher', 'student')
    search_fields = ('title', 'description', 'student__username', 'teacher__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'student', 'teacher')
        }),
        ('Типы и статус', {
            'fields': ('assignment_type', 'exercise_type', 'status')
        }),
        ('Попытки и баллы', {
            'fields': ('attempts', 'max_attempts', 'score', 'max_score')
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
import json


class ExerciseCreateForm(forms.ModelForm):
    # Кастомное поле для JSON данных
    exercise_data_raw = forms.CharField(
        label='Данные упражнения (JSON)',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'placeholder': 'Введите JSON структуру упражнения...\nПример для spelling:\n{\n  "words": ["apple", "banana", "cherry"],\n  "instructions": "Напишите слова правильно"\n}'
        }),
        required=True
    )

    class Meta:
        model = Exercise
        fields = [
            'title', 'description', 'student',
            'assignment_type', 'exercise_type',
            'max_attempts', 'due_date', 'max_score'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'exercise_type': forms.Select(attrs={'class': 'form-select'}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        if teacher:
            # Ограничиваем выбор учеников только теми, кто связан с этим учителем
            self.fields['student'].queryset = User.objects.filter(role='student')

        # Устанавливаем начальные значения
        if not self.instance.pk:
            self.initial['exercise_data_raw'] = '{\n  "words": [],\n  "instructions": ""\n}'
        else:
            self.initial['exercise_data_raw'] = json.dumps(
                self.instance.exercise_data,
                indent=2,
                ensure_ascii=False
            )

    def clean_exercise_data_raw(self):
        data = self.cleaned_data['exercise_data_raw']
        try:
            parsed_data = json.loads(data)
            return parsed_data
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'Неверный JSON формат: {e}')

    def save(self, commit=True):
        exercise = super().save(commit=False)
        exercise.exercise_data = self.cleaned_data['exercise_data_raw']

        if commit:
            exercise.save()

        return exercise
```
---

## `exercises\models.py`

```text
from django.db import models
from django.conf import settings
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

    # Основные поля
    title = models.CharField('Название задания', max_length=200)
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
    max_attempts = models.IntegerField('Максимум попыток', default=3)

    # Данные упражнения
    exercise_data = models.JSONField('Данные упражнения', default=dict)

    # Даты
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    completed_at = models.DateTimeField('Завершено', null=True, blank=True)

    # Результаты
    score = models.IntegerField('Баллы', default=0)
    max_score = models.IntegerField('Максимум баллов', default=100)
    teacher_comment = models.TextField('Комментарий учителя', blank=True)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student}"

    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False

    def can_attempt(self):
        if self.attempts >= self.max_attempts:
            return False
        if self.status in ['completed', 'graded']:
            return False
        return True

    def start_attempt(self):
        from django.utils import timezone
        self.attempts += 1
        self.status = 'in_progress'
        self.save()

    def complete_attempt(self, score):
        from django.utils import timezone
        self.score = score
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
    path('start/<int:exercise_id>/', views.start_exercise, name='start_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('update_status/<int:exercise_id>/', views.update_exercise_status, name='update_exercise_status'),
]
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
        form = ExerciseCreateForm(request.POST, teacher=request.user)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.teacher = request.user
            exercise.save()

            messages.success(request, f'Упражнение "{exercise.title}" создано!')

            # Редирект на панель учителя для этого ученика
            return redirect('vocabulary:teacher_panel', student_id=exercise.student.id)
    else:
        initial = {}
        if student:
            initial['student'] = student

        form = ExerciseCreateForm(initial=initial, teacher=request.user)

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


@login_required
def start_exercise(request, exercise_id):
    """Начать выполнение упражнения (заглушка)"""
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if not request.user == exercise.student:
        messages.error(request, 'Только ученик может выполнять это упражнение')
        return redirect('dashboard:home')

    if not exercise.can_attempt():
        messages.warning(request, 'Вы исчерпали все попытки или задание уже выполнено')
        return redirect('exercises:my_exercises')

    # Начинаем попытку
    exercise.start_attempt()

    messages.info(request, f'Вы начали выполнение упражнения "{exercise.title}"')

    # Временная заглушка - просто показываем детали
    return redirect('exercises:exercise_detail', exercise_id=exercise.id)


@login_required
def delete_exercise(request, exercise_id):
    """Удаление упражнения"""
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if not request.user == exercise.teacher:
        messages.error(request, 'Только создавший учитель может удалить упражнение')
        return redirect('dashboard:home')

    if request.method == 'POST':
        student_id = exercise.student.id
        exercise.delete()
        messages.success(request, 'Упражнение удалено')
        return redirect('exercises:teacher_exercises', student_id=student_id)

    return render(request, 'exercises/delete_confirm.html', {
        'exercise': exercise,
    })


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
                        
                        <div class="row g-3">
                            <!-- Основная информация -->
                            <div class="col-md-6">
                                <h5 class="mb-3 text-primary">Основная информация</h5>
                                
                                <div class="mb-3">
                                    <label class="form-label">Название задания *</label>
                                    {{ form.title }}
                                    {% if form.title.errors %}
                                        <div class="text-danger small">{{ form.title.errors }}</div>
                                    {% endif %}
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Описание</label>
                                    {{ form.description }}
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Ученик *</label>
                                    {{ form.student }}
                                    {% if form.student.errors %}
                                        <div class="text-danger small">{{ form.student.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <!-- Параметры задания -->
                            <div class="col-md-6">
                                <h5 class="mb-3 text-primary">Параметры задания</h5>
                                
                                <div class="row g-2">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label class="form-label">Тип задания</label>
                                            {{ form.assignment_type }}
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label class="form-label">Вид упражнения</label>
                                            {{ form.exercise_type }}
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="row g-2">
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label class="form-label">Максимум попыток</label>
                                            {{ form.max_attempts }}
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="mb-3">
                                            <label class="form-label">Максимум баллов</label>
                                            {{ form.max_score }}
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="mb-3">
                                    <label class="form-label">Срок выполнения</label>
                                    {{ form.due_date }}
                                    <div class="form-text">Оставьте пустым, если срок не ограничен</div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- JSON данные -->
                        <div class="mt-4">
                            <h5 class="mb-3 text-primary">Данные упражнения (JSON)</h5>
                            <p class="text-muted small mb-2">
                                Введите структуру упражнения в формате JSON. В зависимости от типа упражнения структура может различаться.
                            </p>
                            {{ form.exercise_data_raw }}
                            {% if form.exercise_data_raw.errors %}
                                <div class="text-danger small mt-2">{{ form.exercise_data_raw.errors }}</div>
                            {% endif %}
                            
                            <div class="mt-2">
                                <button type="button" class="btn btn-sm btn-outline-info" id="formatJson">
                                    <i class="bi bi-code-slash"></i> Форматировать JSON
                                </button>
                                <button type="button" class="btn btn-sm btn-outline-success" id="validateJson">
                                    <i class="bi bi-check-circle"></i> Проверить JSON
                                </button>
                            </div>
                            
                            <div class="alert alert-info mt-3">
                                <small>
                                    <strong>Примеры структур:</strong><br>
                                    <strong>Spelling:</strong> {"words": ["apple", "banana"], "instructions": "Напишите слова правильно"}<br>
                                    <strong>Drag and Drop:</strong> {"pairs": [{"russian": "собака", "english": "dog"}], "instructions": "Сопоставьте слова"}<br>
                                    <strong>Letter Soup:</strong> {"grid": "a,b,c\nd,e,f\ng,h,i", "words": ["dog", "cat"], "instructions": "Найдите слова"}
                                </small>
                            </div>
                        </div>
                        
                        <div class="mt-4">
                            <button type="submit" class="btn btn-primary btn-lg">
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
document.addEventListener('DOMContentLoaded', function() {
    // Автоформатирование JSON
    document.getElementById('formatJson').addEventListener('click', function() {
        const textarea = document.getElementById('{{ form.exercise_data_raw.id_for_label }}');
        try {
            const parsed = JSON.parse(textarea.value);
            textarea.value = JSON.stringify(parsed, null, 2);
            showToast('success', 'JSON отформатирован', 'Структура успешно отформатирована');
        } catch (e) {
            showToast('error', 'Ошибка', 'Некорректный JSON формат');
        }
    });
    
    // Валидация JSON
    document.getElementById('validateJson').addEventListener('click', function() {
        const textarea = document.getElementById('{{ form.exercise_data_raw.id_for_label }}');
        try {
            JSON.parse(textarea.value);
            showToast('success', 'JSON валиден', 'Структура JSON корректна');
        } catch (e) {
            showToast('error', 'Ошибка', 'Ошибка в JSON: ' + e.message);
        }
    });
    
    // Показываем пример при выборе типа упражнения
    document.getElementById('{{ form.exercise_type.id_for_label }}').addEventListener('change', function() {
        const examples = {
            'spelling': '{\n  "words": ["apple", "banana", "cherry"],\n  "instructions": "Напишите слова правильно",\n  "hints": ["фрукт", "фрукт", "ягода"]\n}',
            'drag_and_drop': '{\n  "pairs": [\n    {"russian": "собака", "english": "dog"},\n    {"russian": "кот", "english": "cat"}\n  ],\n  "instructions": "Сопоставьте русские и английские слова"\n}',
            'letter_soup': '{\n  "grid": "a,p,p,l,e\nd,o,g,x,x\nc,a,t,x,x",\n  "words": ["apple", "dog", "cat"],\n  "instructions": "Найдите слова в сетке"\n}'
        };
        
        const textarea = document.getElementById('{{ form.exercise_data_raw.id_for_label }}');
        if (examples[this.value] && !textarea.value.trim()) {
            if (confirm('Хотите загрузить пример структуры для этого типа упражнения?')) {
                textarea.value = examples[this.value];
            }
        }
    });
    
    // Вспомогательная функция для уведомлений
    function showToast(type, title, message) {
        // Простая реализация - можно заменить на Bootstrap Toast
        alert(`${title}: ${message}`);
    }
});
</script>
{% endblock %}
```
---

## `exercises\templates\exercises\detail.html`

```text
{% extends 'base.html' %}
{% block title %}{{ exercise.title }}{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-lg-10">
            <div class="card shadow">
                <div class="card-header {% if exercise.is_overdue %}bg-danger text-white{% else %}bg-primary text-white{% endif %}">
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="mb-0">{{ exercise.title }}</h4>
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
                            <h5>Результаты</h5>
                            <table class="table table-sm">
                                <tr>
                                    <th width="40%">Попытки:</th>
                                    <td>{{ exercise.attempts }} / {{ exercise.max_attempts }}</td>
                                </tr>
                                <tr>
                                    <th>Баллы:</th>
                                    <td>{{ exercise.score }} / {{ exercise.max_score }}</td>
                                </tr>
                                <tr>
                                    <th>Процент:</th>
                                    <td>
                                        {% if exercise.max_score > 0 %}
                                            {{ exercise.score|floatformat:0 }}%
                                        {% else %}
                                            -
                                        {% endif %}
                                    </td>
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
                                <pre class="bg-dark text-light p-3 rounded" style="max-height: 300px; overflow: auto;"><code>{{ exercise.exercise_data|pprint }}</code></pre>
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
                            {% if exercise.can_attempt %}
                                <a href="{% url 'exercises:start_exercise' exercise.id %}" class="btn btn-primary btn-lg">
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
                                        <i class="bi bi-x-circle me-2"></i>Попытки исчерпаны
                                    {% endif %}
                                </button>
                            {% endif %}
                        {% endif %}
                        
                        {% if is_teacher %}
                            <div class="btn-group">
                                <a href="{% url 'exercises:delete_exercise' exercise.id %}" 
                                   class="btn btn-danger"
                                   onclick="return confirm('Удалить упражнение?')">
                                    <i class="bi bi-trash me-2"></i>Удалить
                                </a>
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

<style>
    .bg-not_started { background-color: #6c757d; }
    .bg-in_progress { background-color: #ffc107; color: #000; }
    .bg-completed { background-color: #198754; }
    .bg-graded { background-color: #0d6efd; }
</style>
{% endblock %}
```
---

## `exercises\templates\exercises\list.html`

```text
{% extends 'base.html' %}
{% block title %}Упражнения - Учитель{% endblock %}

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
                                                <span>{{ exercise.title|truncatechars:30 }}</span>
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
                                    <th>Название</th>
                                    <th>Тип</th>
                                    <th>Статус</th>
                                    <th>Попытки</th>
                                    <th>Баллы</th>
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
                                                {{ exercise.title|truncatechars:40 }}
                                            </a>
                                        </td>
                                        <td>
                                            <span class="badge bg-info">
                                                {{ exercise.get_exercise_type_display }}
                                            </span>
                                        </td>
                                        <td>
                                            <span class="badge bg-{{ exercise.status }}" 
                                                  id="status-{{ exercise.id }}">
                                                {{ exercise.get_status_display }}
                                            </span>
                                        </td>
                                        <td>
                                            {{ exercise.attempts }}/{{ exercise.max_attempts }}
                                        </td>
                                        <td>
                                            {{ exercise.score }}/{{ exercise.max_score }}
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
                                                <a href="{% url 'exercises:delete_exercise' exercise.id %}" 
                                                   class="btn btn-outline-danger" title="Удалить"
                                                   onclick="return confirm('Удалить упражнение?')">
                                                    <i class="bi bi-trash"></i>
                                                </a>
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

<style>
    .bg-not_started { background-color: #6c757d; }
    .bg-in_progress { background-color: #ffc107; }
    .bg-completed { background-color: #198754; }
    .bg-graded { background-color: #0d6efd; }
</style>

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
                                            <h5 class="card-title">{{ exercise.title }}</h5>
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
                                                <a href="{% url 'exercises:start_exercise' exercise.id %}" 
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
    last_reviewed = models.DateTimeField("Последнее повторение", null=True, blank=True)
    next_review = models.DateTimeField("Следующее повторение", null=True, blank=True)
    review_count = models.IntegerField("Количество повторений", default=0)
    correct_answers = models.IntegerField("Правильных ответов", default=0)
    wrong_answers = models.IntegerField("Неправильных ответов", default=0)

    class Meta:
        unique_together = ('student', 'word')
        ordering = ['-assigned_at']
        verbose_name = "Назначенное слово"
        verbose_name_plural = "Назначенные слова"

    def __str__(self):
        return f"{self.student} ← {self.word}"

    def update_review_date(self, is_correct=True):
        """Обновить дату следующего повторения по алгоритму интервального повторения"""
        from django.utils import timezone
        from datetime import timedelta

        self.last_reviewed = timezone.now()

        if is_correct:
            self.correct_answers += 1
            # Увеличиваем интервал повторения
            intervals = [1, 3, 7, 14, 30]  # дни
            level = min(self.review_count, len(intervals) - 1)
            days = intervals[level]
            self.next_review = timezone.now() + timedelta(days=days)
            self.review_count += 1

            if self.review_count >= 5:  # После 5 правильных повторений
                self.status = 'completed'
        else:
            self.wrong_answers += 1
            # Уменьшаем интервал
            self.next_review = timezone.now() + timedelta(days=1)
            self.status = 'review'

        self.save()

    def get_mastery_level(self):
        """Уровень владения словом от 0 до 100%"""
        total = self.correct_answers + self.wrong_answers
        if total == 0:
            return 0
        return int((self.correct_answers / total) * 100)


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
    # Для студентов
    path('student/words/', views.student_words_list, name='student_words'),
    path('student/practice/', views.practice_session, name='practice'),
    path('update_word_status/', views.update_word_status, name='update_word_status'),
    path('mark_reviewed/', views.mark_word_reviewed, name='mark_reviewed'), ]

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


@login_required
def practice_session(request):
    """Сессия тренировки слов"""
    if not request.user.is_student():
        return redirect('dashboard:home')

    # Получаем слова для тренировки
    today = timezone.now()
    student_words = StudentWord.objects.filter(
        student=request.user,
        next_review__lte=today,
        status__in=['new', 'learning', 'review']
    ).select_related('word', 'word__topic').order_by('next_review')[:20]

    if not student_words.exists():
        # Если нет слов для повторения, берем новые
        student_words = StudentWord.objects.filter(
            student=request.user,
            status='new'
        ).select_related('word', 'word__topic')[:10]

    # Сериализуем слова в JSON
    words_list = []
    for student_word in student_words:
        words_list.append({
            'id': student_word.id,
            'word': {
                'russian': student_word.word.russian,
                'english': student_word.word.english,
                'topic_name': student_word.word.topic.name if student_word.word.topic else '',
                'topic_color': student_word.word.topic.color if student_word.word.topic else '#6c757d',
            },
            'status': student_word.status,
            'status_display': student_word.get_status_display(),
        })

    # Преобразуем в JSON строку
    import json
    words_json = json.dumps(words_list)

    return render(request, 'vocabulary/practice.html', {
        'words': words_json,
        'total_words': len(words_list)
    })

@login_required
@require_POST
def mark_word_reviewed(request):
    """Отметить слово как повторенное (правильно/неправильно)"""
    if not request.user.is_student():
        return JsonResponse({'success': False, 'error': 'Доступ запрещен'})

    try:
        data = json.loads(request.body)
        word_id = data.get('word_id')
        is_correct = data.get('is_correct', True)

        student_word = StudentWord.objects.get(id=word_id, student=request.user)
        student_word.update_review_date(is_correct=is_correct)

        return JsonResponse({
            'success': True,
            'status': student_word.status,
            'next_review': student_word.next_review.strftime('%d.%m.%Y') if student_word.next_review else None,
            'mastery': student_word.get_mastery_level()
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
```
---

## `vocabulary\__init__.py`

```text

```
---

## `vocabulary\templates\vocabulary\practice.html`

```text
{% extends 'base.html' %}
{% block title %}Тренировка слов{% endblock %}

{% block extra_style %}
<style>
    .flashcard {
        min-height: 300px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
        cursor: pointer;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        margin: 20px 0;
    }
    .progress-bar {
        transition: width 0.3s ease;
    }
</style>
{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <h4 class="mb-0">Тренировка слов</h4>
                        <div class="text-center">
                            <span id="current-word">0</span> из <span id="total-words">{{ total_words }}</span>
                        </div>
                    </div>
                </div>

                <div class="card-body">
                    <!-- Прогресс-бар -->
                    <div class="progress mb-4" style="height: 10px;">
                        <div id="practice-progress" class="progress-bar bg-success" role="progressbar"
                             style="width: 0%"></div>
                    </div>

                    <!-- Карточка слова -->
                    <div id="flashcard" class="flashcard">
                        <div id="word-front" class="text-center">
                            <h2 id="current-russian" class="display-4 mb-3">Загрузка...</h2>
                            <small class="text-muted">Нажмите на карточку, чтобы увидеть перевод</small>
                        </div>
                        <div id="word-back" class="text-center" style="display: none;">
                            <h2 id="current-english" class="display-4 text-primary mb-3"></h2>
                            <div id="word-info" class="mt-3"></div>
                        </div>
                    </div>

                    <!-- Кнопки ответов -->
                    <div id="answer-buttons" class="text-center mb-4" style="display: none;">
                        <h5 class="mb-3">Вы знали это слово?</h5>
                        <button class="btn btn-success btn-lg me-3" onclick="answerCorrect()">
                            <i class="bi bi-check-circle me-2"></i>Да, знаю
                        </button>
                        <button class="btn btn-danger btn-lg" onclick="answerWrong()">
                            <i class="bi bi-x-circle me-2"></i>Нет, не знал
                        </button>
                    </div>

                    <!-- Кнопка следующего слова -->
                    <div id="next-button" class="text-center" style="display: none;">
                        <button class="btn btn-primary btn-lg" onclick="nextWord()">
                            Следующее слово <i class="bi bi-arrow-right ms-2"></i>
                        </button>
                    </div>
                </div>

                <div class="card-footer text-center">
                    <small class="text-muted">
                        <i class="bi bi-info-circle me-1"></i>
                        Правильные ответы увеличивают интервал повторения, неправильные - уменьшают
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Скрытый элемент с данными слов -->
<script type="application/json" id="words-data">
{{ words|safe }}
</script>

<script>
// Глобальные переменные
let words = [];
let currentIndex = 0;
let totalWords = 0;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные из скрытого элемента
    const wordsDataElement = document.getElementById('words-data');

    if (wordsDataElement) {
        try {
            // Парсим JSON из элемента
            const jsonText = wordsDataElement.textContent.trim();

            if (jsonText) {
                words = JSON.parse(jsonText);
                totalWords = words.length;

                if (totalWords > 0) {
                    loadWord(0);
                    updateProgress();
                    updateWordCounter();

                    // Добавляем обработчик клика на карточку
                    document.getElementById('flashcard').addEventListener('click', function() {
                        if (document.getElementById('word-front').style.display !== 'none') {
                            showTranslation();
                        }
                    });
                } else {
                    showNoWordsMessage();
                }
            } else {
                showNoWordsMessage();
            }
        } catch (error) {
            console.error('Ошибка при парсинге JSON:', error);
            showErrorMessage('Ошибка загрузки данных');
        }
    } else {
        showErrorMessage('Элемент с данными не найден');
    }
});

function showNoWordsMessage() {
    document.getElementById('flashcard').innerHTML =
        '<div class="text-center">' +
        '<i class="bi bi-emoji-frown display-1 text-muted mb-3"></i>' +
        '<h3>Нет слов для повторения!</h3>' +
        '<p>Все слова изучены или нет назначенных слов.</p>' +
        '<a href="{% url "dashboard:student" %}" class="btn btn-primary mt-3">' +
        'Вернуться в кабинет</a>' +
        '</div>';
}

function showErrorMessage(message) {
    document.getElementById('flashcard').innerHTML =
        '<div class="text-center">' +
        '<i class="bi bi-exclamation-triangle display-1 text-danger mb-3"></i>' +
        '<h3>Ошибка</h3>' +
        '<p>' + message + '</p>' +
        '<a href="{% url "dashboard:student" %}" class="btn btn-primary mt-3">' +
        'Вернуться в кабинет</a>' +
        '</div>';
}

function updateWordCounter() {
    document.getElementById('current-word').textContent = currentIndex + 1;
    document.getElementById('total-words').textContent = totalWords;
}

function loadWord(index) {
    if (index >= words.length) {
        // Тренировка завершена
        document.getElementById('flashcard').innerHTML = `
            <div class="text-center">
                <i class="bi bi-check-circle display-1 text-success mb-3"></i>
                <h3>Тренировка завершена!</h3>
                <p>Вы повторили все слова на сегодня.</p>
                <a href="{% url 'dashboard:student' %}" class="btn btn-primary mt-3">
                    Вернуться в кабинет
                </a>
            </div>
        `;
        document.getElementById('answer-buttons').style.display = 'none';
        document.getElementById('next-button').style.display = 'none';
        return;
    }

    const word = words[index];
    document.getElementById('current-russian').textContent = word.word.russian;
    document.getElementById('current-english').textContent = word.word.english;

    let infoHtml = '';
    if (word.word.topic_name) {
        infoHtml += `<span class="badge me-2" style="background: ${word.word.topic_color}">${word.word.topic_name}</span>`;
    }
    infoHtml += `<small class="text-muted d-block mt-2">Статус: ${word.status_display}</small>`;
    document.getElementById('word-info').innerHTML = infoHtml;

    // Сбрасываем отображение
    document.getElementById('word-back').style.display = 'none';
    document.getElementById('word-front').style.display = 'block';
    document.getElementById('answer-buttons').style.display = 'none';
    document.getElementById('next-button').style.display = 'none';

    updateProgress();
}

function showTranslation() {
    document.getElementById('word-front').style.display = 'none';
    document.getElementById('word-back').style.display = 'block';
    document.getElementById('answer-buttons').style.display = 'block';
}

function answerCorrect() {
    markWord(true);
    showNextButton();
}

function answerWrong() {
    markWord(false);
    showNextButton();
}

function markWord(isCorrect) {
    const word = words[currentIndex];

    // Отправляем запрос на сервер
    fetch('{% url "vocabulary:mark_reviewed" %}', {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            word_id: word.id,
            is_correct: isCorrect
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Сетевая ошибка');
        }
        return response.json();
    })
    .then(data => {
        if (!data.success) {
            console.error('Ошибка сервера:', data.error);
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
    });
}

function showNextButton() {
    document.getElementById('answer-buttons').style.display = 'none';
    document.getElementById('next-button').style.display = 'block';
}

function nextWord() {
    currentIndex++;
    if (currentIndex < words.length) {
        loadWord(currentIndex);
        updateWordCounter();
    } else {
        loadWord(words.length); // Завершение тренировки
    }
}

function updateProgress() {
    if (totalWords === 0) return;
    const progress = ((currentIndex) / totalWords) * 100;
    document.getElementById('practice-progress').style.width = progress + '%';
}
</script>
{% endblock %}
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

