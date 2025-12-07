# exercises/forms.py
from django import forms
from .models import Exercise, SpellingDragDropExercise, LetterSoupExercise
from users.models import User
from vocabulary.models import Word
from .utils import generate_letter_soup


class BaseExerciseCreateForm(forms.ModelForm):
    word_selection = forms.MultipleChoiceField(
        choices=[],
        widget=forms.MultipleHiddenInput(),
        required=True,
        error_messages={'required': 'Выберите хотя бы одно слово'}
    )

    class Meta:
        model = Exercise
        fields = ['description', 'student', 'assignment_type', 'due_date']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Например: Изучите эти слова'
            }),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
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
            self.fields['student'].queryset = User.objects.filter(role='student')

    def set_word_choices(self, student):
        """Установить choices для поля word_selection"""
        if isinstance(student, int):
            student_id = student
        else:
            student_id = student.id

        assigned_words = Word.objects.filter(
            studentword__student_id=student_id
        ).distinct()

        choices = [(word.id, f"{word.russian} - {word.english}")
                   for word in assigned_words]
        self.fields['word_selection'].choices = choices


class SpellingDragDropExerciseForm(BaseExerciseCreateForm):
    exercise_type = forms.ChoiceField(
        choices=SpellingDragDropExercise.EXERCISE_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='spelling',
        label='Тип упражнения'
    )

    class Meta(BaseExerciseCreateForm.Meta):
        fields = BaseExerciseCreateForm.Meta.fields + ['exercise_type']

    def save(self, commit=True):
        exercise = super().save(commit=False)
        teacher = self.initial.get('teacher')
        if teacher:
            exercise.teacher = teacher
            exercise.exercise_type = 'spelling_drag_drop'

        if commit:
            exercise.save()

        selected_word_ids = self.cleaned_data.get('word_selection', [])
        words = Word.objects.filter(id__in=selected_word_ids)

        pairs = []
        for word in words:
            pairs.append({
                'russian': word.russian,
                'english': word.english.lower()
            })

        SpellingDragDropExercise.objects.create(
            exercise=exercise,
            type=self.cleaned_data['exercise_type'],
            pairs=pairs
        )

        return exercise


class LetterSoupExerciseForm(BaseExerciseCreateForm):
    grid_size = forms.IntegerField(
        min_value=8,
        max_value=25,
        initial=15,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Размер сетки'
    )

    class Meta(BaseExerciseCreateForm.Meta):
        fields = BaseExerciseCreateForm.Meta.fields + ['grid_size']

    def save(self, commit=True):
        exercise = super().save(commit=False)
        teacher = self.initial.get('teacher')
        if teacher:
            exercise.teacher = teacher
            exercise.exercise_type = 'letter_soup'

        if commit:
            exercise.save()

        selected_word_ids = self.cleaned_data.get('word_selection', [])
        words = Word.objects.filter(id__in=selected_word_ids)

        english_words = [word.english.lower() for word in words]
        grid_size = self.cleaned_data.get('grid_size', 15)

        grid, placed_words = generate_letter_soup(english_words, grid_size=grid_size)

        LetterSoupExercise.objects.create(
            exercise=exercise,
            words=english_words,
            grid=grid,
            placed_words=placed_words,
            grid_size=grid_size
        )

        return exercise