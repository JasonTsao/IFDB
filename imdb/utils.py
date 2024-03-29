import xml.etree.ElementTree as ET
import datetime
import json
import urllib2
import oauth2 as oauth
import urllib

from django.db.models import Q
from lxml import html
from io import StringIO
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect

from profiles.models import UserProfile, Profile, CollaborationLink
from movies.models import Movie, MovieGenre

OMDB_API = 'http://www.omdbapi.com/?'


def searchOMDB(url):
	response = False
	try:
		conn = urllib2.urlopen(url)
		try:
			response = json.loads(conn.read())
		finally:
			conn.close()
	except urllib2.HTTPError as error:
		print 'Error getting imdb data: {0}'.format(error)
	return response


def saveUserProfile(movie, name, role):
	try:
		user, created = UserProfile.objects.get_or_create(name=name)

		profile, created = Profile.objects.get_or_create(user=user, name=name, role=role)

		if created:
			movies_array = profile.movies

			if not movies_array:
				movies_array = []

			movies_array.append(movie.id)
			profile.movies = movies_array
		else:
			movies_array = profile.movies

			if not movie in movies_array:
				movies_array.append(movie.id)
				profile.movies = movies_array

		profile.save()

	except Exception as e:
		print 'Unable to get or save {0}: {1}'.format(role, e)
	return profile.id


def addProfileLinks(profiles_list, movie):
	try:
		for profile in profiles_list:
			for profile_user in profiles_list:
				if profile != profile_user:

					p1_profile = Profile.objects.get(pk=profile)
					p2_profile = Profile.objects.get(pk=profile_user)

					try:
						CollaborationLink.objects.get(profile_1=p2_profile, profile_2=p1_profile)
					except:
						collaboration_link, created = CollaborationLink.objects.get_or_create(profile_1=p1_profile, profile_2=p2_profile)
						if not movie in collaboration_link.movies:
							collaboration_link.movies.append(movie)
							collaboration_link.save()
					
	except Exception as e:
		print 'Unable to add profile link: {0}'.format(e)
	return True


def saveMovieAndProfileData(response):
	rtn_dict = {'success':False, 'msg':''}
	try:
		movie_collaborators = []
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

		movie.release_date = datetime.datetime.strptime(response['Released'], '%d %b %Y').date()
		movie.year = int(response['Year'])
		movie.save()

		movie = Movie.objects.get(imdb_id=response['imdbID'])

		# Saving Director Information
		director_id = saveUserProfile(movie, response['Director'].strip(), 'director')
		# Saving Writer Information
		writer_id = saveUserProfile(movie, response['Writer'].strip(), 'writer')

		movie_collaborators.append(director_id)
		movie_collaborators.append(writer_id)

		actors = response['Actors'].split(',')

		for actor in actors:
			actor_id = saveUserProfile(movie, actor.strip(), 'actor')
			movie_collaborators.append(actor_id)

		addProfileLinks(movie_collaborators, movie.id)

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
		request_parameters = {
			't': movie_title
		}

		url = OMDB_API + urllib.urlencode(request_parameters)
		response = searchOMDB(url)

		saved = saveMovieAndProfileData(response)
		if saved['success']:
			rtn_dict['response'] = response
			rtn_dict['msg'] = 'Successfully retrieved imdb movie data'
			rtn_dict['success'] = True
		else:
			rtn_dict['msg'] = 'Unable to save movie and profile data from IMDB: {0}'.format(saved['msg'])

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")