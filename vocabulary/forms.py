from django import forms
from .models import Word, Topic
from users.models import User


class WordCreateForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(role='student'),
        label="Ученик",
        required=True
    )

    class Meta:
        model = Word
        fields = ['russian', 'english', 'topic']
        widgets = {
            'russian': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: собака'
            }),
            'english': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: dog'
            }),
            'topic': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'russian': 'Русское слово',
            'english': 'Английский перевод',
            'topic': 'Тема'
        }