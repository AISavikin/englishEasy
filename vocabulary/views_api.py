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