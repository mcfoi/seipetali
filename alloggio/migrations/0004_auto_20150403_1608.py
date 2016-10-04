# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alloggio', '0003_auto_20150316_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alloggio',
            name='descrizione_breve',
            field=models.TextField(max_length=100, verbose_name=b'Descrizione alloggio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='descrizione_breve_en',
            field=models.TextField(max_length=100, null=True, verbose_name=b'Descrizione alloggio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='descrizione_breve_it',
            field=models.TextField(max_length=100, null=True, verbose_name=b'Descrizione alloggio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='descrizione_lunga',
            field=models.TextField(max_length=1000, verbose_name=b'Descrizione dettagliata'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='descrizione_lunga_en',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Descrizione dettagliata'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='descrizione_lunga_it',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Descrizione dettagliata'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='regole_casa',
            field=models.TextField(max_length=1000, verbose_name=b'Regole della casa e informazioni varie'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='regole_casa_en',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Regole della casa e informazioni varie'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='alloggio',
            name='regole_casa_it',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Regole della casa e informazioni varie'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='servizioopzionale',
            name='costo',
            field=models.DecimalField(max_digits=12, decimal_places=2),
            preserve_default=True,
        ),
    ]
