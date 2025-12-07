from django.db import models
from django.conf import settings
from django.utils import timezone
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
    word = models.ForeignKey('Word', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField("Назначено", auto_now_add=True)
    status = models.CharField("Статус", max_length=10, choices=STATUS_CHOICES, default='new')

    # Детальная статистика
    times_seen = models.IntegerField("Показов слова", default=0)
    times_attempted = models.IntegerField("Попыток ответа", default=0)
    times_correct = models.IntegerField("Правильных ответов", default=0)
    times_wrong = models.IntegerField("Неправильных ответов", default=0)
    total_response_time = models.IntegerField("Общее время ответов (мс)", default=0)
    avg_response_time = models.FloatField("Среднее время ответа (мс)", default=0.0)

    # Серии и прогресс
    current_streak = models.IntegerField("Текущая серия правильных", default=0)
    longest_streak = models.IntegerField("Лучшая серия правильных", default=0)
    last_correct_date = models.DateTimeField("Последний правильный ответ", null=True, blank=True)

    # Для аналитики
    first_seen = models.DateTimeField("Первое знакомство", auto_now_add=True)
    last_interaction = models.DateTimeField("Последнее взаимодействие", auto_now=True)

    class Meta:
        unique_together = ('student', 'word')
        ordering = ['-assigned_at']
        verbose_name = "Назначенное слово"
        verbose_name_plural = "Назначенные слова"

    def __str__(self):
        return f"{self.student} ← {self.word}"

    def update_statistics(self, is_correct=True, response_time=0):
        """Обновление статистики после взаимодействия со словом"""
        self.times_seen += 1
        self.times_attempted += 1
        self.total_response_time += response_time

        if is_correct:
            self.times_correct += 1
            self.current_streak += 1
            self.last_correct_date = timezone.now()

            # Обновляем лучшую серию
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak

            # Автоматически обновляем статус на основе статистики
            if self.times_correct >= 5 and self.current_streak >= 3:
                self.status = 'completed'
            elif self.times_correct >= 2:
                self.status = 'learning'
        else:
            self.times_wrong += 1
            self.current_streak = 0

            if self.status == 'completed' and self.current_streak == 0:
                self.status = 'review'

        # Обновляем среднее время ответа
        if self.times_attempted > 0:
            self.avg_response_time = self.total_response_time / self.times_attempted

        # Обновляем дату последнего взаимодействия
        self.last_interaction = timezone.now()
        self.save()

    def get_accuracy_percentage(self):
        """Возвращает процент правильных ответов"""
        if self.times_attempted == 0:
            return 0
        return (self.times_correct / self.times_attempted) * 100

    def get_days_since_last_seen(self):
        """Возвращает количество дней с последнего взаимодействия"""
        if not self.last_interaction:
            return None
        delta = timezone.now() - self.last_interaction
        return delta.days

    def get_mastery_level(self):
        """Определяет уровень владения словом"""
        accuracy = self.get_accuracy_percentage()

        if self.times_attempted == 0:
            return "Не изучено"
        elif accuracy >= 90 and self.current_streak >= 5:
            return "Мастер"
        elif accuracy >= 80 and self.current_streak >= 3:
            return "Продвинутый"
        elif accuracy >= 70:
            return "Средний"
        elif accuracy >= 50:
            return "Начинающий"
        else:
            return "Новичок"

    def reset_progress(self):
        """Сброс прогресса для слова"""
        self.times_seen = 0
        self.times_attempted = 0
        self.times_correct = 0
        self.times_wrong = 0
        self.total_response_time = 0
        self.avg_response_time = 0.0
        self.current_streak = 0
        self.status = 'new'
        self.last_correct_date = None
        self.save()
