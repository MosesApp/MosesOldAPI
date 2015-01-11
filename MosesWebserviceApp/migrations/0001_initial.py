# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import MosesWebserviceApp.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('receipt_image', models.ImageField(upload_to=MosesWebserviceApp.models.get_unique_image_file_path, null=True)),
                ('amount', models.IntegerField()),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(max_length=10, choices=[('paid', 'Paid'), ('not paid', 'Not paid')], default='not paid')),
            ],
            options={
                'ordering': ('amount',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to=MosesWebserviceApp.models.get_unique_image_file_path, null=True)),
                ('status', models.CharField(max_length=10, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active')),
            ],
            options={
                'ordering': ('status',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('administrator', models.BooleanField(default=False)),
                ('group', models.ForeignKey(to='MosesWebserviceApp.Group', related_name='group')),
            ],
            options={
                'ordering': ('user',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('full_name', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=254, unique=True)),
                ('facebook_id', models.CharField(max_length=20, unique=True)),
                ('locale', models.CharField(max_length=5)),
                ('timezone', models.IntegerField()),
            ],
            options={
                'ordering': ('facebook_id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='groupuser',
            name='user',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='user'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='groupuser',
            unique_together=set([('user', 'group')]),
        ),
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='creator'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('creator', 'name')]),
        ),
        migrations.AddField(
            model_name='bill',
            name='debtor',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='debtor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='group',
            field=models.ForeignKey(to='MosesWebserviceApp.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='receiver',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='receiver'),
            preserve_default=True,
        ),
    ]
