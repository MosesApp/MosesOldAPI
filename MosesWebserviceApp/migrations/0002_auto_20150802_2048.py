# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MosesWebserviceApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('amount', models.FloatField(null=True)),
                ('relation', models.CharField(default='debtor', choices=[('debtor', 'debtor'), ('taker', 'taker')], max_length=10)),
                ('status', models.CharField(default='not paid', choices=[('paid', 'Paid'), ('not paid', 'Not paid')], max_length=10)),
                ('payed_date', models.DateTimeField(blank=True, null=True)),
                ('bill', models.ForeignKey(to='MosesWebserviceApp.Bill', null=True, related_name='bill')),
                ('member', models.ForeignKey(to='MosesWebserviceApp.User', related_name='member')),
            ],
            options={
                'ordering': ('member',),
            },
        ),
        migrations.RemoveField(
            model_name='userexpense',
            name='bill',
        ),
        migrations.RemoveField(
            model_name='userexpense',
            name='member',
        ),
        migrations.DeleteModel(
            name='UserExpense',
        ),
    ]
