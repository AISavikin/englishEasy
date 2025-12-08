from django.urls import path
from . import views
from .views import CustomLoginView, CustomLogoutView, RegisterView

app_name = 'users'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]