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