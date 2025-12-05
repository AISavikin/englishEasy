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