# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-17 18:45
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_auto_20170731_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballotmeasurecontest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time of creation.'),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontest',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='A key-value store for storing arbitrary information not covered elsewhere.'),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time of the last update.'),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontestidentifier',
            name='identifier',
            field=models.CharField(help_text='A unique identifier developed by an upstream or third party source.', max_length=300),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontestidentifier',
            name='scheme',
            field=models.CharField(help_text='The name of the service that created the identifier.', max_length=300),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontestsource',
            name='note',
            field=models.CharField(blank=True, help_text='A short, optional note related to an object.', max_length=300),
        ),
        migrations.AlterField(
            model_name='ballotmeasurecontestsource',
            name='url',
            field=models.URLField(help_text='A hyperlink related to an object.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time of creation.'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='A key-value store for storing arbitrary information not covered elsewhere.'),
        ),
        migrations.AlterField(
            model_name='candidacy',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time of the last update.'),
        ),
        migrations.AlterField(
            model_name='candidacysource',
            name='note',
            field=models.CharField(blank=True, help_text='A short, optional note related to an object.', max_length=300),
        ),
        migrations.AlterField(
            model_name='candidacysource',
            name='url',
            field=models.URLField(help_text='A hyperlink related to an object.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='candidatecontest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time of creation.'),
        ),
        migrations.AlterField(
            model_name='candidatecontest',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='A key-value store for storing arbitrary information not covered elsewhere.'),
        ),
        migrations.AlterField(
            model_name='candidatecontest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time of the last update.'),
        ),
        migrations.AlterField(
            model_name='candidatecontestidentifier',
            name='identifier',
            field=models.CharField(help_text='A unique identifier developed by an upstream or third party source.', max_length=300),
        ),
        migrations.AlterField(
            model_name='candidatecontestidentifier',
            name='scheme',
            field=models.CharField(help_text='The name of the service that created the identifier.', max_length=300),
        ),
        migrations.AlterField(
            model_name='candidatecontestsource',
            name='note',
            field=models.CharField(blank=True, help_text='A short, optional note related to an object.', max_length=300),
        ),
        migrations.AlterField(
            model_name='candidatecontestsource',
            name='url',
            field=models.URLField(help_text='A hyperlink related to an object.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='election',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time of creation.'),
        ),
        migrations.AlterField(
            model_name='election',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='A key-value store for storing arbitrary information not covered elsewhere.'),
        ),
        migrations.AlterField(
            model_name='election',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time of the last update.'),
        ),
        migrations.AlterField(
            model_name='electionidentifier',
            name='election',
            field=models.ForeignKey(help_text='Reference to the Election identified by this alternative identifier.', on_delete=django.db.models.deletion.CASCADE, related_name='identifiers', to='elections.Election'),
        ),
        migrations.AlterField(
            model_name='electionidentifier',
            name='identifier',
            field=models.CharField(help_text='A unique identifier developed by an upstream or third party source.', max_length=300),
        ),
        migrations.AlterField(
            model_name='electionidentifier',
            name='scheme',
            field=models.CharField(help_text='The name of the service that created the identifier.', max_length=300),
        ),
        migrations.AlterField(
            model_name='electionsource',
            name='event',
            field=models.ForeignKey(help_text='Reference to the Election this source verifies.', on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='elections.Election'),
        ),
        migrations.AlterField(
            model_name='electionsource',
            name='note',
            field=models.CharField(blank=True, help_text='A short, optional note related to an object.', max_length=300),
        ),
        migrations.AlterField(
            model_name='electionsource',
            name='url',
            field=models.URLField(help_text='A hyperlink related to an object.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='partycontest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time of creation.'),
        ),
        migrations.AlterField(
            model_name='partycontest',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='A key-value store for storing arbitrary information not covered elsewhere.'),
        ),
        migrations.AlterField(
            model_name='partycontest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time of the last update.'),
        ),
        migrations.AlterField(
            model_name='partycontestidentifier',
            name='identifier',
            field=models.CharField(help_text='A unique identifier developed by an upstream or third party source.', max_length=300),
        ),
        migrations.AlterField(
            model_name='partycontestidentifier',
            name='scheme',
            field=models.CharField(help_text='The name of the service that created the identifier.', max_length=300),
        ),
        migrations.AlterField(
            model_name='partycontestsource',
            name='note',
            field=models.CharField(blank=True, help_text='A short, optional note related to an object.', max_length=300),
        ),
        migrations.AlterField(
            model_name='partycontestsource',
            name='url',
            field=models.URLField(help_text='A hyperlink related to an object.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='retentioncontest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='The date and time of creation.'),
        ),
        migrations.AlterField(
            model_name='retentioncontest',
            name='extras',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, help_text='A key-value store for storing arbitrary information not covered elsewhere.'),
        ),
        migrations.AlterField(
            model_name='retentioncontest',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='The date and time of the last update.'),
        ),
        migrations.AlterField(
            model_name='retentioncontestidentifier',
            name='identifier',
            field=models.CharField(help_text='A unique identifier developed by an upstream or third party source.', max_length=300),
        ),
        migrations.AlterField(
            model_name='retentioncontestidentifier',
            name='scheme',
            field=models.CharField(help_text='The name of the service that created the identifier.', max_length=300),
        ),
        migrations.AlterField(
            model_name='retentioncontestsource',
            name='note',
            field=models.CharField(blank=True, help_text='A short, optional note related to an object.', max_length=300),
        ),
        migrations.AlterField(
            model_name='retentioncontestsource',
            name='url',
            field=models.URLField(help_text='A hyperlink related to an object.', max_length=2000),
        ),
    ]
