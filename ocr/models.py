from django.db import models

# Create your models here.

from django.db import models


class UploadFile(models.Model):
    file = models.FileField(upload_to='files/%Y/%m/%d')
    text = models.TextField()
    tag = models.DateTimeField(auto_now=True)
