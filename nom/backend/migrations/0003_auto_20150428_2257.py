# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20150406_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='orgs',
            field=models.ManyToManyField(related_name='admins', to='backend.Company'),
        ),
        migrations.AlterField(
            model_name='foodevent',
            name='attendees',
            field=models.ManyToManyField(related_name='attended_events', to='backend.User'),
        ),
        migrations.AlterField(
            model_name='foodevent',
            name='company',
            field=models.ForeignKey(related_name='events', to='backend.Company'),
        ),
    ]
