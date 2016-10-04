# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alloggio', '0004_auto_20150403_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='alloggio',
            name='prezzo_week',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
