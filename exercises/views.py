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