# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        (b'annotate', b'0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name=b'textannotation',
            name=b'text_type',
        ),
    ]
