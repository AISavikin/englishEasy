# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import SimpleRegisterForm


def home(request):
    """Главная страница с формами входа и регистрации"""
    context = {}
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    # Если есть данные POST для входа
    if request.method == 'POST' and 'login-username' in request.POST:
        username = request.POST.get('login-username')
        password = request.POST.get('login-password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Неверный логин или пароль')

    # Если есть данные POST для регистрации
    elif request.method == 'POST' and 'register-username' in request.POST:
        # Создаем копию POST данных с правильными именами полей
        post_data = request.POST.copy()
        post_data['username'] = post_data.get('register-username')
        post_data['password1'] = post_data.get('register-password1')
        post_data['password2'] = post_data.get('register-password2')

        form = SimpleRegisterForm(post_data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
            return redirect('dashboard:home')
        else:
            # Сохраняем ошибки формы для отображения
            context = {'register_form': form}

    return render(request, 'users/home.html', context)


def simple_register(request):
    """Простая регистрация (альтернативный вариант)"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = SimpleRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
            return redirect('dashboard:home')
    else:
        form = SimpleRegisterForm()

    return render(request, 'users/register.html', {'form': form})
