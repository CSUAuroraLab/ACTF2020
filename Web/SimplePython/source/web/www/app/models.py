# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
# Create your models here.

class PostgreSQLModel(models.Model):
    class Meta:
        abstract = True
        required_db_vendor = 'postgresql'

class Profile(PostgreSQLModel):
    id = models.AutoField(primary_key=True)
    profile = JSONField(blank=True, null=True)