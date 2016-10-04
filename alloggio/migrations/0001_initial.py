# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '__first__'),
        ('seipetali_configuration', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('address', '__first__'),
        ('photologue', '0006_auto_20141028_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alloggio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False)),
                ('tipo', models.CharField(default=b'appartamento', max_length=16, choices=[(b'appartamento', b'Appartamento'), (b'singola', b'Casa Singola'), (b'residence', b'Residence')])),
                ('descrizione_breve', models.TextField(max_length=100)),
                ('descrizione_breve_it', models.TextField(max_length=100, null=True)),
                ('descrizione_breve_en', models.TextField(max_length=100, null=True)),
                ('descrizione_lunga', models.TextField(max_length=1000)),
                ('descrizione_lunga_it', models.TextField(max_length=1000, null=True)),
                ('descrizione_lunga_en', models.TextField(max_length=1000, null=True)),
                ('regole_casa', models.TextField(max_length=1000)),
                ('regole_casa_it', models.TextField(max_length=1000, null=True)),
                ('regole_casa_en', models.TextField(max_length=1000, null=True)),
                ('postiletto', models.PositiveIntegerField()),
                ('descrizione_letti', models.CharField(max_length=100)),
                ('descrizione_letti_it', models.CharField(max_length=100, null=True)),
                ('descrizione_letti_en', models.CharField(max_length=100, null=True)),
                ('prezzo', models.FloatField(default=0.0)),
                ('piano', models.IntegerField(default=0)),
                ('ascensore', models.BooleanField(default=False)),
                ('accesso_disabili', models.BooleanField(default=False)),
                ('animali_ammessi', models.BooleanField(default=False)),
                ('posti_auto', models.IntegerField(default=0)),
                ('address', models.ForeignKey(to='address.Address')),
                ('calendar', models.ForeignKey(to='schedule.Calendar', blank=True)),
                ('gallery', models.ForeignKey(to='photologue.Gallery')),
                ('iva', models.ForeignKey(blank=True, to='seipetali_configuration.Iva', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Letto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('postiletto', models.PositiveIntegerField()),
                ('descrizione', models.CharField(max_length=64)),
                ('descrizione_it', models.CharField(max_length=64, null=True)),
                ('descrizione_en', models.CharField(max_length=64, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LettoRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.PositiveIntegerField(default=1)),
                ('note', models.TextField(max_length=100)),
                ('alloggio', models.ForeignKey(to='alloggio.Alloggio')),
                ('letto', models.ForeignKey(to='alloggio.Letto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServizioBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=64)),
                ('nome_it', models.CharField(max_length=64, null=True)),
                ('nome_en', models.CharField(max_length=64, null=True)),
                ('descrizione', models.CharField(max_length=500)),
                ('descrizione_it', models.CharField(max_length=500, null=True)),
                ('descrizione_en', models.CharField(max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'servizio base',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ServizioOpzionale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('nome', models.CharField(max_length=64)),
                ('nome_it', models.CharField(max_length=64, null=True)),
                ('nome_en', models.CharField(max_length=64, null=True)),
                ('descrizione', models.CharField(max_length=500)),
                ('descrizione_it', models.CharField(max_length=500, null=True)),
                ('descrizione_en', models.CharField(max_length=500, null=True)),
                ('costo', models.FloatField()),
                ('fattore_tempo', models.IntegerField(default=1)),
                ('iva', models.ForeignKey(to='seipetali_configuration.Iva', null=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'servizio Opzionale',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='alloggio',
            name='letti',
            field=models.ManyToManyField(to='alloggio.Letto', through='alloggio.LettoRelation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alloggio',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alloggio',
            name='servizi_base',
            field=models.ManyToManyField(to='alloggio.ServizioBase', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alloggio',
            name='servizi_opzionali',
            field=models.ManyToManyField(to='alloggio.ServizioOpzionale', null=True, blank=True),
            preserve_default=True,
        ),
    ]
