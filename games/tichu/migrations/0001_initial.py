# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import tichu.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='StateType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('long_description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TichuGameState',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('notes', models.TextField(blank=True)),
                ('hands', tichu.models.HandField()),
                ('last_played', tichu.models.JSONField()),
                ('tichu', tichu.models.JSONField()),
                ('grand_tichu', tichu.models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AlternativeTichuGameState',
            fields=[
                ('tichugamestate_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='tichu.TichuGameState', serialize=False, primary_key=True)),
                ('original', models.ForeignKey(to='tichu.AlternativeTichuGameState')),
            ],
            options={
                'abstract': False,
            },
            bases=('tichu.tichugamestate',),
        ),
        migrations.AddField(
            model_name='tichugamestate',
            name='game',
            field=models.ForeignKey(blank=True, to='tichu.Game'),
        ),
        migrations.AddField(
            model_name='tichugamestate',
            name='state_type',
            field=models.ForeignKey(to='tichu.StateType'),
        ),
    ]
