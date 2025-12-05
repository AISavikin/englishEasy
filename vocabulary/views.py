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