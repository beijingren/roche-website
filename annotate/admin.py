from django.contrib import admin

from .models import Annotation


class AnnotationAdmin(admin.ModelAdmin):
    list_display = ['lemma', 'tei_tag', 'ip']

admin.site.register(Annotation, AnnotationAdmin)
