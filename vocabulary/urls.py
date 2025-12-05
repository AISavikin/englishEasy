# vocabulary/urls.py

from django.urls import path
from . import views

app_name = 'vocabulary'

urlpatterns = [
    # Страница выбора ученика
    path('select_student/', views.select_student, name='select_student'),

    # Панель учителя для конкретного ученика
    path('teacher_panel/<int:student_id>/', views.teacher_panel, name='teacher_panel'),

    # AJAX-запросы
    path('word/create/ajax/', views.word_create_ajax, name='word_create_ajax'),
    path('topic/create/ajax/', views.topic_create_ajax, name='topic_create_ajax'),
    path('word/delete/ajax/', views.word_delete_ajax, name='word_delete_ajax'),

    # Другие страницы
    path('word/create/', views.word_create, name='word_create'),
    path('assign/<int:student_id>/', views.assign_words, name='assign_words'),
    path('assignment/create/<int:student_id>/', views.create_assignment, name='create_assignment'),
    # Для студентов
    path('student/words/', views.student_words_list, name='student_words'),
    path('student/practice/', views.practice_session, name='practice'),
    path('update_word_status/', views.update_word_status, name='update_word_status'),
    path('mark_reviewed/', views.mark_word_reviewed, name='mark_reviewed'), ]
