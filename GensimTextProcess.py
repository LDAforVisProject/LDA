import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models
from nltk.corpus import stopwords
import csv, os
import pattern #for gensim to lemmatize text, it requires this module


"""
#Todo list:
#Convert 2012 file into csv
#Convert 2013 file into csv
#check on really short abstracts
#replace low frequency terms with multi_word_terms from keyword list
"""


#SET PARAMETERS
#number of topics
k = 10
#Filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


#Reads from "/KeyVisCorpora/abstracts.txt"
#Abstract list populated by corporaReader.py, which iterate through files in the KeyVisCorpora folder and writes them to a single file called 'abstracts.txt'
abstractList = []
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'r') as inputFile:
	document = inputFile.readlines()
	for abstract in document:
		abstractList.append(abstract)

#Keywords dict (for swapping with low-freq single word terms)
#key value is the string length of the keyword, so we can sort by longest term
keywordDict = {}
with open(os.path.join(__location__,'data/KeyVisData.csv'),'rU') as input:
    cr = csv.reader(input)
    for line in cr:
    	keywords = [x.lower() for x in line]
        for term in keywords:
        	termLength = len(term)
        	keywordDict[term] = termLength

#Join any multi-word keywords that are also in the abstractList with 
sortedList = sorted(keywordDict, key=keywordDict.get, reverse=True)
print sortedList

#Create token list from abstractList; unicode encoding and lower case
abstractTokens = [[unicode(word, "utf-8", errors = "ignore") for word in document.lower().split()] for document in abstractList]

#Build dictionary
dictionary = corpora.Dictionary(abstractTokens)





#remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stopwords.words('english') if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq ==1]
dictionary.filter_tokens(stop_ids) #remove them from the dictionary "dictionary.filter_tokens(stop_ids + once_ids)"
dictionary.compactify() # remove gaps in id sequence after words that were removed
dictionary.save(os.path.join(__location__, 'data/KeyVis.dict')) #store dictionary for future reference

dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))



#Initialize Corpus

#Memory efficient method to read from text without storing in RAM
class MyCorpus(object):
	def __iter__(self):
		for line in open(os.path.join(__location__,'data/KeyVisData.txt')):
			#Assume there's one document per line, tokens separated by comma
			yield dictionary.doc2bow(line.lower().split(','))

corpus = MyCorpus()

#tf/idf transformation
#TODO explore other possible transformations
tfidf = models.TfidfModel(corpus) #tfidf is a read-only object that converts any vector from the old representation to the new representation
corpus_tfidf = tfidf[corpus]

#Save as market matrix
corpora.MmCorpus.serialize(os.path.join(__location__, 'data/KeyVis_tfidf.mm'), corpus_tfidf)

mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))
print mm


#Extract LSI topics using the default one-pass algorithm
# lsi = models.lsimodel.LsiModel(corpus=mm, id2word=dictionary, num_topics=k)
# lsi.print_topics(k)

lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k,  update_every=10, chunksize = 10, passes = 5)
# lda.print_topics(k)

# We print the topics
def visualizeTopics(lda, k, top):
	i = 0
	for topic in lda.show_topics(topics=k, formatted=False, topn=top):
		i = i + 1
		print "Topic #" + str(i) + ":\n",
		print "++++++++++++++"
		for p, word in topic:
			print word

		print ""
		
#CSV writer example
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

visualizeTopics(lda, k, 10)

writeTopics(os.path.join(__location__, 'data/LDATopics.csv'), lda, k)