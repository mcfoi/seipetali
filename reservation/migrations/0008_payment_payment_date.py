# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_payment_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 15, 13, 50, 17, 280749, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
