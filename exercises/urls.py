from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    # Создание упражнения
    path('create/', views.create_exercise, name='create_exercise'),
    path('create/<int:student_id>/', views.create_exercise, name='create_exercise_for_student'),

    # Просмотр списков
    path('teacher/', views.teacher_exercises_list, name='teacher_exercises'),
    path('teacher/<int:student_id>/', views.teacher_exercises_list, name='teacher_exercises_for_student'),
    path('my/', views.student_exercises_list, name='my_exercises'),

    # Детали упражнения
    path('detail/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),

    # Действия с упражнением
    path('start/<int:exercise_id>/', views.start_exercise, name='start_exercise'),
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('update_status/<int:exercise_id>/', views.update_exercise_status, name='update_exercise_status'),
]