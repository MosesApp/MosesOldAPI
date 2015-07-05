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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('receipt_image', models.ImageField(upload_to=MosesWebserviceApp.models.get_unique_image_file_path, null=True)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('amount',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('amount', models.FloatField(null=True)),
                ('relation', models.CharField(choices=[('debtor', 'debtor'), ('taker', 'taker')], max_length=10, default='debtor')),
                ('status', models.CharField(choices=[('paid', 'Paid'), ('not paid', 'Not paid')], max_length=10, default='not paid')),
                ('payed_date', models.DateTimeField(null=True, blank=True)),
                ('bill', models.ForeignKey(null=True, related_name='bill', to='MosesWebserviceApp.Bill')),
            ],
            options={
                'ordering': ('member',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('prefix', models.CharField(max_length=3, default='CAD')),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('prefix',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('image', models.ImageField(upload_to=MosesWebserviceApp.models.get_unique_image_file_path, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], max_length=10, default='active')),
            ],
            options={
                'ordering': ('status',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('full_name', models.CharField(max_length=300)),
                ('email', models.CharField(unique=True, max_length=254)),
                ('facebook_id', models.CharField(unique=True, max_length=20)),
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
        migrations.AlterUniqueTogether(
            name='currency',
            unique_together=set([('prefix',)]),
        ),
        migrations.AddField(
            model_name='billuser',
            name='member',
            field=models.ForeignKey(to='MosesWebserviceApp.User', related_name='member'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='currency',
            field=models.ForeignKey(to='MosesWebserviceApp.Currency', related_name='currency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='group',
            field=models.ForeignKey(to='MosesWebserviceApp.Group'),
            preserve_default=True,
        ),
    ]
