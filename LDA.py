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
k = 10	#number of topics

#filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#load id2word Dictionary
dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))

#load Corpus iterator
mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))

print mm


#TRAIN LDA MODEL
lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k, 
	update_every=1, chunksize=10000, passes=5)

# Method to print topics in a more reader-friendly method
def visualizeTopics(lda, k, top):
	i = 0
	for topic in lda.show_topics(topics=k, formatted=False, topn=top):
		i = i + 1
		print "Topic #" + str(i) + ":\n",
		print "++++++++++++++"
		for p, word in topic:
			print word

		print ""
		
#Write topics to CSV
def writeTopics(outputfile, lda, k, topn=10):
	with open(outputfile, 'wb') as output:
		topicList = []
		for topic in lda.show_topics(topics=k, formatted=False, topn=topn):
			subTopicList = []
			for p, word in topic:
				subTopicList.append(word)
			topicList.append(subTopicList)
		w = csv.writer(output)
		for q in topicList:
			w.writerow(q)

#generate topics
visualizeTopics(lda, k, 10)
#Save topics to csv
writeTopics(os.path.join(__location__, 'data/LDATopics.csv'), lda, k)


