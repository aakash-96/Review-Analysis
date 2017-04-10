import pandas as pd
import numpy as np
import string
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from textblob import TextBlob as tb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import gc

from scraper import get_Reviews,get_hate_reviews,get_love_reviews


def parseOutText(document,movie_name):
	stop_words = set(stopwords.words("english"))
	
	#unicode to string
	document = document.encode("ascii","ignore")
	movie_name = movie_name.encode("ascii","ignore")
	#remove the punctuation and convert to lowercase
	document = document.translate(string.maketrans("",""),string.punctuation)
	document = document.lower()
	movie_name = movie_name.translate(string.maketrans("",""),string.punctuation)
	movie_name = movie_name.lower()

	#Blob object
	movie_name_blob = tb(movie_name)
	blob = tb(document)
	stop_words |= set(movie_name_blob.words)
	
	#removing the stopwords
	words = set(blob.words) - stop_words
	#stemming the words
	final_words = list(words)
	tset = set()
	stemmer = SnowballStemmer("english")
	for i in final_words:
		tset.add(stemmer.stem(i))
	#Converting to String
	final_string = ""
	if tset.__len__() > 0:
		final_string+=tset.pop()
	for i in range(tset.__len__()):
		final_string+=" "
		final_string+=tset.pop()
	
	return final_string

def partial_Parse_Out_Text(words_list,movie_name):
	stop_words = set(stopwords.words("english"))

	movie_name = movie_name.encode("ascii","ignore")
	movie_name = movie_name.translate(string.maketrans("",""),string.punctuation)
	movie_name = movie_name.lower()
	movie_name_blob = tb(movie_name)
	
	#adding movie name to stopwords list
	stop_words |= set(movie_name_blob.words)
	#removing the stopwords
	words = set(words_list) - stop_words
	#stemming the words
	final_words = list(words)
	tset = set()
	stemmer = SnowballStemmer("english")
	for i in final_words:
		tset.add(stemmer.stem(i))
	#Converting to String
	final_string = ""
	if tset.__len__() > 0:
		final_string+=tset.pop()
	for i in range(tset.__len__()):
		final_string+=" "
		final_string+=tset.pop()
	
	return final_string

#gathering the data
#text_data = pd.read_table("train.tsv")
#train_label = text_data.pop("Sentiment")
#train_phrase = text_data.pop("Phrase")

def train_data(movie_name):
	testfeats,final_url = get_Reviews(movie_name)
	if testfeats == None:
		return None,None,None

	#training corpus training data
	from nltk.corpus import movie_reviews
	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')
	negfeats = [movie_reviews.words(id) for id in negids]
	posfeats = [movie_reviews.words(id) for id in posids]

	label_train = []
	for i in range(len(negfeats)):
		label_train.append(0)
	for i in posfeats:
		label_train.append(1)
	trainfeats = negfeats + posfeats

	#pre-processing of the documents
	print("pre-processing of the documents")
	final_train_data = []
	for i in range(len(trainfeats)):
		temp = trainfeats[i]
		final_train_data.append(partial_Parse_Out_Text(temp,movie_name))
	gc.collect()
	
	hatefeats = get_hate_reviews(movie_name,final_url)
	print "Cleaning and parsing the hate movie reviews..."
	final_hate_reviews = []
	for i in range(len(hatefeats)):
		temp = hatefeats[i]
		final_hate_reviews.append(parseOutText(temp,movie_name))
	for i in range(len(final_hate_reviews)):
		label_train.append(0)

	lovefeats = get_love_reviews(movie_name,final_url)
	print "Cleaning and parsing the love movie reviews..."
	final_love_reviews = []
	for i in range(len(lovefeats)):
		temp = lovefeats[i]
		final_love_reviews.append(parseOutText(temp,movie_name))
	for i in range(len(final_love_reviews)):
		label_train.append(1)
	
	#complete training data set
	final_train_data = final_train_data + final_hate_reviews + final_love_reviews
	
	#Bag of Words
	print("Creating the bag of words")
	vectorizer = CountVectorizer()
	matrix = vectorizer.fit_transform(final_train_data)
	features_train = matrix.toarray()
	print(features_train.shape)

	tfidf = TfidfTransformer(sublinear_tf=True, norm=False)
	tfidf_matrix = tfidf.fit_transform(matrix)
	#print(tfidf_matrix.todense())
	gc.collect()

	# Create an empty list and append the clean reviews one by one
	print "\nCleaning and parsing the test set movie reviews..."
	final_test_data = []
	for i in range(len(testfeats)):
		temp = testfeats[i]
		final_test_data.append(parseOutText(temp,movie_name))

	# Get a bag of words for the test set, and convert to a numpy array
	features_test = vectorizer.transform(final_test_data)
	features_test = features_test.toarray()

	return features_train,features_test,label_train



def data():
	from nltk.corpus import movie_reviews

	negids = movie_reviews.fileids('neg')
	posids = movie_reviews.fileids('pos')

	negfeats = [movie_reviews.words(id) for id in negids]
	posfeats = [movie_reviews.words(id) for id in posids]

	negcutoff = len(negfeats)*3/4
	poscutoff = len(posfeats)*3/4

	label_train = []
	for i in negfeats[:negcutoff]:
		label_train.append(0)
	for i in posfeats[:poscutoff]:
		label_train.append(1)


	label_test = []
	for i in negfeats[negcutoff:]:
		label_test.append(0)
	for i in posfeats[poscutoff:]:
		label_test.append(1)

	trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
	testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]

	#pre-processing of the documents
	print("pre-processing of the documents")
	final_train_data = []
	for i in range(len(trainfeats)):
		temp = trainfeats[i]
		final_train_data.append(partial_Parse_Out_Text(temp,movie_name))
	#list of processed documents
	gc.collect()

	#Bag of Words
	print("Creating the bag of words")
	vectorizer = CountVectorizer()
	matrix = vectorizer.fit_transform(final_train_data)
	features_train = matrix.toarray()
	print(features_train.shape)

	tfidf = TfidfTransformer(sublinear_tf=True, norm=False)
	tfidf_matrix = tfidf.fit_transform(matrix)
	#print(tfidf_matrix.todense())
	gc.collect()


	# Create an empty list and append the clean reviews one by one

	print "Cleaning and parsing the test set movie reviews...\n"
	final_test_data = []
	for i in range(len(testfeats)):
		temp = testfeats[i]
		final_test_data.append(partial_Parse_Out_Text(temp,movie_name))

	# Get a bag of words for the test set, and convert to a numpy array
	features_test = vectorizer.transform(final_test_data)
	features_test = features_test.toarray()

	return features_train,features_test,label_train,label_test