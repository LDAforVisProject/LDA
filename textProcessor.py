''' Text Processor

@file: 		textProcessor.py
@author: 	Charley Wu, Matthias Hofer

Reads from the aggregated abstracts.txt file created by 
corporaReader.py

Requires: http://www.clips.ua.ac.be/pattern

Pre-processing steps:
	- tokenize by white space
	- lemmatize using the pattern lemmatizer
	- remove stopwords based on the 'NLTK english stopword 
		list
	- remove some additional terms that are manually 
		populated in the variable exclusionlist
	- remove single orccurence terms (singletons)
'''

import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import csv, os
import codecs
from gensim import corpora, models
from nltk.corpus import stopwords
from pattern.vector import stem, LEMMA

#Filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


"""(1) Read from abstracts.txt populated by corporaReader.py"""
print "Reading abstracts.txt ..."
abstractList = []
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'rU') as inputFile:
	document = inputFile.readlines()
	for abstract in document:
		abstractList.append(abstract)
print "Finished reading  %i abstracts.txt!" % len(abstractList)


"""(2) Create token list from abstractList; unicode encoding"""
print "Creating token list ..."
#abstractTokens = [[unicode(word, "utf-8", errors = "ignore") for word in line.split()] for line in abstractList]
#abstractTokens = [[stem(word, stemmer=LEMMA) for word in line] for line in abstractTokens]
abstractTokens = [[stem(word, stemmer=LEMMA) for word in line.split()] for line in abstractList]

"""Build dictionary and do dictionary pre-processing"""
print "Building dicitonary ..."
dictionary = corpora.Dictionary(abstractTokens)
#remove stop words and words that appear only once
stopwords = stopwords.words('english')
exclusionlist = ['-', 'se', 'h', 'd', 'iee', '+'] #manually populated; add to this if necessary
stopwords = stopwords + exclusionlist
stop_ids = [dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq ==1]
dictionary.filter_tokens(stop_ids) #remove them from the dictionary "dictionary.filter_tokens(stop_ids + once_ids)"
dictionary.filter_tokens(once_ids) #remove terms that only occur once
dictionary.compactify() # remove gaps in id sequence after words that were removed
dictionary.save(os.path.join(__location__, 'data/KeyVis.dict')) #store dictionary for future reference
#dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))


"""Initialize corpus"""
class MyCorpus(object):
	def __iter__(self):
		for line in open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'rU'):
			#line = unicode(line, 'utf-8', errors='ignore')
			lowers = line.lower()
			tokenList = lowers.split()
			output = [stem(word, stemmer=LEMMA) for word in tokenList]
			#Assume there's one document per line, tokens separated by space
			yield dictionary.doc2bow([x.strip() for x in output])

corpus = MyCorpus()


"""tf-idf transformation; tfidf is a read-only object that converts any vector 
from the old representation to the new representation"""
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#Save as market matrix
corpora.MmCorpus.serialize(os.path.join(__location__, 'data/KeyVis_tfidf.mm'), corpus_tfidf)
mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))
print "DONE:", mm
