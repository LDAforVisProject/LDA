'''
Created on 19.11.2014

@author: RM
'''

import logging
import unicodecsv
from gensim import corpora, models
import os, csv

#Method to print the k-most-likely terms for all found topics in a 
#more reader-friendly method
def visualizeTopics(lda, k, numberOfTerms):
    i = 0
    topicList = ''
    topicList_withProbabilities = ''
    topicListCollection_withProbabilities = []
    
    for topic in lda.show_topics(topics=k, formatted=False, topn=numberOfTerms):
        i = i + 1
        print "Topic #" + str(i) + ": ",
        
        for p, word in topic:
            topicList = topicList + word + ', '
            topicList_withProbabilities = topicList_withProbabilities + word + '|' + str(p) + ', '

        print topicList[:-2]
        
        topicListCollection_withProbabilities.append(topicList_withProbabilities)
        topicList = ''
        topicList_withProbabilities = ''

    """    
    i = 0
    for topicList_withProbabilities in topicListCollection_withProbabilities:
        i = i + 1
        print "Topic #" + str(i) + ": ",
        print topicList_withProbabilities[:-2]
    """        
        
'''
Write topics to CSV
'''
def writeTopics(outputfile, lda, k, numberOfTerms, alignment='vertical'):
    if alignment == 'vertical':
        with open(outputfile, 'wb') as output:
            topicList = []
            i = 0
            for topic in lda.show_topics(topics=k, formatted=False, topn=numberOfTerms):
                subTopicList = []
                i = i + 1
                subTopicList.append("Topic " + str(i))
                for p, word in topic:
                    subTopicList.append(word + '|' + str(p))
                topicList.append(subTopicList)
            
            #transpose 2-d topic array; topics are now represented column-wise
            topicListTransposed = [list(j) for j in zip(*topicList)] 
            wunicode = unicodecsv.writer(output, encoding='utf-8')
            errorIndex = 0
            
            #unicodeCSVWriter = UnicodeWriter(output)
            #unicodeCSVWriter.writerows(topicListTransposed)
            
            for q in topicListTransposed:
                try:
                    #w.writerow(qAlternative)
                    #csv_writer.writerow(q)
                    wunicode.writerow(q)
                    
                except UnicodeEncodeError as e:
                    errorIndex = errorIndex + 1
                    print "LDA::writeTopics(): String seems not to be ASCII-encoded. See issue #5. Error #" + str(errorIndex)
                    print e
                    
    elif alignment == 'horizontal':
        with open(outputfile, 'wb') as output:
            wunicode = unicodecsv.writer(output, encoding='utf-8')
            
            i = 0
            errorIndex = 0
            
            for topic in lda.show_topics(topics=k, formatted=False, topn=numberOfTerms):
                elementList = []
                i = i + 1
                for p, word in topic:
                    elementList.append(word + '|' + str(p))
                
                try:
                    #w.writerow(qAlternative)
                    #csv_writer.writerow(q)
                    wunicode.writerow(elementList)
                    
                except UnicodeEncodeError as e:
                    errorIndex = errorIndex + 1
                    print "LDA::writeTopics(): String seems not to be ASCII-encoded. See issue #5. Error #" + str(errorIndex)
                    print e            

'''
Executes gensim's LDA with given arguments.
@return: Generated LDA object. 
'''
def executeLDA(k, alpha, passes, relativeLocation, writeToFile = False):
    # Filepath variables
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    #load id2word Dictionary
    dictionary = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))
    #load Corpus iterator
    mm = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))
    
    nOfTerms = len(dictionary)
    
    # Train LDA model
    lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=k, 
        update_every=5, chunksize=100, passes=passes)
    
    if writeToFile == True:
        #print ""
        #Visualize Topics
        #visualizeTopics(lda, k, nOfTerms)
        #Save topics to csv
        fileLocation = os.path.join(__location__, relativeLocation)
        writeTopics(fileLocation, lda, k, nOfTerms, 'horizontal')
        
    return lda