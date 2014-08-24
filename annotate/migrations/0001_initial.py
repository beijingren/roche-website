# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'TextAnnotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'text', models.TextField()),
                (b'text_type', models.CharField(max_length=128, choices=[(b'prosa', b'Prosa'), (b'poetry', b'Poetry')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
