from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from users.models import User
from vocabulary.models import StudentWord,  Topic


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

    # Статистика
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
        'topics_with_progress': topics_with_progress,
        'recent_words': recent_words,
        'weekly_stats': weekly_stats,
    }
    return render(request, 'dashboard/student.html', context)