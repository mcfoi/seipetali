# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alloggio', '0003_auto_20150316_2251'),
        ('reservation', '0003_reservation_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('iva', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('original_service', models.ForeignKey(blank=True, to='alloggio.ServizioOpzionale', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='session',
        ),
        migrations.AddField(
            model_name='reservation',
            name='iva',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reservation',
            name='price',
            field=models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='servizi_opzional',
            field=models.ManyToManyField(to='reservation.ReservationService', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(default=b'pending', max_length=10, choices=[(b'pending', 'Pending'), (b'reserved', 'Reserved')]),
            preserve_default=True,
        ),
    ]
