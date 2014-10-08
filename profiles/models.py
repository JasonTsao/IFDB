from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField
# Create your models here.

from movies.models import Movie, MovieGenre
from .forms import StringListField

class MovieListField(ListField):
    def formfield(self, **kwargs):
        return models.Field.formfield(self, StringListField, **kwargs)


class UserProfile(models.Model):
	name = models.CharField(max_length=255)
	birthday = models.DateField(null=True,blank=True)

	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ["name", "birthday"]

	def __unicode__(self):
		try:
			return str('{0}'.format(self.name)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"


class Profile(models.Model):
	user = models.ForeignKey(UserProfile)
	role = models.CharField(max_length=255, null=True, blank=True)
	name= models.CharField(max_length=255)
	movies = MovieListField(models.ForeignKey(Movie))
	#movies = ListField(models.CharField(max_length=255)) #save Movie.id here
	#movies = ListField(models.ForeignKey(Movie)) #save Movie.id here
	
	#collaborators = ListField(models.CharField(max_length=255))

	class Meta:
		unique_together = ["role", "name"]

	def __unicode__(self):
		try:
			return str('{0} : {1}'.format(self.name, self.role)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"


class CollaborationLink(models.Model):
	profile_1 = models.ForeignKey(Profile, related_name='profile_1')
	profile_2 = models.ForeignKey(Profile, related_name='profile_2')
	#movies = ListField(models.ForeignKey(Movie))
	movies = MovieListField(models.ForeignKey(Movie))

	class Meta:
		unique_together = ["profile_1", "profile_2"]

	def __unicode__(self):
		try:
			return str('{0} : {1} :: {2} : {3}'.format(self.profile_1.name, self.profile_1.role, self.profile_2.name, self.profile_2.role)).decode().encode('utf-8')
		except Exception as e:
			return "Can't be displayed"