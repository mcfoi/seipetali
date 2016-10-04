# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0006_auto_20150403_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(default=0, max_digits=12, decimal_places=2),
            preserve_default=False,
        ),
    ]
