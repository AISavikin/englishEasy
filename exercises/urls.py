# exercises/urls.py
from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    # Выбор типа упражнения
    path('select_type/', views.select_exercise_type, name='select_type'),
    path('select_type/<int:student_id>/', views.select_exercise_type, name='select_type_for_student'),

    # Создание разных типов упражнений
    path('create/spelling_drag_drop/', views.create_spelling_drag_drop, name='create_spelling_drag_drop'),
    path('create/spelling_drag_drop/<int:student_id>/', views.create_spelling_drag_drop,
         name='create_spelling_drag_drop_for_student'),
    path('create/letter_soup/', views.create_letter_soup, name='create_letter_soup'),
    path('create/letter_soup/<int:student_id>/', views.create_letter_soup, name='create_letter_soup_for_student'),

    # Общие URL (оставляем для совместимости)
    path('create/', views.create_spelling_drag_drop, name='create_exercise'),
    path('create/<int:student_id>/', views.create_spelling_drag_drop, name='create_exercise_for_student'),

    # Просмотр списков
    path('teacher/', views.teacher_exercises_list, name='teacher_exercises'),
    path('teacher/<int:student_id>/', views.teacher_exercises_list, name='teacher_exercises_for_student'),
    path('my/', views.student_exercises_list, name='my_exercises'),

    # Детали упражнения
    path('detail/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),

    # Выполнение упражнений
    path('do/<int:exercise_id>/', views.do_exercise, name='do_exercise'),
    path('complete/<int:exercise_id>/', views.complete_exercise, name='complete_exercise'),

    # Действия с упражнением
    path('delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('update_status/<int:exercise_id>/', views.update_exercise_status, name='update_exercise_status'),
    path('update_word_stat/<int:exercise_id>/', views.update_word_stat, name='update_word_stat'),
    # Новые маршруты для Drag & Drop
    path('create/drag_drop/', views.create_drag_drop, name='create_drag_drop'),
    path('create/drag_drop/<int:student_id>/', views.create_drag_drop,
         name='create_drag_drop_for_student'),

]
