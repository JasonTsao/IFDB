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

	def __unicode__(self):
		try:
			return str('{0} : {1}'.format(self.name, self.role)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"


class CollaborationLink(models.Model):
	profile_1 = models.ForeignKey(Profile, related_name='profile_1')
	profile_2 = models.ForeignKey(Profile, related_name='profile_2')
	movies = ListField(models.ForeignKey(Movie))

	class Meta:
		unique_together = ["profile_1", "profile_2"]

	def __unicode__(self):
		try:
			return str('{0} : {1}'.format(self.profile_1.name, self.profile_2.name)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"