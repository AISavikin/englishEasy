from django.contrib import admin
from .models import Exercise

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'teacher', 'assignment_type', 'exercise_type', 'status', 'score', 'due_date')
    list_filter = ('assignment_type', 'exercise_type', 'status', 'teacher', 'student')
    search_fields = ('title', 'description', 'student__username', 'teacher__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'student', 'teacher')
        }),
        ('Типы и статус', {
            'fields': ('assignment_type', 'exercise_type', 'status')
        }),
        ('Попытки и баллы', {
            'fields': ('attempts', 'max_attempts', 'score', 'max_score')
        }),
        ('Даты', {
            'fields': ('due_date', 'completed_at', 'created_at', 'updated_at')
        }),
        ('Данные', {
            'fields': ('exercise_data', 'teacher_comment')
        }),
    )