from __future__ import unicode_literals

from django.db import models
from decimal import *

class Config(models.Model):
    corpus_size = models.IntegerField(primary_key=True, blank=True)
    class Meta:
        db_table = 'config'

class Negative(models.Model):
    bigram = models.TextField(primary_key=True, unique=True, blank=True, db_index=True)
    freq = models.IntegerField()

    def get_prob(self):
        return Decimal(float(self.freq) / Negative.objects.count())

    class Meta:
        db_table = 'negative'

class Positive(models.Model):
    bigram = models.TextField(primary_key=True, unique=True, blank=True, db_index=True)
    freq = models.IntegerField()

    def get_prob(self):
        return Decimal(float(self.freq) / Positive.objects.count())
    
    class Meta:
        db_table = 'positive'

class TestTweets(models.Model):
    username = models.TextField(blank=False)
    screenname = models.TextField(blank=False)
    tweet = models.TextField(blank=False)
    pub_time = models.DateTimeField()
    

