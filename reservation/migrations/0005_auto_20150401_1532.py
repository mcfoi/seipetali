# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_auto_20150401_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='servizi_opzional',
        ),
        migrations.AddField(
            model_name='reservationservice',
            name='reservation',
            field=models.ForeignKey(related_name='servizi_opzional', default=1, to='reservation.Reservation'),
            preserve_default=False,
        ),
    ]
