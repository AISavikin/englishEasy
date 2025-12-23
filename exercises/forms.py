# exercises/forms.py
from django import forms
from .models import Exercise, SpellingDragDropExercise, LetterSoupExercise, DragDropExercise
from users.models import User
from vocabulary.models import Word
from .utils import generate_letter_soup


# exercises/forms.py - в BaseExerciseCreateForm замените поле word_selection

class BaseExerciseCreateForm(forms.ModelForm):
    word_selection = forms.CharField(
        widget=forms.HiddenInput(),
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

    # Удалите метод set_word_choices - он больше не нужен


# exercises/forms.py

class SpellingDragDropExerciseForm(BaseExerciseCreateForm):
    # Поле для типа упражнения внутри SpellingDragDrop (spelling или drag_and_drop)
    exercise_subtype = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
        initial='spelling'
    )

    # Поле для типа задания (домашняя, классная и т.д.) - уже есть в BaseExerciseCreateForm

    class Meta(BaseExerciseCreateForm.Meta):
        # Все поля из BaseExerciseCreateForm уже включают assignment_type
        pass  # Ничего не меняем

    def save(self, commit=True):
        exercise = super().save(commit=False)
        teacher = self.initial.get('teacher')
        if teacher:
            exercise.teacher = teacher
            exercise.exercise_type = 'spelling_drag_drop'  # Это тип основного упражнения

        if commit:
            exercise.save()

        # Получаем выбранные слова
        selected_word_ids = self.cleaned_data.get('word_selection', '').split(',')
        selected_word_ids = [id.strip() for id in selected_word_ids if id.strip()]

        words = Word.objects.filter(id__in=selected_word_ids)

        # Создаем пары слов
        pairs = []
        for word in words:
            pairs.append({
                'word_id': word.id,  # Добавляем ID
                'russian': word.russian,
                'english': word.english.lower()
            })

        # Создаем конкретное упражнение SpellingDragDrop
        SpellingDragDropExercise.objects.create(
            exercise=exercise,
            type=self.cleaned_data.get('exercise_subtype', 'spelling'),  # spelling или drag_and_drop
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

        selected_word_ids = self.cleaned_data.get('word_selection', '').split(',')
        selected_word_ids = [id.strip() for id in selected_word_ids if id.strip()]

        words = Word.objects.filter(id__in=selected_word_ids)

        # Сохраняем пары слов
        pairs = []
        english_words = []

        for word in words:
            pairs.append({
                'russian': word.russian,
                'english': word.english.lower()
            })
            english_words.append(word.english.lower())

        grid_size = self.cleaned_data.get('grid_size', 15)

        grid, placed_words = generate_letter_soup(english_words, grid_size=grid_size)

        LetterSoupExercise.objects.create(
            exercise=exercise,
            words=english_words,
            pairs=pairs,  # Сохраняем пары
            grid=grid,
            placed_words=placed_words,
            grid_size=grid_size
        )

        return exercise


class DragDropExerciseForm(BaseExerciseCreateForm):
    """Форма для создания отдельного Drag & Drop упражнения"""

    class Meta(BaseExerciseCreateForm.Meta):
        pass

    def save(self, commit=True):
        exercise = super().save(commit=False)
        teacher = self.initial.get('teacher')
        if teacher:
            exercise.teacher = teacher
            exercise.exercise_type = 'drag_drop'  # Новый тип

        if commit:
            exercise.save()

        # Получаем выбранные слова (аналогично SpellingDragDropExerciseForm)
        selected_word_ids = self.cleaned_data.get('word_selection', '').split(',')
        selected_word_ids = [id.strip() for id in selected_word_ids if id.strip()]

        words = Word.objects.filter(id__in=selected_word_ids)

        # Создаем пары слов
        pairs = []
        for word in words:
            pairs.append({
                'word_id': word.id,
                'russian': word.russian,
                'english': word.english.lower()
            })

        # Создаем конкретное упражнение DragDrop
        DragDropExercise.objects.create(
            exercise=exercise,
            pairs=pairs
        )

        return exercise