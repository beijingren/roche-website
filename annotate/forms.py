from django import forms
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render_to_response

from .models import TextAnnotation


class UIMAWizard(SessionWizardView):
    template_name = 'uima/advanced.html'
    uima_result = None

    def done(self, form_list, **kwargs):
        return render_to_response('done.html', {
            'form_data': [form.cleaned_data for form in form_list],
        })

    def get_context_data(self, form, **kwargs):
        context = super(UIMAWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == '1':
            context.update({'uima_result': self.uima_result })
        return context

    def process_step(self, form):
        if self.steps.current == '0':
            text_type = form.data['0-text_type']
            text = form.data['0-text']
            self.uima_result = text
        return self.get_form_step_data(form)

class UIMAWizardForm(forms.Form):
    ANALYSIS_CHOICES = (
        ('prosa', 'Prosa'),
        ('poetry', 'Poetry'),
    )
    text_type = forms.ChoiceField(choices=ANALYSIS_CHOICES)
    text = forms.CharField(widget=forms.Textarea)

class UIMAWizardForm2(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)

class TextAnnotationForm(forms.ModelForm):
    class Meta:
        model = TextAnnotation
        widgets = {'text': forms.Textarea(attrs={'cols': 100, 'rows': 6})} 

