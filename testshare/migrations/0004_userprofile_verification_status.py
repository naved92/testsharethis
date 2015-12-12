# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testshare', '0003_userprofile_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verification_status',
            field=models.CharField(default=b'p', max_length=2, choices=[(b'a', b'active'), (b'd', b'deactive'), (b'o', b'other'), (b'p', b'pending'), (b's', b'suspended')]),
        ),
    ]
