from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from vocabulary.models import StudentWord
from .forms import SpellingDragDropExerciseForm, LetterSoupExerciseForm
from .models import Exercise, SpellingDragDropExercise, LetterSoupExercise
from users.models import User
import json


@login_required
def select_exercise_type(request, student_id=None):
    """Страница выбора типа упражнения"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    student = None
    if student_id:
        student = get_object_or_404(User, id=student_id, role='student')

    return render(request, 'exercises/select_type.html', {
        'student': student,
        'students': User.objects.filter(role='student')
    })


@login_required
def create_spelling_drag_drop(request, student_id=None):
    """Создание упражнения Spelling/Drag & Drop"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    student = None
    if student_id:
        student = get_object_or_404(User, id=student_id, role='student')

    if request.method == 'POST':
        form = SpellingDragDropExerciseForm(
            request.POST,
            teacher=request.user,
            initial={'teacher': request.user}
        )

        if form.is_valid():
            exercise = form.save()
            messages.success(request,
                             f'Упражнение типа "{exercise.get_exercise_type_display()}" создано!')

            # Получаем конкретное упражнение для отображения подтипа
            concrete_exercise = exercise.get_concrete_exercise()
            if concrete_exercise and hasattr(concrete_exercise, 'type'):
                messages.success(request, f'Тип упражнения: {concrete_exercise.get_type_display()}')

            return redirect('vocabulary:teacher_panel', student_id=exercise.student.id)
        else:
            # Показываем ошибки формы
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        initial = {'teacher': request.user}
        if student:
            initial['student'] = student

        form = SpellingDragDropExerciseForm(initial=initial, teacher=request.user)

    return render(request, 'exercises/create_spelling_drag_drop.html', {
        'form': form,
        'student': student,
        'students': User.objects.filter(role='student')
    })


@login_required
def create_letter_soup(request, student_id=None):
    """Создание упражнения Letter Soup"""
    if not request.user.is_teacher():
        return redirect('dashboard:home')

    student = None
    if student_id:
        student = get_object_or_404(User, id=student_id, role='student')

    if request.method == 'POST':
        form = LetterSoupExerciseForm(
            request.POST,
            teacher=request.user,
            initial={'teacher': request.user}
        )



        if form.is_valid():
            exercise = form.save()
            messages.success(request, 'Упражнение "Буквенный суп" создано!')
            return redirect('vocabulary:teacher_panel', student_id=exercise.student.id)
    else:
        initial = {'teacher': request.user}
        if student:
            initial['student'] = student

        form = LetterSoupExerciseForm(initial=initial, teacher=request.user)


    return render(request, 'exercises/create_letter_soup.html', {
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
# exercises/views.py - обновим do_exercise
@login_required
def do_exercise(request, exercise_id):
    """Выполнение упражнения"""
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if not request.user == exercise.student:
        messages.error(request, 'Только ученик может выполнять это упражнение')
        return redirect('dashboard:home')

    if exercise.status in ['completed', 'graded']:
        messages.warning(request, 'Задание уже выполнено или проверено')
        return redirect('exercises:my_exercises')

    if exercise.status == 'not_started':
        exercise.start_attempt()

    concrete_exercise = exercise.get_concrete_exercise()

    if exercise.exercise_type == 'spelling_drag_drop':
        spelling_exercise = concrete_exercise
        if spelling_exercise.type == 'spelling':
            return render(request, 'exercises/spelling.html', {
                'exercise': exercise,
                'spelling_exercise': spelling_exercise,
                'pairs': spelling_exercise.pairs,
                'pairs_json': json.dumps(spelling_exercise.pairs),
            })
        else:  # drag_and_drop
            return render(request, 'exercises/drag_and_drop.html', {
                'exercise': exercise,
                'spelling_exercise': spelling_exercise,
                'pairs': spelling_exercise.pairs,
                'pairs_json': json.dumps(spelling_exercise.pairs),
            })

    elif exercise.exercise_type == 'letter_soup':
        letter_soup = concrete_exercise
        # Получаем слова из пар
        pairs = []
        words = []

        # Получаем пары из JSON поля pairs
        if hasattr(letter_soup, 'pairs') and letter_soup.pairs:
            pairs = letter_soup.pairs
            words = [pair.get('english', '') for pair in pairs if pair.get('english')]
        else:
            # Если нет пар, берем из поля words
            words = letter_soup.words
            pairs = [{'english': word, 'russian': '???'} for word in words]

        return render(request, 'exercises/letter_soup.html', {
            'exercise': exercise,
            'letter_soup': letter_soup,
            'words': words,
            'pairs': pairs,
            'grid': letter_soup.grid,
            'placed_words': letter_soup.placed_words,
            'grid_size': letter_soup.grid_size,
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


@login_required
def update_word_stat(request, exercise_id):
    """AJAX-обновление статистики StudentWord при проверке слова"""
    if request.method == 'POST':
        exercise = get_object_or_404(Exercise, id=exercise_id)

        # Проверка прав: только студент упражнения
        if request.user != exercise.student:
            return JsonResponse({'success': False, 'error': 'Нет доступа'})

        # Получаем данные из POST
        word_id = request.POST.get('word_id')
        is_correct_str = request.POST.get('is_correct', 'false')
        is_correct = is_correct_str.lower() == 'true'
        response_time_str = request.POST.get('response_time', '0')
        try:
            response_time = float(response_time_str)
        except ValueError:
            response_time = 0.0

        if not word_id:
            return JsonResponse({'success': False, 'error': 'Отсутствует word_id'})

        try:
            # Находим StudentWord
            student_word = StudentWord.objects.get(student=exercise.student, word__id=word_id)

            # Обновляем статистику
            student_word.update_statistics(is_correct=is_correct, response_time=response_time)

            return JsonResponse({'success': True})
        except StudentWord.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Слово не назначено студенту'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Неверный метод запроса'})