# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20150831_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name=b'\xe5\xaf\xbc\xe8\x88\xaa\xe5\x90\x8d\xe7\xa7\xb0')),
                ('index', models.IntegerField(default=999, verbose_name=b'\xe5\xaf\xbc\xe8\x88\xaa\xe7\x9a\x84\xe6\x8e\x92\xe5\xba\x8f')),
            ],
            options={
                'verbose_name': '\u5bfc\u822a',
                'verbose_name_plural': '\u5bfc\u822a',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb', blank=True, to='blog.Index', null=True),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
