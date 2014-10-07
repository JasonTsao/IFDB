from lxml import html
from io import StringIO
from datetime import date, timedelta
from django.http import HttpResponse, HttpResponseRedirect

import xml.etree.ElementTree as ET
import datetime

import json
import urllib2
import oauth2 as oauth
import urllib

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


def omdbSearchByTitle(request):
	rtn_dict = {"success": False, "msg": ""}

	#imdb_id = request.GET.get('id', False)
	movie_title = request.GET.get('title', False)

	if movie_title :
		url = OMDB_API + 't=' + movie_title
		response = searchOMDB(url)
		rtn_dict['response'] = response
		rtn_dict['msg'] = 'Successfully retrieved imdb movie data'
		rtn_dict['success'] = True

	return HttpResponse(json.dumps(rtn_dict, indent=4), content_type="application/json")