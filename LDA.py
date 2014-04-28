import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from nltk.corpus import stopwords


#load id2word Dictionary
id2word = corpora.Dictionary.load('/Users/charleywu/Github/CogSci/LSA/tmp/Brothers.dict')

#load Corpus iterator
mm = corpora.MmCorpus('/Users/charleywu/Github/CogSci/LSA/tmp/Brothers_tfidf.mm')

print mm

#Extract 100 LDA topics, using 5 pass and updating every 1 chunk (5,000 documents)
lda = models.ldamodel.LdaModel(corpus = mm, id2word = id2word, num_topics = 100, update_every=1, chunksize = 5000, passes = 5)

lda.print_topics(20)