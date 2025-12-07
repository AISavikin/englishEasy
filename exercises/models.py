from django.db import models
from django.conf import settings
from django.utils import timezone

import json


# exercises/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Exercise(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [
        ('homework', 'Домашняя работа'),
        ('classwork', 'Работа на уроке'),
        ('test', 'Контрольная работа'),
    ]

    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('graded', 'Проверено'),
    ]

    # Основные поля
    description = models.TextField('Описание', blank=True)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exercises',
        limit_choices_to={'role': 'student'},
        verbose_name='Ученик'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_exercises',
        limit_choices_to={'role': 'teacher'},
        verbose_name='Учитель'
    )

    # Типы
    assignment_type = models.CharField(
        'Тип задания',
        max_length=20,
        choices=ASSIGNMENT_TYPE_CHOICES,
        default='homework'
    )

    # Статус и попытки
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )
    attempts = models.IntegerField('Количество попыток', default=0)

    # Даты
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    completed_at = models.DateTimeField('Завершено', null=True, blank=True)

    # Результаты
    teacher_comment = models.TextField('Комментарий учителя', blank=True)

    # Поле для определения типа конкретного упражнения
    exercise_type = models.CharField('Тип упражнения', max_length=50, default='spelling_drag_drop')

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['-created_at']

    def __str__(self):
        return f"Упражнение для {self.student} ({self.created_at.date()})"

    def is_overdue(self):
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False

    def start_attempt(self):
        """Начать новую попытку выполнения"""
        if self.status == 'not_started':
            self.attempts += 1
            self.status = 'in_progress'
            self.save()

    def complete_attempt(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()

    def get_concrete_exercise(self):
        """Получить конкретное упражнение в зависимости от типа"""
        if self.exercise_type == 'spelling_drag_drop':
            return self.spellingdragdropexercise
        elif self.exercise_type == 'letter_soup':
            return self.lettersoupexercise
        return None


# exercises/models.py
class SpellingDragDropExercise(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ('spelling', 'Правописание (Spelling)'),
        ('drag_and_drop', 'Перетаскивание (Drag and Drop)'),
    ]

    exercise = models.OneToOneField(
        Exercise,
        on_delete=models.CASCADE,
        related_name='spellingdragdropexercise',
        primary_key=True
    )

    type = models.CharField(
        'Тип упражнения',
        max_length=20,
        choices=EXERCISE_TYPE_CHOICES,
        default='spelling'
    )

    # Данные упражнения (пары слов)
    pairs = models.JSONField('Пары слов', default=list)

    # Дополнительные настройки
    shuffle_letters = models.BooleanField('Перемешивать буквы', default=True)
    show_hints = models.BooleanField('Показывать подсказки', default=True)

    class Meta:
        verbose_name = 'Spelling/Drag & Drop упражнение'
        verbose_name_plural = 'Spelling/Drag & Drop упражнения'

    def __str__(self):
        return f"{self.get_type_display()} - {self.exercise.student}"


# exercises/models.py
class LetterSoupExercise(models.Model):
    exercise = models.OneToOneField(
        Exercise,
        on_delete=models.CASCADE,
        related_name='lettersoupexercise',
        primary_key=True
    )

    # Слова для поиска
    words = models.JSONField('Слова для поиска', default=list)

    # Сетка букв
    grid = models.JSONField('Сетка букв', default=list)

    # Информация о размещенных словах
    placed_words = models.JSONField('Размещенные слова', default=list)

    # Настройки сетки
    grid_size = models.IntegerField('Размер сетки', default=15)
    include_backwards = models.BooleanField('Включать обратное направление', default=True)
    include_diagonals = models.BooleanField('Включать диагонали', default=False)

    class Meta:
        verbose_name = 'Letter Soup упражнение'
        verbose_name_plural = 'Letter Soup упражнения'

    def __str__(self):
        return f"Letter Soup - {self.exercise.student}"