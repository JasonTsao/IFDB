from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField
# Create your models here.

from movies.models import Movie, MovieGenre

class Profile(models.Model):
	role = models.CharField(max_length=255, null=True, blank=True)
	name= models.CharField(max_length=255)
	movies = ListField(EmbeddedModelField(Movie))
	collaborators = ListField(EmbeddedModelField('Profile'))
