# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('block_time', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location_name', models.CharField(max_length=300, blank=True)),
                ('location_lat', models.FloatField(null=True, blank=True)),
                ('location_long', models.FloatField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('logtext', models.CharField(max_length=50, blank=True)),
                ('timestamp', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_text', models.CharField(max_length=300, blank=True)),
                ('post_photo', models.ImageField(upload_to=b'post_images/', blank=True)),
                ('post_time', models.DateTimeField(null=True, blank=True)),
                ('post_sharecount', models.IntegerField(null=True, blank=True)),
                ('post_location', models.ForeignKey(blank=True, to='testshare.Location', null=True)),
            ],
            options={
                'ordering': ['-post_time'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('about_me', models.CharField(max_length=300, blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('last_location', models.CharField(max_length=300, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_maker',
            field=models.ForeignKey(to='testshare.UserProfile'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_sharedfrom',
            field=models.ForeignKey(blank=True, to='testshare.Post', null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='logger',
            field=models.ForeignKey(to='testshare.UserProfile'),
        ),
        migrations.AddField(
            model_name='block',
            name='blocked',
            field=models.ForeignKey(related_name='user_who_got_blocked', to='testshare.UserProfile'),
        ),
        migrations.AddField(
            model_name='block',
            name='blocker',
            field=models.ForeignKey(related_name='user_who_blocked', to='testshare.UserProfile'),
        ),
    ]
