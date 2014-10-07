from bs4 import BeautifulSoup

from lxml import html
from io import StringIO
from datetime import date, timedelta

import xml.etree.ElementTree as ET
import datetime

import json
import urllib2
import urllib


def syncBoxOfficeMojoData():
	pass


def pullMovieDataFromList(list_id):
	request_url = "http://boxofficemojo.com/movies/alphabetical.htm?letter={0}&p=.htm".format(list_id)
	try:
		html_doc = urllib2.urlopen(request_url).read()
		soup = BeautifulSoup(html_doc)
		html_tables = soup.find_all('table')
		movie_list = html_tables[3].find_all('tr')
		count = 0
		for movie in movie_list:
			if count = 0:
				count += 1
				continue
			movie_datas = movie.find_all('td')
			movie_name = movie_datas[0].find_all('b')[0].text
			movie_data_url = movie_datas[0].find_all('a')[0].get('href')
			movie_studio = movie_datas[1].find_all('font')[0].text
			total_gross = int(movie_datas[2].find_all('font')[0].text[1:])
			total_theaters = int(movie_datas[3].fidn_all('font')[0].text)
			opening_gross = int(movie_datas[4].find_all('font')[0].text[1:])
			opening_theaters = int(movie_datas[5].find_all('font')[0].text[1:])
			opening = movie_datas[6].find_all('a')[0].text
			details = pullMoviePageData(movie_data_url)
	except Exception, e:
		print e


def pullMoviePageData(data_url):
	request_url = "http://boxofficemojo.com{}".format(data_url)
	try:
		data = {}
		html_doc = urllib2.urlopen(request_url).read()
		soup = BeautifulSoup(html_doc)
		data_divs = soup.find_all(attrs={"class": "mp_box"})
		for data_div in data_divs:
			data_table = data_div.find_all('table')[0]
			data_rows = data_table.find_all('tr')
			for row in data_rows:
				results = None
				row_datas = row.find_all('td')
				list_results = row_datas[1].find_all('a')
				data[row_datas[0].text[:-1]] = row_datas[1].text
	except Exception, e:
		print e
