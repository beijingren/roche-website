from django import forms

from .models import TextAnnotation


class TextAnnotationForm(forms.ModelForm):
    class Meta:
        model = TextAnnotation
        widgets = {'text': forms.Textarea(attrs={'cols': 100, 'rows': 6})} 
