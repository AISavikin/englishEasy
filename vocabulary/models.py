from django.db import models
from django.conf import settings

from users.models import User


class Topic(models.Model):
    name = models.CharField("Название темы", max_length=100)
    color = models.CharField("Цвет (HEX)", max_length=7, default="#3B82F6")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Тема"
        verbose_name_plural = "Темы"

    def __str__(self):
        return self.name


class Word(models.Model):
    russian = models.CharField("Русский", max_length=100)
    english = models.CharField("English", max_length=100)
    topic = models.ForeignKey(
        Topic,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='words'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('russian', 'english')
        ordering = ['russian']
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def save(self, *args, **kwargs):
        self.english = self.english.strip().lower()
        self.russian = self.russian.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.russian} → {self.english}"


class StudentWord(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('learning', 'Изучается'),
        ('review', 'Повторение'),
        ('completed', 'Изучено'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_words',
        limit_choices_to={'role': 'student'}
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_words_by_teacher',
        verbose_name="Назначено учителем"
    )
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField("Назначено", auto_now_add=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='new')
    last_reviewed = models.DateTimeField("Последнее повторение", null=True, blank=True)
    next_review = models.DateTimeField("Следующее повторение", null=True, blank=True)
    review_count = models.IntegerField("Количество повторений", default=0)
    correct_answers = models.IntegerField("Правильных ответов", default=0)
    wrong_answers = models.IntegerField("Неправильных ответов", default=0)

    class Meta:
        unique_together = ('student', 'word')
        ordering = ['-assigned_at']
        verbose_name = "Назначенное слово"
        verbose_name_plural = "Назначенные слова"

    def __str__(self):
        return f"{self.student} ← {self.word}"

    def update_review_date(self, is_correct=True):
        """Обновить дату следующего повторения по алгоритму интервального повторения"""
        from django.utils import timezone
        from datetime import timedelta

        self.last_reviewed = timezone.now()

        if is_correct:
            self.correct_answers += 1
            # Увеличиваем интервал повторения
            intervals = [1, 3, 7, 14, 30]  # дни
            level = min(self.review_count, len(intervals) - 1)
            days = intervals[level]
            self.next_review = timezone.now() + timedelta(days=days)
            self.review_count += 1

            if self.review_count >= 5:  # После 5 правильных повторений
                self.status = 'completed'
        else:
            self.wrong_answers += 1
            # Уменьшаем интервал
            self.next_review = timezone.now() + timedelta(days=1)
            self.status = 'review'

        self.save()

    def get_mastery_level(self):
        """Уровень владения словом от 0 до 100%"""
        total = self.correct_answers + self.wrong_answers
        if total == 0:
            return 0
        return int((self.correct_answers / total) * 100)

