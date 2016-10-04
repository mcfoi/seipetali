# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
import alloggio


class Migration(migrations.Migration):

    dependencies = [
        ('alloggio', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(**fixture(alloggio, ['initial_data.json'])),

    ]
