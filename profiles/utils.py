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
	profiles_movies = []
	profiles_ids = []
	profiles_array = []

	profiles = Profile.objects.all()

	for profile in profiles:
		profiles_ids.append(profile.id)
		profiles_array.append(model_to_dict(profile))
		profiles_movies.append(profile.movies)

	rtn_dict['profile_movies'] = profiles_movies
	rtn_dict['profile_ids'] = profiles_ids
	rtn_dict['profiles'] = profiles_array
	return HttpResponse(json.dumps(rtn_dict), content_type="application/json")


def getMovies(request):
	rtn_dict = {"success": False, "msg": ""}
	movies = []

	try:
		movie_objs = Movie.objects.all()

		for movie in movie_objs:
			movies.append(model_to_dict(movie))
		rtn_dict['success'] = True
	except Exception as e:
		print 'Unable to retrieve movies: {0}'.format(e)
		rtn_dict['msg'] = 'Unable to retrieve movies: {0}'.format(e)

	rtn_dict['movies'] = movies

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