# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MosesWebserviceApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook_id',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='timezone',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
