from django.db import models


class TextAnnotation(models.Model):
    ANALYSIS_CHOICES = (
        ('prosa', 'Prosa'),
        ('poetry', 'Poetry'),
    )

    text = models.TextField()
    #text_type = models.CharField(max_length=128, choices=ANALYSIS_CHOICES)
