import xml.etree.ElementTree as ET
import datetime
import json
import urllib2
import oauth2 as oauth
import urllib

from lxml import html
from io import StringIO
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect

from profiles.models import Profile
from movies.models import Movie, MovieGenre

OMDB_API = 'http://www.omdbapi.com/?'


def searchOMDB(url):
	try:
		conn = urllib2.urlopen(url)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()
	except urllib2.HTTPError as error:
		print 'Error getting imdb data: {0}'.format(error)
	return response


def saveUserProfile(movie_id, name, role):
	# Saving Writer information
	try:
		profile, created = Profile.objects.get_or_create(name=name, role=role)

		if created:
			movies_array = profile.movies
			if not movies_array:
				movies_array = []

			movies_array.append(movie_id)
			profile.movies = movies_array
		else:
			movies_array = profile.movies
			if not movie_id in movies_array:
				movies_array.append(movie_id)
				profile.movies = movies_array

		profile.save()
	except Exception as e:
		print 'Unable to get or save {0}: {1}'.format(role, e)
	return True


def saveMovieAndProfileData(response):
	rtn_dict = {'success':False, 'msg':''}
	try:
		movie, created = Movie.objects.get_or_create(imdb_id=response['imdbID'])
		movie.title = response['Title']

		genres = []
		movie_genres = response['Genre'].split(',')

		for movie_genre in movie_genres:
			genre, created = MovieGenre.objects.get_or_create(genre=movie_genre)
			genres.append(genre)

		movie.genres = genres
		movie.language = response['Language']
		movie.Country = response['Country']
		movie.metascore = int(response['Metascore'])
		movie.imdb_rating = float(response['imdbRating'])

		movie.save()

		movie = Movie.objects.get(imdb_id=response['imdbID'])

		# Saving Director Information
		saveUserProfile(movie.id, response['Director'], 'director')
		# Saving Writer Information
		saveUserProfile(movie.id, response['Writer'], 'writer')

		actors = response['Actors'].split(',')

		for actor in actors:
			saveUserProfile(movie.id, actor, 'actor')

		rtn_dict['success'] = True
	except Exception as e:
		print 'Unable to save movie and profile data from IMDB: {0}'.format(e)
		rtn_dict['msg'] = 'Unable to save movie and profile data from IMDB: {0}'.format(e)
		return rtn_dict
	return rtn_dict


def omdbSearchByTitle(request):
	rtn_dict = {"success": False, "msg": ""}

	#imdb_id = request.GET.get('id', False)
	movie_title = request.GET.get('title', False)

	if movie_title :
		url = OMDB_API + 't=' + movie_title
		response = searchOMDB(url)

		saved = saveMovieAndProfileData(response)
		if saved['success']:
			rtn_dict['response'] = response
			rtn_dict['msg'] = 'Successfully retrieved imdb movie data'
			rtn_dict['success'] = True
		else:
			rtn_dict['msg'] = 'Unable to save movie and profile data from IMDB: {0}'.format(saved['msg'])

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")