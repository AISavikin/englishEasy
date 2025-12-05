from django import forms
from .models import Exercise
from users.models import User
import json


class ExerciseCreateForm(forms.ModelForm):
    # Кастомное поле для JSON данных
    exercise_data_raw = forms.CharField(
        label='Данные упражнения (JSON)',
        widget=forms.Textarea(attrs={
            'rows': 10,
            'placeholder': 'Введите JSON структуру упражнения...\nПример для spelling:\n{\n  "words": ["apple", "banana", "cherry"],\n  "instructions": "Напишите слова правильно"\n}'
        }),
        required=True
    )

    class Meta:
        model = Exercise
        fields = [
            'title', 'description', 'student',
            'assignment_type', 'exercise_type',
            'max_attempts', 'due_date', 'max_score'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'student': forms.Select(attrs={'class': 'form-select'}),
            'assignment_type': forms.Select(attrs={'class': 'form-select'}),
            'exercise_type': forms.Select(attrs={'class': 'form-select'}),
            'max_attempts': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
            'max_score': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)

        if teacher:
            # Ограничиваем выбор учеников только теми, кто связан с этим учителем
            self.fields['student'].queryset = User.objects.filter(role='student')

        # Устанавливаем начальные значения
        if not self.instance.pk:
            self.initial['exercise_data_raw'] = '{\n  "words": [],\n  "instructions": ""\n}'
        else:
            self.initial['exercise_data_raw'] = json.dumps(
                self.instance.exercise_data,
                indent=2,
                ensure_ascii=False
            )

    def clean_exercise_data_raw(self):
        data = self.cleaned_data['exercise_data_raw']
        try:
            parsed_data = json.loads(data)
            return parsed_data
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'Неверный JSON формат: {e}')

    def save(self, commit=True):
        exercise = super().save(commit=False)
        exercise.exercise_data = self.cleaned_data['exercise_data_raw']

        if commit:
            exercise.save()

        return exercise