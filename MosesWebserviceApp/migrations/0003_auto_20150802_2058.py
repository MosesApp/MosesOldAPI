# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MosesWebserviceApp', '0002_auto_20150802_2048'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expense',
            options={'ordering': ('user',)},
        ),
        migrations.RemoveField(
            model_name='expense',
            name='member',
        ),
        migrations.AddField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='expense_user', default=-3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='groupuser',
            name='user',
            field=models.ForeignKey(related_name='group_user', to='MosesWebserviceApp.User'),
        ),
    ]
