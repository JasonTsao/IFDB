from django.db import models

# Create your models here.
class BOMMovieData(models.Model):
	movie_name = models.CharField(max_length=255)
	movie_data = models.TextField()