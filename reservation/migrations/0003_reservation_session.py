# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('reservation', '0002_remove_reservation_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sessions.Session', null=True),
            preserve_default=True,
        ),
    ]
