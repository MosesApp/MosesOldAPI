# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('amount', models.IntegerField(max_length=10)),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(default='not paid', choices=[('paid', 'Paid'), ('not paid', 'Not paid')], max_length=10)),
            ],
            options={
                'ordering': ('amount',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=300)),
                ('status', models.CharField(default='active', choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10)),
            ],
            options={
                'ordering': ('status',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('group', models.ForeignKey(to='MosesWebserviceApp.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=50)),
                ('full_name', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=254)),
                ('facebook_id', models.IntegerField(max_length=20)),
                ('locale', models.CharField(max_length=5)),
                ('timezone', models.IntegerField(max_length=32)),
            ],
            options={
                'ordering': ('facebook_id',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='groupuser',
            name='user',
            field=models.ForeignKey(to='MosesWebserviceApp.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(to='MosesWebserviceApp.User'),
            preserve_default=True,
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
