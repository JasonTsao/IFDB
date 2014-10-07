from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from models import *
from movies.models import *
from social.models import *
from django.http import HttpResponse, HttpResponseRedirect

from datetime import datetime, timedelta
import time
import json
import ast


def removeMovies(request):
	rtn_dict = {"success": False, "msg": ""}

	try:
		movies = Movie.objects.all()

		for movie in movies:
			movie.delete()
		rtn_dict['success'] = True
	except Exception as e:
		print 'Unable to remove movies: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


def getMovies(request):
	rtn_dict = {"success": False, "msg": ""}
	movies_array = []
	movie_ids = []

	movies = Movie.objects.all()

	for movie in movies:
		movie_ids.append(movie.id)
		movie_dict = model_to_dict(movie)
		movie_genres = []

		for movie_genre in movie_dict['genres']:
			movie_genres.append(model_to_dict(movie_genre))

		movie_dict['genres'] = movie_genres
		movie_dict['release_date'] = str(movie_dict['release_date'])
		movies_array.append(movie_dict)

	rtn_dict['movies'] = movies_array
	rtn_dict['movie_ids'] = movie_ids
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")
