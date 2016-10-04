# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20150612_0845'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=300, null=True, verbose_name='Indirizzo', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='citta',
            field=models.CharField(max_length=100, null=True, verbose_name='Citt\xe1', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='postal_code',
            field=models.CharField(max_length=100, null=True, verbose_name='Codice postale', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='provincia',
            field=models.CharField(max_length=100, null=True, verbose_name='Provincia', blank=True),
            preserve_default=True,
        ),
    ]
