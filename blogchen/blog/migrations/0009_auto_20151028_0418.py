# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '\u5206\u7c7b', 'verbose_name_plural': '\u5206\u7c7b'},
        ),
        migrations.AlterField(
            model_name='category',
            name='level',
            field=models.IntegerField(default=0, null=True, verbose_name=b'\xe7\xad\x89\xe7\xba\xa7', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='path',
            field=models.CharField(max_length=80, null=True, verbose_name=b'\xe8\xb7\xaf\xe5\xbe\x84', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='pid',
            field=models.ForeignKey(verbose_name=b'\xe7\x88\xb6\xe7\xba\xa7', blank=True, to='blog.Category', null=True),
        ),
    ]
