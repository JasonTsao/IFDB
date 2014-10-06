from lxml import html
from io import StringIO
from datetime import date, timedelta

import xml.etree.ElementTree as ET
import datetime

import json
import urllib2
import urllib

def pullMovieDataFromList(list_id):
	request_url = "http://boxofficemojo.com/movies/alphabetical.htm?letter={0}&p=.htm".format(list_id)
	try:
		pass
	except Exception, e:
		print e
