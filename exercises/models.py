from django.db import models
from django.conf import settings
import json


class Exercise(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [
        ('homework', 'Домашняя работа'),
        ('classwork', 'Работа на уроке'),
        ('test', 'Контрольная работа'),
    ]

    EXERCISE_TYPE_CHOICES = [
        ('spelling', 'Правописание (Spelling)'),
        ('drag_and_drop', 'Перетаскивание (Drag and Drop)'),
        ('letter_soup', 'Буквенный суп (Letter Soup)'),
    ]

    STATUS_CHOICES = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнено'),
        ('graded', 'Проверено'),
    ]

    # Основные поля
    title = models.CharField('Название задания', max_length=200)
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
    exercise_type = models.CharField(
        'Вид упражнения',
        max_length=20,
        choices=EXERCISE_TYPE_CHOICES,
        default='spelling'
    )

    # Статус и попытки
    status = models.CharField(
        'Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )
    attempts = models.IntegerField('Количество попыток', default=0)
    max_attempts = models.IntegerField('Максимум попыток', default=3)

    # Данные упражнения
    exercise_data = models.JSONField('Данные упражнения', default=dict)

    # Даты
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    due_date = models.DateTimeField('Срок выполнения', null=True, blank=True)
    completed_at = models.DateTimeField('Завершено', null=True, blank=True)

    # Результаты
    score = models.IntegerField('Баллы', default=0)
    max_score = models.IntegerField('Максимум баллов', default=100)
    teacher_comment = models.TextField('Комментарий учителя', blank=True)

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student}"

    def is_overdue(self):
        from django.utils import timezone
        if self.due_date and timezone.now() > self.due_date:
            return True
        return False

    def can_attempt(self):
        if self.attempts >= self.max_attempts:
            return False
        if self.status in ['completed', 'graded']:
            return False
        return True

    def start_attempt(self):
        from django.utils import timezone
        self.attempts += 1
        self.status = 'in_progress'
        self.save()

    def complete_attempt(self, score):
        from django.utils import timezone
        self.score = score
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()