from django import forms
from .models import Exercise
from users.models import User
from vocabulary.models import Word
from .utils import generate_letter_soup
import json


class ExerciseCreateForm(forms.ModelForm):
    # Поле для выбора слов (множественный выбор)
    word_selection = forms.MultipleChoiceField(
        choices=[],
        widget=forms.MultipleHiddenInput(),
        required=True,
        error_messages={'required': 'Выберите хотя бы одно слово'}
    )

    class Meta:
        model = Exercise
        fields = [
            'description', 'student',
            'assignment_type', 'exercise_type',
            'due_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Например: Найдите слова в буквенном супе'
            }),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'exercise_type': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        if teacher:
            # Ограничиваем выбор учеников только теми, кто связан с этим учителем
            self.fields['student'].queryset = User.objects.filter(role='student')

        # Динамически установим choices для word_selection
        if 'student' in self.initial and self.initial['student']:
            self.set_word_choices(self.initial['student'])

    def set_word_choices(self, student):
        """Установить choices для поля word_selection"""
        if isinstance(student, int):
            student_id = student
        else:
            student_id = student.id

        # Получаем слова, назначенные ученику
        assigned_words = Word.objects.filter(
            studentword__student_id=student_id
        ).distinct()

        # Формируем choices
        choices = [(word.id, f"{word.russian} - {word.english}")
                   for word in assigned_words]
        self.fields['word_selection'].choices = choices

    def clean(self):
        cleaned_data = super().clean()

        # Проверяем, что выбраны слова
        word_selection = cleaned_data.get('word_selection')
        if not word_selection:
            self.add_error('word_selection', 'Выберите хотя бы одно слово')

        return cleaned_data

    def save(self, commit=True):
        exercise = super().save(commit=False)
        teacher = self.initial.get('teacher')
        if teacher:
            exercise.teacher = teacher

        # Формируем данные упражнения из выбранных слов
        selected_word_ids = self.cleaned_data.get('word_selection', [])

        # Получаем объекты слов
        words = Word.objects.filter(id__in=selected_word_ids)

        # Формируем пары слов
        pairs = []
        english_words = []

        for word in words:
            pairs.append({
                'russian': word.russian,
                'english': word.english.lower()
            })
            english_words.append(word.english.lower())

        # Формируем exercise_data в зависимости от типа упражнения
        exercise_type = self.cleaned_data['exercise_type']

        if exercise_type in ['spelling', 'drag_and_drop']:
            exercise.exercise_data = {
                'pairs': pairs,
                'instructions': self.cleaned_data.get('description', '')
            }
        elif exercise_type == 'letter_soup':
            # Генерируем буквенный суп с автоматическим расчетом размера сетки
            grid, placed_words = generate_letter_soup(english_words)  # grid_size=None по умолчанию

            exercise.exercise_data = {
                'pairs': pairs,
                'english_words': english_words,
                'grid': grid,
                'placed_words': placed_words,
                'grid_size': len(grid),  # динамический размер
                'instructions': self.cleaned_data.get('description', '') or 'Найдите английские слова в сетке'
            }

        if commit:
            exercise.save()

        return exercise