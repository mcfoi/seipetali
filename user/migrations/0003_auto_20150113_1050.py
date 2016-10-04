# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django_migration_fixture import fixture
import user


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_phone_number'),
    ]

    operations = [
        migrations.RunPython(**fixture(user, ['initial_data.json'])),

    ]
