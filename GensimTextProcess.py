import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from nltk.corpus import stopwords
import csv, os

#number of topics
k = 10

#Todo List:
#Chunk terms by comma separation
#Intialize Dictionary

#Filepath variable
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = os.path.join(__location__,'data')


#Create dictionary from text file
texts = []
with open(os.path.join(__location__,'KeyVisData.csv'),'rU') as input:
    cr = csv.reader(input)
    for line in cr:
    	output = [word.lower() for word in line]
        texts.append(output) 

dictionary = corpora.Dictionary(texts)

#remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stopwords.words('english') if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq ==1]
dictionary.filter_tokens(stop_ids) #remove them from the dictionary "dictionary.filter_tokens(stop_ids + once_ids)"
dictionary.compactify() # remove gaps in id sequence after words that were removed
dictionary.save(os.path.join(__location__, '/tmp/KeyVis.dict')) #store dictionary for future reference

dictionary = corpora.Dictionary.load(os.path.join(__location__, '/tmp/KeyVis.dict'))



#Initialize Corpus

#Memory efficient method to read from text without storing in RAM
class MyCorpus(object):
	def __iter__(self):
		for line in open(os.path.join(__location__,'KeyVisData.txt')):
			#Assume there's one document per line, tokens separated by comma
			yield dictionary.doc2bow(line.lower().split(','))

corpus = MyCorpus()

#tf/idf transformation
#TODO explore other possible transformations
tfidf = models.TfidfModel(corpus) #tfidf is a read-only object that converts any vector from the old representation to the new representation
corpus_tfidf = tfidf[corpus]

#Save as market matrix
corpora.MmCorpus.serialize(os.path.join(__location__, 'KeyVis_tfidf.mm'), corpus_tfidf)

mm = corpora.MmCorpus(os.path.join(__location__, 'KeyVis_tfidf.mm'))
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
"""
#CSV writer
with open('Sample.csv', 'wb') as output:
    w = csv.writer(output) #name and location of output file
    for q in SampleList:  #writes a new row for each item in SampleList
        w.writerow(q)
"""
visualizeTopics(lda, k, 10)


