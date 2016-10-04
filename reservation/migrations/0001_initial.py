# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedule', '__first__'),
        ('alloggio', '0003_auto_20150316_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('method', models.CharField(default=b'paypal', max_length=10, choices=[(b'bonifico', 'Bonifico Bancario'), (b'vaglia', 'Vaglia Postale'), (b'paypal', 'Paypal')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('numero_ospiti', models.IntegerField()),
                ('status', models.CharField(max_length=10, choices=[(b'pending', 'Pending'), (b'reserved', 'Reserved')])),
                ('total', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('alloggio', models.ForeignKey(to='alloggio.Alloggio')),
                ('event', models.ForeignKey(to='schedule.Event')),
                ('servizi_opzional', models.ManyToManyField(to='alloggio.ServizioOpzionale', null=True, blank=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='sessions.Session', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='payment',
            name='reservation',
            field=models.ForeignKey(to='reservation.Reservation'),
            preserve_default=True,
        ),
    ]
