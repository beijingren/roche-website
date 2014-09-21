from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class TextAnnotation(models.Model):
    ANALYSIS_CHOICES = (
        ('prosa', 'Prosa'),
        ('poetry', 'Poetry'),
    )

    text = models.TextField()
    comment = models.TextField(blank=True)
    pub_date = models.DateField(auto_now_add=True)

class Annotation(models.Model):
    tei_tag = models.CharField(max_length=1024)
    lemma = models.CharField(max_length=1024)
    ip = models.GenericIPAddressField(null=True)

    def rdf(self):
        print "rdf"

@receiver(pre_save, sender=Annotation)
def sparql_handler(sender, **kwargs):
    print sender
