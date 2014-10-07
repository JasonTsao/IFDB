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

from movies.models import Movie, MovieGenre
from profiles.models import Profile

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

		try:
			director, created = Profile.objects.get_or_create(name=response['Director'], role='director')

			if created:
				director.movies.append(movie)
			director.save()
		except Exception as e:
			print 'Unable to get or save director: {0}'.format(e)
			pass

		movie.save()

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