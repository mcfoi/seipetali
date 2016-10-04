# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0005_auto_20150401_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservationservice',
            name='costo',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reservationservice',
            name='fattore_tempo',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
