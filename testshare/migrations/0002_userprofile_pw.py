# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testshare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pw',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
