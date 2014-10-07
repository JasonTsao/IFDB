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
		html_doc = html_doc.replace("&nbsp;", " ")
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
		html_doc = html_doc.replace("&nbsp;", "")
		soup = BeautifulSoup(html_doc)
		data_divs = soup.find_all(attrs={"class": "mp_box"})
		for data_div in data_divs:
			data_table = data_div.find_all('table')[0]
			data_rows = data_table.find_all('tr')
			for row in data_rows:
				results = None
				row_datas = row.find_all('td')
				result_string = str(row_datas[1])
				list_results = result_string.split("<br/>")
				for result in list_results:
					item_data = {}
					item_name = BeautifulSoup(result).find_all('a')
					if len(item_name) > 0:
						item_data["name"] = item_name[0].text
						item_data["url"] = item_name[0].get('href')
					else:
						item_data["name"] = item_name[0].text
					data[row_datas[0].text[:-1]] = item_data
				if len(list_results) < 1:
					data[row_datas[0].text[:-1]] = row_datas[1].text
		additional_page_li = soup.find_all(attrs={"class": "nav_tabs"})[0].find_all('a')
		for additional_page in additional_page_a:
			page_url = additional_page.get('href')
			new_url = "http://boxofficemojo.com{}".format(page_url)
			if additional_page.text == "Daily":
				loadDailyPerformanceData(new_url)
	except Exception, e:
		print e


def loadDailyPerformanceData(new_url):
	rtn_data = {}
	try:
		html_doc = urllib2.urlopen(new_url).read()
		soup = BeautifulSoup(html_doc)
		tables = soup.find_all('table')[7:]
		for table in tables:
			rows = table.find_all('tr')
			for row in rows:
				table_datas = row.find_all('td')
				for table_data in table_datas:
					datas = table_data.find_all('font')
					if len(datas) == 0:
						continue
					count = 0
					for data in datas:
						daily_data = {}
						count += 1
						if count == 1 and data.text == "Rank ":
							break
						if len(datas) == 11:
							if count % 2 == 0:
								continue
							elif count == 1:
								daily_data['rank'] = int(data.text)
							elif count == 3:
								daily_data['gross'] = int(data.text[1:])
							elif count == 5:
								daily_data['daily change'] = int(data.text[:-1])
							elif count == 9:
								daily_data['theaters'] = int(data.text.split(" / $")[0])
								daily_data['theater average'] = int(data.text.split(" / $")[1])
						elif len(datas) == 7:
							if count == 1:
								daily_data['rank'] = int(data.text)
							elif count == 2:
								daily_data['gross'] = int(data.text[1:])
							elif count == 3:
								daily_data['daily change'] = int(data.text[:-1])
							elif count == 6:
								daily_data['theaters'] = int(data.text.split(" / $")[0])
								daily_data['theater average'] = int(data.text.split(" / $")[1])
						elif len(datas) == 5:
							if count == 1:
								daily_data['rank'] = int(data.text)
							elif count == 2:
								daily_data['gross'] = int(data.text[1:])
							elif count == 4:
								daily_data['theaters'] = int(data.text.split(" / $")[0])
								daily_data['theater average'] = int(data.text.split(" / $")[1])
						date = table_data.find_all('a')[0].get('href').split('&')[0].split('sortdate=')[1]
						rtn_data[date] = daily_data
	except Exception, e:
		print e
	return rtn_data
