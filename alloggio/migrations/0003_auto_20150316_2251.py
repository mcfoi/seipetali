# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alloggio', '0002_auto_20150113_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alloggio',
            name='letti',
            field=models.ManyToManyField(to='alloggio.Letto', null=True, through='alloggio.LettoRelation', blank=True),
            preserve_default=True,
        ),
    ]
