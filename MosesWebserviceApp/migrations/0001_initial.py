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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('receipt_image', models.ImageField(null=True, upload_to=MosesWebserviceApp.models.get_unique_image_file_path)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('amount',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(null=True)),
                ('relation', models.CharField(max_length=10, default='debtor', choices=[('debtor', 'debtor'), ('taker', 'taker')])),
                ('status', models.CharField(max_length=10, default='not paid', choices=[('paid', 'Paid'), ('not paid', 'Not paid')])),
                ('payed_date', models.DateTimeField(null=True, blank=True)),
                ('bill', models.ForeignKey(null=True, to='MosesWebserviceApp.Bill', related_name='bill')),
            ],
            options={
                'ordering': ('member',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('administrator', models.BooleanField(default=False)),
                ('group', models.ForeignKey(related_name='group', to='MosesWebserviceApp.Group')),
            ],
            options={
                'ordering': ('user',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
            field=models.ForeignKey(related_name='user', to='MosesWebserviceApp.User'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='groupuser',
            unique_together=set([('user', 'group')]),
        ),
        migrations.AddField(
            model_name='group',
            name='creator',
            field=models.ForeignKey(related_name='creator', to='MosesWebserviceApp.User'),
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
            model_name='UserExpense',
            name='member',
            field=models.ForeignKey(related_name='member', to='MosesWebserviceApp.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='currency',
            field=models.ForeignKey(related_name='currency', to='MosesWebserviceApp.Currency'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='group',
            field=models.ForeignKey(to='MosesWebserviceApp.Group'),
            preserve_default=True,
        ),
    ]
