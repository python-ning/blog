# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20151028_0418'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ad',
        ),
    ]
