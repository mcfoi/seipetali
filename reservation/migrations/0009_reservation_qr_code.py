# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataqrcode', '__first__'),
        ('reservation', '0008_payment_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='qr_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='dataqrcode.DataQRCode', null=True),
            preserve_default=True,
        ),
    ]
