from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField


class Distributor(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)


class MovieReviewSite(models.Model):
	models.CharField(max_length=255)


class Movie(models.Model):
	title = models.CharField(max_length=255, unique=True)
	budget = models.FloatField(null=True, blank=True)
	gross = models.FloatField(null=True, blank=True)
	marketing_budget = models.FloatField(null=True, blank=True)
	genre = models.CharField(max_length=255, null=True, blank=True)
	release_date = models.DateField(blank=True, null=True)
	num_distributed_theaters = models.IntegerField(null=True, blank=True)
	distributors = ListField(EmbeddedModelField('Distributor'))
	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

class MovieScore(models.Model):
	site = EmbeddedModelField('MovieReviewSite')
	movie = EmbeddedModelField('Movie')
	score = models.CharField(max_length=255, null=True, blank=True)