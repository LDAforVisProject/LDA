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
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models
import os, csv

"""Model parameters"""
k = 20	#number of topics

#filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#load id2word Dictionary
dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))

#load Corpus iterator
mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))

print mm

#TRAIN LDA MODEL
lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k, 
	update_every=5, chunksize=100, passes=10)

#Method to print the k-most-likely terms for all found topics in a 
#more reader-friendly method
def visualizeTopics(lda, k, topn):
	i = 0
	topicList = ''
	for topic in lda.show_topics(topics=k, formatted=False, topn=topn):
		i = i + 1
		print "Topic #" + str(i) + ": ",
		for p, word in topic:
			topicList = topicList + word + ', '
		print topicList[:-2]
		topicList = ''
		
#Write topics to CSV
def writeTopics(outputfile, lda, k, topn):
	with open(outputfile, 'wb') as output:
		topicList = []
		i = 0
		for topic in lda.show_topics(topics=k, formatted=False, topn=topn):
			subTopicList = []
			i = i + 1
			subTopicList.append("Topic " + str(i))
			for p, word in topic:
				subTopicList.append(word)
			topicList.append(subTopicList)
		#transpose 2-d topic array; topics are now represented column-wise
		topicListTransposed = [list(j) for j in zip(*topicList)] 
		w = csv.writer(output)
		for q in topicListTransposed:
			w.writerow(q)

print ""
outputfile = os.path.join(__location__, 'data/LDATopics.csv')
nOfTerms = 10

#Visualize Topics
visualizeTopics(lda, k, nOfTerms)

#Save topics to csv
writeTopics(outputfile, lda, k, nOfTerms)
