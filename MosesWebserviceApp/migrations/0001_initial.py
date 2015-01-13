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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('receipt_image', models.ImageField(null=True, upload_to=MosesWebserviceApp.models.get_unique_image_file_path)),
                ('amount', models.IntegerField()),
                ('currency', models.CharField(max_length=3, default='BR', choices=[('CA', 'CA'), ('US', 'US'), ('BR', 'BR')])),
                ('deadline', models.DateTimeField()),
            ],
            options={
                'ordering': ('amount',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('relation', models.CharField(max_length=10, default='debtor', choices=[('debtor', 'debtor'), ('taker', 'taker')])),
                ('status', models.CharField(max_length=10, default='not paid', choices=[('paid', 'Paid'), ('not paid', 'Not paid')])),
                ('bill', models.ForeignKey(to='MosesWebserviceApp.Bill', related_name='bill', null=True)),
            ],
            options={
                'ordering': ('member',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('image', models.ImageField(null=True, upload_to=MosesWebserviceApp.models.get_unique_image_file_path)),
                ('status', models.CharField(max_length=10, default='active', choices=[('active', 'Active'), ('inactive', 'Inactive')])),
            ],
            options={
                'ordering': ('status',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
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
            model_name='billuser',
            name='member',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='group',
            field=models.ForeignKey(to='MosesWebserviceApp.Group'),
            preserve_default=True,
        ),
    ]
