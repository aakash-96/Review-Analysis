import requests
import urllib2
from bs4 import BeautifulSoup
import re
from re import findall
import string

def url_Builder(movie_name):
	url = "http://www.omdbapi.com/?t="
	url+=movie_name
	json_response = requests.get(url)

	#error codes
	if json_response.status_code != 200:
		print('Status:', response.status_code, 'Problem with the request. Exiting.')
		exit()
	data = json_response.json()
	if len(data) == 2:
		return "error"

	imdb_id = data["imdbID"]
	print(data["Title"])
	print(imdb_id)
	final_url = "http://www.imdb.com/title/" + imdb_id +"/reviews"

	return final_url

def get_Reviews(movie_name):
	final_url = url_Builder(movie_name)
	final_url_global = final_url
	
	if final_url == "error":
		return None

	reviews=[]
	short_heads=[]
	for i in {0,10,20}:
		final_url=final_url_global
		final_url+="?start="+str(i)
		html = urllib2.urlopen(final_url)
		page = html.read()
		soup = BeautifulSoup(page, 'html.parser')
		tags = soup.find_all('div', id="tn15content")
		for i in tags:
			temp_reviews = i.find_all('p')
			temp_short_heads = i.find_all('h2')
		del(temp_reviews[-1])
		for i in temp_reviews:
			reviews.append(i)
		for i in temp_short_heads:
			short_heads.append(i)

	#extracting final text reviews from the html page
	final_reviews = []
	for i in reviews:
		final_reviews.append(i.text)
	final_short_heads = []
	for i in short_heads:
		final_short_heads.append(i.text)

	#since reviews are sent to parseouttext but short_heads are not
	for i in final_short_heads:
		temp = i.encode('ascii','ignore')
		temp = temp.translate(string.maketrans("",""),string.punctuation)
		temp = temp.lower()
		final_reviews.append(temp)
	return final_reviews,final_url_global

#final_url_global was returned so that get_hate_reviews and love reviews
#don't have to fetch the imdb id and form the url again

def get_hate_reviews(movie_name,final_url):
	final_url+="?filter=hate&spoiler=hide"
	html = urllib2.urlopen(final_url)
	page = html.read()
	soup = BeautifulSoup(page, 'html.parser')
	tags = soup.find_all('div', id="tn15content")
	for i in tags:
		reviews = i.find_all('p')
		short_heads = i.find_all('h2')
	del(reviews[-1])
	final_reviews = []
	for i in reviews:
		final_reviews.append(i.text.encode("ascii","ignore"))
	final_short_heads = []
	for i in short_heads:
		final_short_heads.append(i.text)
	for i in final_short_heads:
		temp = i.encode('ascii','ignore')
		temp = temp.translate(string.maketrans("",""),string.punctuation)
		temp = temp.lower()
		final_reviews.append(temp)
	return final_reviews

def get_love_reviews(movie_name,final_url):
	final_url+="?filter=love&spoiler=hide"
	html = urllib2.urlopen(final_url)
	page = html.read()
	soup = BeautifulSoup(page, 'html.parser')
	tags = soup.find_all('div', id="tn15content")
	for i in tags:
		reviews = i.find_all('p')
		short_heads = i.find_all('h2')
	del(reviews[-1])
	final_reviews = []
	for i in reviews:
		final_reviews.append(i.text)
	final_short_heads = []
	for i in short_heads:
		final_short_heads.append(i.text)
	for i in final_short_heads:
		temp = i.encode('ascii','ignore')
		temp = temp.translate(string.maketrans("",""),string.punctuation)
		temp = temp.lower()
		final_reviews.append(temp)
	return final_reviews
	
#----------------------------------------------------------leave the last one
#----------------------------------------------------------add spoiler to stopwords

#get_Reviews("Batman begins")