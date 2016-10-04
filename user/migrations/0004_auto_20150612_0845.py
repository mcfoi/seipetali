# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20150113_1050'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='locatario',
            field=models.BooleanField(default=True, editable=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='locatore',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
