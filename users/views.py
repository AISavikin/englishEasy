from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SimpleRegisterForm


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        messages.success(self.request, f'Добро пожаловать, {self.request.user.username}!')
        return reverse_lazy('dashboard:home')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:home')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы успешно вышли из системы')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    form_class = SimpleRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('dashboard:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        messages.success(self.request, f'Аккаунт создан! Добро пожаловать, {user.username}!')
        return response


def home(request):
    """Главная страница с приветствием"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    return render(request, 'users/home.html')