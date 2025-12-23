# exercises/admin.py
from django.contrib import admin
from .models import Exercise, SpellingExercise, DragDropExercise, LetterSoupExercise  # Изменяем импорты


class SpellingExerciseInline(admin.StackedInline):
    model = SpellingExercise
    extra = 0


class DragDropExerciseInline(admin.StackedInline):
    model = DragDropExercise
    extra = 0


class LetterSoupExerciseInline(admin.StackedInline):
    model = LetterSoupExercise
    extra = 0


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'teacher', 'assignment_type', 'exercise_type', 'status', 'due_date')
    list_filter = ('assignment_type', 'exercise_type', 'status', 'teacher', 'student')
    search_fields = ('description', 'student__username', 'teacher__username')
    readonly_fields = ('created_at', 'updated_at')

    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            if obj.exercise_type == 'spelling':
                inlines.append(SpellingExerciseInline(self.model, self.admin_site))
            elif obj.exercise_type == 'drag_drop':
                inlines.append(DragDropExerciseInline(self.model, self.admin_site))
            elif obj.exercise_type == 'letter_soup':
                inlines.append(LetterSoupExerciseInline(self.model, self.admin_site))
        return inlines


@admin.register(SpellingExercise)
class SpellingExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'pairs_count')

    def pairs_count(self, obj):
        return len(obj.pairs)

    pairs_count.short_description = 'Количество пар'


@admin.register(DragDropExercise)
class DragDropExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'pairs_count')

    def pairs_count(self, obj):
        return len(obj.pairs)

    pairs_count.short_description = 'Количество пар'


@admin.register(LetterSoupExercise)
class LetterSoupExerciseAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'grid_size', 'words_count')

    def words_count(self, obj):
        return len(obj.words)

    words_count.short_description = 'Количество слов'