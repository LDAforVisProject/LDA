''' LDA

@file: 		LDA.py
@author: 	Charley Wu, Matthias Hofer

Main topic modeling file:
Runs 'LDA' after textProcessor.py has done the text 
pre-processing and written KeyVis.dict and KeyVis_tfidf.mm

Also, provide a method for writing and visualizing topics

Allows for quicker experimentation with LDA parameters
'''

import logging 
#import chardet

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models
import os, csv

"""Model parameters"""
k = 20	#number of topics

""" Output settings """
nOfTerms = 10


#filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#load id2word Dictionary
dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))
#nOfTerms = len(dictionary)


#load Corpus iterator
mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))

print mm

#TRAIN LDA MODEL
lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k, 
	update_every=5, chunksize=100, passes=10)

#Method to print the k-most-likely terms for all found topics in a 
#more reader-friendly method
def visualizeTopics(lda, k, numberOfTerms):
	i = 0
	topicList = ''
	topicList_withProbabilities = ''
	topicListCollection_withProbabilities = []
	
	for topic in lda.show_topics(topics=k, formatted=False, topn=numberOfTerms):
		i = i + 1
		print "Topic #" + str(i) + ": ",
		
		for p, word in topic:
			topicList = topicList + word + ', '
			# TODO: Append to list
			topicList_withProbabilities = topicList_withProbabilities + word + '|' + str(p) + ', '
		
		print topicList[:-2]
		topicListCollection_withProbabilities.append(topicList_withProbabilities)
		
		topicList = ''
		topicList_withProbabilities = ''
	
	i = 0
	for topicList_withProbabilities in topicListCollection_withProbabilities:
		i = i + 1
		print "Topic #" + str(i) + ": ",
		print topicList_withProbabilities[:-2]
		
#Write topics to CSV
def writeTopics(outputfile, lda, k, numberOfTerms):
	with open(outputfile, 'wb') as output:
		topicList = []
		i = 0
		for topic in lda.show_topics(topics=k, formatted=False, topn=numberOfTerms):
			subTopicList = []
			i = i + 1
			subTopicList.append("Topic " + str(i))
			for p, word in topic:
				subTopicList.append(word + '|' + str(p))
			topicList.append(subTopicList)
		
		#transpose 2-d topic array; topics are now represented column-wise
		topicListTransposed = [list(j) for j in zip(*topicList)] 
		w = csv.writer(output)
		for q in topicListTransposed:
			try:
				w.writerow(q)
			except UnicodeEncodeError as e:
				"""
				# TODO: Install chardet, try to convert broken keyword strings into ASCII (or other working encoding).
				#		At least find working method to detect broken keyword strings.
				
				qAlternative = []
				i = 0
				for keyword in q:
					qAlternative[i] = keyword.decode(encoding['encoding']).encode('ascii')
					i++
				"""
				
				print "Not ACII-encoded"

print ""
outputfile = os.path.join(__location__, 'data/LDATopics.csv')

#Visualize Topics
visualizeTopics(lda, k, nOfTerms)

#Save topics to csv
writeTopics(outputfile, lda, k, nOfTerms)
