import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from nltk.corpus import stopwords
import csv, os

# TEST


#Todo List:
#Chunk terms by comma separation
#Intialize Dictionary

#Filepath variable
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#f = open(os.path.join(__location__, 'bundled-resource.jpg'))

#Create Dictionary from text file
dictionary = corpora.Dictionary(line.lower().split() for line in open(os.path.join(__location__,'KeyVisData.csv')))

print dictionary

#remove stop words and words that appear only once
stop_ids = [dictionary.token2id[stopword] for stopword in stopwords.words('english') if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq ==1]
dictionary.filter_tokens(stop_ids) #remove them from the dictionary "dictionary.filter_tokens(stop_ids + once_ids)"
dictionary.compactify() # remove gaps in id sequence after words that were removed
dictionary.save(os.path.join(__location__, '/tmp/KeyVis.dict')) #store dictionary for future reference

dictionary = corpora.Dictionary.load(os.path.join(__location__, '/tmp/KeyVis.dict'))
print dictionary



#Initialize Corpus

#Memory efficient method to read from text without storing in RAM
class MyCorpus(object):
	def __iter__(self):
		for line in open(os.path.join(__location__,'KeyVisData.txt')):
			#Assume there's one document per line, tokens separated by whitespace
			yield dictionary.doc2bow(line.lower().split())

corpus = MyCorpus()

#tf/idf transformation
#TODO explore other possible transformations
tfidf = models.TfidfModel(corpus) #tfidf is a read-only object that converts any vector from the old representation to the new representation
corpus_tfidf = tfidf[corpus]

#Save as market matrix
corpora.MmCorpus.serialize(os.path.join(__location__, 'KeyVis_tfidf.mm'), corpus_tfidf)


mm = corpora.MmCorpus(os.path.join(__location__, 'KeyVis_tfidf.mm'))
print mm

"""
#Extract 400 LSI topics: using the default one-pass algorithm
lsi = models.lsimodel.LsiModel(corpus = mm, id2word = dictionary, num_topics = 400)
lsi.print_topics(10)
"""


