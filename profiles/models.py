from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField
# Create your models here.

from movies.models import Movie, MovieGenre

class Profile(models.Model):
	role = models.CharField(max_length=255, null=True, blank=True)
	name= models.CharField(max_length=255)
	#movies = ListField(models.CharField(max_length=255)) #save Movie.id here
	movies = ListField(models.ForeignKey(Movie)) #save Movie.id here
	collaborators = ListField(models.CharField(max_length=255))


class CollaborationLink(models.Model):
	profile_1 = models.ForeignKey(Profile, related_name='profile_1')
	profile_2 = models.ForeignKey(Profile, related_name='profile_2')
	movies = ListField(models.ForeignKey(Movie))