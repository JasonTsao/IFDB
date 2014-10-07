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


def newProfile(request):
	rtn_dict = {"success": False, "msg": ""}

	try:
		movies = []
		movie, created = Movie.objects.get_or_create(title='The Matrix')
		movie.budget = 100000.0
		movie.gross = 4898788920
		movie.genre = 'horror'
		movie.save()


		movies.append(movie)

		print 'movies'
		print movies

		new_profile = Profile()
		new_profile.movies = movies
		new_profile.save()
		rtn_dict['success'] = True
		rtn_dict['profile'] = new_profile
	except Exception as e:
		print 'Unable to save profile: {0}'.format(e)
		rtn_dict['msg'] = 'Unable to save profile: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


def removeProfiles(request):
	rtn_dict = {"success": False, "msg": ""}

	try:
		profiles = Profile.objects.all()

		for profile in profiles:
			profile.delete()
		rtn_dict['success'] = True
	except Exception as e:
		print 'Unable to remove profiles: {0}'.format(e)

	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


def getProfiles(request):
	rtn_dict = {"success": False, "msg": ""}
	profiles_array = []

	profiles = Profile.objects.all()

	for profile in profiles:
		profile_dict = {}
		movies_array = []
		profile_dict = model_to_dict(profile)


		for movie_id in profile.movies:
			movie_genres = []

			movie = Movie.objects.get(id=movie_id)
			movie_dict = model_to_dict(movie)
			for movie_genre in movie_dict['genres']:
				movie_genres.append(model_to_dict(movie_genre))

			movie_dict['genres'] = movie_genres
			movies_array.append(movie_dict)

		profile_dict['movies'] = movies_array
		profiles_array.append(profile_dict)

	rtn_dict['profiles'] = profiles_array

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")


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
		movies_array.append(movie_dict)

	rtn_dict['movies'] = movies_array
	rtn_dict['movie_ids'] = movie_ids
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")

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