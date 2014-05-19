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
#replace low frequency terms with multi-word terms from keyword list
"""


#number of topics
k = 10

#Filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


#Iterate through files in the KeyVisCorpora folder and append each abstract to abstractList
abstractList = []
corporaFolder = os.path.join(__location__, 'KeyVisCorpora')
for publication in os.listdir(corporaFolder):
	if publication.endswith('.csv'):
		with open(os.path.join(corporaFolder,publication), 'rU') as csvfile:
			cr = csv.reader(csvfile, delimiter=',')
			for document in cr:
				if (len(document) >= 3):
					abstract = document[2]
					if abstract != "Abstract":
						abstractList.append(abstract)

#Create token list; unicode encoding and lower case
abstractTokens = [[unicode(word, "utf-8", errors = "ignore") for word in document.lower().split()] for document in abstractList]

#Build dictionary
dictionary = corpora.Dictionary(abstractTokens)


#Keywords list (for swapping with low-freq single word terms)
#still unused
keywords = []
with open(os.path.join(__location__,'data/KeyVisData.csv'),'rU') as input:
    cr = csv.reader(input)
    for line in cr:
    	output = [word.lower() for word in line]
        keywords.append(output) 


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

lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k)
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