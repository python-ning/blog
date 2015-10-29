# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20151024_1103'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb\xe5\x90\x8d')),
                ('desc', models.CharField(max_length=50, null=True, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('path', models.CharField(max_length=80, verbose_name=b'\xe8\xb7\xaf\xe5\xbe\x84')),
                ('level', models.IntegerField(default=0, verbose_name=b'\xe7\xad\x89\xe7\xba\xa7')),
                ('start', models.SmallIntegerField(default=0, verbose_name=b'\xe6\x98\xaf\xe5\x90\xa6\xe5\x90\xaf\xe5\x8a\xa8', choices=[(0, b'\xe5\x90\xaf\xe5\x8a\xa8'), (1, b'\xe4\xb8\x8d\xe5\x90\xaf\xe5\x8a\xa8')])),
                ('pid', models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe7\xba\xa7', to='blog.category')),
            ],
        ),
    ]
