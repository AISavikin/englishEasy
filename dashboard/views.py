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