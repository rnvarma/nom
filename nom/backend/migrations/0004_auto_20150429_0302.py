# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20150428_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodevent',
            name='date',
            field=models.DateField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='foodevent',
            name='endTime',
            field=models.TimeField(default=None, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='foodevent',
            name='startTime',
            field=models.TimeField(default=None, null=True, blank=True),
        ),
    ]
