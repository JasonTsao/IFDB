from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField


class IMDBMedia(models.Model):
	imdb_id = models.CharField(max_length=255, null=True, blank=True)
	title = models.CharField(max_length=255, null=True, blank=True)
	director = models.CharField(max_length=255, null=True, blank=True)
	writer = models.CharField(max_length=255, null=True, blank=True)
	year = models.PositiveSmallIntegerField(blank=True, null=True)
	imdb_type = models.CharField(max_length=255, null=True, blank=True)
	rated = models.CharField(max_length=255, null=True, blank=True)
	language = models.CharField(max_length=255, null=True, blank=True)
	imdb_votes = models.CharField(max_length=255, null=True, blank=True)
	country = models.CharField(max_length=255, null=True, blank=True)
	actors = ListField(null=True, blank=True)
	released = models.DateField(null=True,blank=True)
	genre = ListField(null=True,blank=True)
	awards = models.CharField(max_length=255, null=True, blank=True)
	run_time = models.CharField(max_length=255, null=True, blank=True)
	imdb_rating = models.FloatField(max_length=255, null=True, blank=True)
	imdb_votes = models.IntegerField(null=True,blank=True)
	metascore = models.IntegerField(null=True,blank=True)
	poster_img = models.CharField(max_length=255, null=True, blank=True)
