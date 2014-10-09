from bs4 import BeautifulSoup

from lxml import html
from io import StringIO
from datetime import date, timedelta

from models import BOMMovieData

import xml.etree.ElementTree as ET
import datetime

import json
import urllib2
import urllib


@celery.task
def syncBoxOfficeMojoData():
	char_arr = ["NUM", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
	for char in char_arr:
		pullMovieDataFromList(char)


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
			data = {}
			if count == 0:
				count += 1
				continue
			movie_datas = movie.find_all('td')
			movie_name = movie_datas[0].find_all('b')[0].text
			data["name"] = movie_name
			movie_data_url = movie_datas[0].find_all('a')[0].get('href')
			movie_studio = movie_datas[1].find_all('font')[0].text
			data["studio"] = movie_studio
			total_gross = movie_datas[2].find_all('font')[0].text[1:].replace(",", "")
			data["total gross"] = total_gross
			if "/a" not in total_gross.lower():
				total_gross = int(total_gross)
			total_theaters = movie_datas[3].find_all('font')[0].text.replace(",", "")
			data["total theaters"] = total_theaters
			if "/a" not in total_theaters.lower():
				total_theaters = int(total_theaters)
			opening_gross = movie_datas[4].find_all('font')[0].text[1:].replace(",", "")
			if "/a" not in opening_gross.lower():
				opening_gross = int(opening_gross)
			data["opening gross"] = opening_gross
			opening_theaters = movie_datas[5].find_all('font')[0].text.replace(",", "")
			if "/a" not in opening_theaters.lower():
				opening_theaters = int(opening_theaters)
			data["opening theaters"] = opening_theaters
			opening = movie_datas[6].find_all('a')[0].text
			data["opening"] = opening
			data["details"] = pullMoviePageData(movie_data_url)
			bom_data = BOMMovieData(movie_name=movie_name)
			bom_data.movie_data = data
			bom_data.save()
	except Exception, e:
		print e


def pullMoviePageData(data_url):
	data = {}
	try:
		request_url = "http://boxofficemojo.com{}".format(data_url)
		html_doc = urllib2.urlopen(request_url).read()
		html_doc = html_doc.replace("&nbsp;", " ")
		soup = BeautifulSoup(html_doc)
		tables = soup.find_all('table')
		if len(tables) > 5:
			table = tables[5]
			rows = table.find_all('tr')
			for row in rows:
				row_data = row.text.split('\n')
				for item in row_data:
					item_info = item.split(": ")
					data[item_info[0]] = item_info[1]
		data_divs = soup.find_all(attrs={"class": "mp_box"})
		for data_div in data_divs:
			if len(data_div.find_all('table')) < 1:
				pass
			else:
				data_table = data_div.find_all('table')[0]
				data_rows = data_table.find_all('tr')
				for row in data_rows:
					results = None
					row_datas = row.find_all('td')
					if len(row_datas) < 2:
						continue
					result_string = str(row_datas[1])
					list_results = result_string.split("<br/>")
					if len(list_results) < 2:
						key = row_datas[0].text
						if key[-1:] == ":":
							key = key[:-1]
						data[key] = row_datas[1].text
					else:
						for result in list_results:
							item_data = {}
							item_name = BeautifulSoup(result).find_all('a')
							if len(item_name) > 0:
								item_data["name"] = item_name[0].text
								item_data["url"] = item_name[0].get('href')
							key = row_datas[0].text
							if key[-1:] == ":":
								key = key[:-1]
							data[key] = item_data
		next_data = soup.find_all(attrs={"class": "nav_tabs"})
		if len(next_data) > 0:
			additional_page_li = next_data[0].find_all('a')
			for additional_page in additional_page_li:
				page_url = additional_page.get('href')
				new_url = "http://boxofficemojo.com{}".format(page_url)
				if additional_page.text == "Daily":
					data["daily"] = loadDailyPerformanceData(new_url)
				if additional_page.text == "Foreign":
					data["foreign"] = loadForeignBoxOfficeData(new_url)
	except Exception, e:
		print "ERROR :: {}".format(e)
	return data


def loadDailyPerformanceData(new_url):
	rtn_data = []
	try:
		html_doc = urllib2.urlopen(new_url).read()
		html_doc = html_doc.replace("&nbsp;", " ")
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
					daily_data = {}
					for data in datas:
						count += 1
						if "rank" in data.text.lower():
							break
						if len(datas) == 11:
							if count % 2 == 0:
								continue
							elif count == 1:
								if "-" in data.text:
									daily_data['rank'] = "Not Ranked"
								else:
									daily_data['rank'] = int(data.text.replace(",", ""))
							elif count == 3:
								daily_data['gross'] = int(data.text[1:].replace(",", ""))
							elif count == 5:
								daily_data['daily change'] = float(data.text[:-1].replace(",", ""))
							elif count == 9:
								daily_data['theaters'] = int(data.text.split(" / $")[0].replace(",", ""))
								daily_data['theater average'] = int(data.text.split(" / $")[1].replace(",", ""))
						elif len(datas) == 7:
							if count == 1:
								if "-" in data.text:
									daily_data['rank'] = "Not Ranked"
								else:
									daily_data['rank'] = int(data.text.replace(",", ""))
							elif count == 2:
								daily_data['gross'] = int(data.text[1:].replace(",", ""))
							elif count == 3:
								daily_data['daily change'] = float(data.text[:-1].replace(",", ""))
							elif count == 6:
								daily_data['theaters'] = int(data.text.split(" / $")[0].replace(",", ""))
								daily_data['theater average'] = int(data.text.split(" / $")[1].replace(",", ""))
						elif len(datas) == 5:
							if count == 1:
								if "-" in data.text:
									daily_data['rank'] = "Not Ranked"
								else:
									daily_data['rank'] = int(data.text.replace(",", ""))
							elif count == 2:
								daily_data['gross'] = int(data.text[1:].replace(",", ""))
							elif count == 4:
								daily_data['theaters'] = int(data.text.split(" / $")[0].replace(",", ""))
								daily_data['theater average'] = int(data.text.split(" / $")[1].replace(",", ""))
						# this date is being stored with format YYYY-MM-DD
						date = table_data.find_all('a')[0].get('href').split('&')[0].split('sortdate=')[1]
						daily_data["date"] = date
						rtn_data.append(daily_data)
	except Exception, e:
		print "ERROR :: {}".format(e)
	return rtn_data


def loadForeignBoxOfficeData(new_url):
	rtn_data = []
	try:
		html_doc = urllib2.urlopen(new_url).read()
		html_doc = html_doc.replace("&nbsp;", " ")
		soup = BeautifulSoup(html_doc)
		tables = soup.find_all('table')
		if len(tables) > 5:
			table = tables[5]
			table_rows = table.find_all('tr')[3:]
			count = 0
			for row in table_rows:
				tds = row.find_all('td')
				if len(tds) > 5:
					if count == 0:
						count += 1
						continue
					print tds
					region_dict = {
						"country": tds[0].text,
						"distributor": tds[1].text,
						"release date": tds[2].text,
					}
					opening_weekend = tds[3].text[1:].replace(",", "")
					total_gross = tds[5].text[1:].replace(",", "")
					if "-" not in opening_weekend.lower() and len(opening_weekend) > 0:
						region_dict["opening weekend"] = int(opening_weekend)
					if "/a" not in total_gross.lower() and len(total_gross) > 0:
						region_dict["total gross"] = int(total_gross)
					rtn_data.append(region_dict)
	except Exception, e:
		print "ERROR (FOREIGN STATS) :: {}".format(e)
	return rtn_data


def loadWeekendBoxOfficeData(new_url):
	rtn_data = []
	try:
		html_doc = urllib2.urlopen(new_url).read().replace("&nbsp;", " ")
		soup = BeautifulSoup(html_doc)
		center = soup.find_all('center')
		if len(center) > 1:
			tables = center[1].find_all('table')
			if len(tables) > 1:
				for table in tables:
					rows = tables[6].find_all('tr')
					if len(rows) > 1:
						rows = rows[1:]
						for row in rows:
							data = row.find_all('td')
							rtn_item = {}
							try:
								rtn_item["date"] = data[0].text
							except Exception, e:
								continue
							try:
								rtn_item["week"] = int(data[7].text)
							except Exception, e:
								continue
							try:
								rtn_item["rank"] = int(data[1].text)
							except Exception, e:
								rtn_item["rank"] = None
							try:
								rtn_item["gross"] = int(data[2].text[1:])
							except Exception, e:
								rtn_item["gross"] = None
							try:
								rtn_item["theaters"] = int(data[4].text)
							except Exception, e:
								rtn_item["theaters"] = None
							rtn_data.append(rtn_item)
	except Exception, e:
		print "ERROR (WEEKEND STATS) :: {}".format(e)
	return rtn_data


def loadWeeklyBoxOfficeData(new_url):
	rtn_data = []
	try:
		html_doc = urllib2.urlopen(new_url).read().replace("&nbsp;", " ")
		soup = BeautifulSoup(html_doc)
		center = soup.find_all('center')
		if len(center) > 1:
			tables = center[1].find_all('table')
			if len(tables) > 0:
				count = 0
				for table in tables:
					year = int(center[1].find_all(attrs={"size": 5})[count].text)
					rows = table.find_all('tr')
					if len(rows) > 1:
						rows = rows[1:]
						for row in rows:
							try:
								data = row.find_all('td')
								item_data = {
									"year": year,
									"week number": int(datas[0].find_all('a')[0].get('href').split("wk=")[1].split("&")[1]),
								}
								try:
									item_data["rank"] = int(datas[1].text.replace(",", ""))
								except Exception, e:
									print e
								try:
									item_data["gross"] = int(datas[2].text[1:].replace(",", ""))
								except Exception, e:
									print e
								try:
									item_data["theaters"] = int(datas[4].text.replace(",", ""))
								except Exception, e:
									print e
								rtn_data.append(item_data)
							except Exception, e:
								print e
					count += 1
	except Exception, e:
		raise e
