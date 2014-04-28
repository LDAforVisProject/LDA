import logging 
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities

#tiny example corpus of 9 documents
documents = ["Human machine interface for lab abc computer applications", "A survey of user opinion of computer system response time", "The EPS user interface management system", "System and human system engineering testing of EPS", "Relation of user perceived response time to error measurement", "The generation of random binary unordered trees", "The intersection graph of paths in trees", "Graph minors IV Widths of trees and well quasi ordering","Graph minors A survey"]


#remove common words and tokenize
#TODO: very simplified preprocessing method.  Replace with NLTK tools
stoplist = set('for a of the and to in'.split()) 
texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents] 

#remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]



#Convert documents to dictionary
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') #save for future use

#The gensim.corpora.dictionary.Dictionary class assigns a unique integer to each unique word
#The largest integery is equal to the number of dimenions of the vector representation for a document
print(dictionary.token2id) 


#converting tokenized documents to vectors
#doc2bow() counts the number of occurences of each distinct word, converts the word to its interger word id and returns the result as a sparse vector
new_doc = "Human computer interface"
new_vec = dictionary.doc2bow(new_doc.lower().split())
print(new_vec)

#Create Corpus
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) #store to disk for later use
print corpus

#CORPUS STREAMING - one document at a time for memory use
class MyCorpus(object):
	def __iter__(self):
		for line in open('sample.txt'):
			#Assume there's one document per line, tokens separated by whitespace
			yield dictionary.doc2bow(line.lower().split())

corpus_memory_friendly = MyCorpus() #Doesn't load the corpus into memory

for vector in corpus_memory_friendly:
	print vector
