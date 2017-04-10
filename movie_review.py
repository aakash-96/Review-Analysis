import pandas as pd
import numpy as np
import string
import gc

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

from features import data,train_data

movie_name = raw_input("Enter the movie name:")

#features_train,features_test,label_train,label_test = data()
features_train,features_test,label_train = train_data(movie_name)

if features_train == None:
	print("error: check the movie name")
	exit()

#from sklearn.naive_bayes import GaussianNB
#clf = GaussianNB()
#clf.fit(features_train,label_train)
#result = clf.predict(features_test)

from sklearn.metrics import accuracy_score
#print(accuracy_score(result,label_test))


print "Training the random forest..."
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators = 100) 
forest = forest.fit( features_train,label_train )
result = forest.predict(features_test)

count=0
size=0
for i in range(len(result)):
	if result[i]==1:
		count = count+1
	size = size+1
print(count,size)
x=float(count)/float(size)*100
print(r"{:f}% text reviews are positive".format(x))
#print(result)

#print(accuracy_score(result,label_test))


#from sklearn import svm
#clf = svm.SVC(kernel = "rbf", C = 10000.0)
#clf.fit(features_train,label_train)
#pred = clf.predict(features_test)
#print(accuracy_score(result,label_test))

#from sklearn import tree
#clf = tree.DecisionTreeClassifier(min_samples_split = 40)
#clf.fit(features_train,label_train)
#result = clf.predict(features_test)
#print(accuracy_score(result,label_test))
