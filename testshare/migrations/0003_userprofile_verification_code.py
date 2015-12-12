# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testshare', '0002_userprofile_pw'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verification_code',
            field=models.CharField(default=b'123456', max_length=128),
        ),
    ]
