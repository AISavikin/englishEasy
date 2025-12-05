from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from users.models import User
from vocabulary.models import StudentWord, Assignment


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

    return render(request, 'dashboard/student.html', {
        'assigned_words': assigned_words  # ДОБАВИТЬ
    })