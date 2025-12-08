from datetime import timedelta, date
from django.db.models import Sum, Count, Avg, Q
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
    # Получаем все слова студента
    student_words = StudentWord.objects.filter(student=request.user)

    # Общая статистика
    stats_detail = {
        'total_words': student_words.count(),
        'total_attempts': student_words.aggregate(Sum('times_attempted'))['times_attempted__sum'] or 0,
        'total_correct': student_words.aggregate(Sum('times_correct'))['times_correct__sum'] or 0,
        'total_wrong': student_words.aggregate(Sum('times_wrong'))['times_wrong__sum'] or 0,
        'avg_response_time': student_words.aggregate(Avg('avg_response_time'))['avg_response_time__avg'] or 0,
        'total_response_time_min': sum(
            (sw.total_response_time / 60000) for sw in student_words
        ) if student_words else 0,
    }

    # Рассчитываем проценты
    if stats_detail['total_attempts'] > 0:
        stats_detail['accuracy_percent'] = round(
            (stats_detail['total_correct'] / stats_detail['total_attempts']) * 100, 1
        )
    else:
        stats_detail['accuracy_percent'] = 0

    # Распределение по уровням владения
    mastery_levels = {}
    for word in student_words:
        level = word.get_mastery_level()
        mastery_levels[level] = mastery_levels.get(level, 0) + 1
    stats_detail['mastery_levels'] = mastery_levels

    # Слова, требующие внимания (давно не повторялись)
    words_need_review = student_words.filter(
        Q(last_interaction__lt=timezone.now() - timezone.timedelta(days=7)) |
        Q(times_wrong__gte=3)
    )[:10]

    context.update({
        'stats_detail': stats_detail,
        'words_need_review': words_need_review,
    })

    return render(request, 'dashboard/student.html', context)
