# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Corp(models.Model):
    corp_name = models.CharField(max_length=64, unique=True, verbose_name="企业名称")
    corp_id = models.CharField(max_length=128, unique=True, verbose_name="企业ID")

    def __str__(self):
        return self.corp_name

    class Meta:
        verbose_name = "企业"
        verbose_name_plural = "企业"


class Agent(models.Model):
    corp = models.ForeignKey(Corp)
    agent_id = models.IntegerField()
    corp_secret = models.CharField(max_length=128)

    def __str__(self):
        return "%s-%s" % (self.corp.corp_name, self.agent_id)


    class Meta:
        unique_together = ("corp", "agent_id")
        verbose_name_plural = "应用ID"
        verbose_name = "应用ID"


