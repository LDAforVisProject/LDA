#Main python file
#Reads from the joined abstracts.txt file created by corporaReader.py
#Preprocessing steps:
	#convert all to lowercase
	#tokenizes by white space
	#lemmatizes using the Pattern lemmatizer
	#removes stopwords based on the NLTK english stopword list
		#removes some additional terms that are manually populated in the variable exclusionlist
	#removes terms that only occur once


import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models
from nltk.corpus import stopwords
import csv, os
from pattern.vector import stem, LEMMA


#SET PARAMETERS
#number of topics
k = 10
#Filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


#Reads from "/KeyVisCorpora/abstracts.txt"
#Abstract list populated by corporaReader.py, which iterate through files in the KeyVisCorpora folder and writes them to a single file called 'abstracts.txt'
abstractList = []
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'rU') as inputFile:
	document = inputFile.readlines()
	for abstract in document:
		abstractList.append(abstract)


#Create token list from abstractList; unicode encoding and lower case
abstractTokens = [[unicode(word, "utf-8", errors = "ignore") for word in line.lower().split()] for line in abstractList]
abstractTokens = [[stem(word, stemmer=LEMMA) for word in line] for line in abstractTokens]
#Build dictionary
dictionary = corpora.Dictionary(abstractTokens)

#PREPROCESSING
#remove stop words and words that appear only once
stopwords = stopwords.words('english')
exclusionlist = ['-', 'se' ] #manually populated; add to this if necessary
stopwords = stopwords + exclusionlist
stop_ids = [dictionary.token2id[stopword] for stopword in stopwords if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq ==1]
dictionary.filter_tokens(stop_ids) #remove them from the dictionary "dictionary.filter_tokens(stop_ids + once_ids)"
dictionary.filter_tokens(once_ids) #remove terms that only occur once
dictionary.compactify() # remove gaps in id sequence after words that were removed
dictionary.save(os.path.join(__location__, 'data/KeyVis.dict')) #store dictionary for future reference

#dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))
#Initialize Corpus

#Memory efficient method to read from text without storing in RAM
class MyCorpus(object):
	def __iter__(self):
		for line in open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'rU'):
			line = unicode(line, errors='ignore')
			lowers = line.lower()
			tokenList = lowers.split()
			output = [stem(word, stemmer=LEMMA) for word in tokenList]
			#Assume there's one document per line, tokens separated by space
			yield dictionary.doc2bow([x.strip() for x in output])

corpus = MyCorpus()

#tf/idf transformation
tfidf = models.TfidfModel(corpus) #tfidf is a read-only object that converts any vector from the old representation to the new representation
corpus_tfidf = tfidf[corpus]

#Save as market matrix
corpora.MmCorpus.serialize(os.path.join(__location__, 'data/KeyVis_tfidf.mm'), corpus_tfidf)

mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))
print mm

#TRAIN LDA MODEL
lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k)
#example of more parameters
#lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k,  update_every=10, chunksize = 10, passes = 5)


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