
from django import forms

from .models import TextAnnotation


class TextAnnotationForm(forms.ModelForm):
    class Meta:
        model = TextAnnotation
