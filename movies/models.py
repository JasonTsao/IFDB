from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField


class Distributor(models.Model):
	name = models.CharField(max_length=255, null=True, blank=True)


class MovieReviewSite(models.Model):
	models.CharField(max_length=255)


class MovieGenre(models.Model):
	genre = models.CharField(max_length=255)
	def __unicode__(self):
		try:
			return str('{0}'.format(self.genre)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"


class Movie(models.Model):
	title = models.CharField(max_length=255, unique=True)
	budget = models.FloatField(null=True, blank=True)
	gross = models.FloatField(null=True, blank=True)
	marketing_budget = models.FloatField(null=True, blank=True)
	genres = ListField(EmbeddedModelField('MovieGenre'))
	release_date = models.DateField(blank=True, null=True)
	num_distributed_theaters = models.IntegerField(null=True, blank=True)
	distributors = ListField(EmbeddedModelField('Distributor'))
	run_time = models.TimeField(null=True, blank=True)
	plot = models.CharField(max_length=255, null=True, blank=True)

	year = models.PositiveSmallIntegerField(blank=True, null=True)

	rated = models.CharField(max_length=255, null=True, blank=True)
	language = models.CharField(max_length=255, null=True, blank=True)

	imdb_id = models.CharField(max_length=255, null=True, blank=True)
	imdb_votes = models.CharField(max_length=255, null=True, blank=True)
	imdb_rating = models.FloatField(max_length=255, null=True, blank=True)
	imdb_votes = models.IntegerField(null=True,blank=True)
	metascore = models.IntegerField(null=True,blank=True)

	awards = models.CharField(max_length=255, null=True, blank=True)
	poster_img = models.CharField(max_length=255, null=True, blank=True)
	
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		try:
			return str('{0} : {1}'.format(self.title, self.year)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"


class MovieScore(models.Model):
	site = EmbeddedModelField('MovieReviewSite')
	movie = EmbeddedModelField('Movie')
	score = models.CharField(max_length=255, null=True, blank=True)