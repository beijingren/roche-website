import json
import uuid

from django import forms
from django.contrib.formtools.wizard.views import SessionWizardView
from django.shortcuts import render_to_response

from pika import BasicProperties
from pika import BlockingConnection
from pika import ConnectionParameters

from roche.settings import RABBITMQ_SERVER

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

            # Prepare message
            uima_response = {}
            uima_response['response'] = None
            uima_corr_id = str(uuid.uuid4())
            uima_body = json.dumps({'text': text, })

            def uima_on_response(channel, method, props, body):
                if uima_corr_id == props.correlation_id:
                     uima_response['response'] = body

            # Call UIMA
            uima_connection = BlockingConnection(ConnectionParameters(host=RABBITMQ_SERVER))
            uima_channel = uima_connection.channel()
            uima_result = uima_channel.queue_declare(exclusive=True)
            uima_callback_queue = uima_result.method.queue
            uima_channel.basic_consume(uima_on_response, no_ack=True, queue=uima_callback_queue)
            uima_channel.basic_publish(exchange='',
                                       routing_key='uima_plain_worker',
                                       properties=BasicProperties(reply_to=uima_callback_queue,
                                                                  content_type='application/json',
                                                                  correlation_id=uima_corr_id, ),
                                       body=uima_body)

            while uima_response['response'] is None:
                uima_connection.process_data_events()

            self.uima_result = uima_response['response']

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

