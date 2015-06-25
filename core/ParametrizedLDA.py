'''
Created on 19.11.2014

@author: RM
'''

import unicodecsv
from gensim import corpora, models
import os
import sqlite3
import logging

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
def writeTopics(dbConn, lda, configuration, numberOfTerms, alignment='vertical'):
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    errorCount = 0
    
    ldaConfigID = -1
    try:
        # Write LDA configuration to file.
        ldaValues = []
        
        ldaValues.append(configuration.alpha)
        ldaValues.append(configuration.k)
        ldaValues.append(configuration.eta)

        dbConn.execute("insert into ldaConfigurations (alpha, kappa, eta) VALUES (?, ?, ?)", ldaValues)
        # Commit query. 
        dbConn.commit()
        
    except:
        errorCount = errorCount + 1 #logger.info("ERROR")
    
    # Get ldaConfigID.
    for res in dbConn.execute(  "select ldaConfigurationID from ldaConfigurations " + 
                                "where alpha = ? and kappa = ? and eta = ?", ldaValues):
        ldaConfigID = res[0]
            
    i = 0
    # Write topics into db.
    for topic in lda.show_topics(topics=configuration.k, formatted=False, topn=numberOfTerms):
        try:
            # Write topic data into DB.    
            topicValues = []
            
            topicValues.append(i)
            topicValues.append(ldaConfigID)

            dbConn.execute("insert into topics (topicID, ldaConfigurationID) VALUES (?, ?)", topicValues)
            
        except:
            errorCount = errorCount + 1 #logger.info("ERROR / topic")
            
        keywordInTopicData = []
        for p, word in topic:
            keywordID = -1
            # Get ID for this keyword.
            try:
                request = "select keywordID from keywords " + "where keyword = '" + word + "'"
                #for res in dbConn.execute(  "select keywordID from keywords " + 
                #                            "where keyword = '?'", word):
                for res in dbConn.execute(request):
                    keywordID = int(res[0])
                
            except:
                errorCount = errorCount + 1 #logger.info("ERROR / keyword not found (probably has ' or \" in it).")
            
            finally:
                if (keywordID != -1):
                    #currValues.append(keywordID)
                    #currValues.append(p)
                    #currValues.append(ldaConfigID)
                    keywordInTopicData.append((i, keywordID, p, ldaConfigID))
                    
        # Increment topic counter.
        i = i + 1
        
        # Write batch of topic -> keyword/probability data to database.
        #'''
        try:
            dbConn.executemany('insert into keywordInTopic VALUES (?, ?, ?, ?)', keywordInTopicData)
        except:
            print keywordInTopicData
            
        dbConn.commit()
        #'''
        
    dbConn.close()

def writeTopicsToCSVFiles(outputfile, lda, configuration, numberOfTerms, alignment='vertical'):

    # Output to file:
    with open(outputfile, 'wb') as output:
        wunicode = unicodecsv.writer(output, encoding='utf-8')
        
        i = 0
        errorIndex = 0
        
        # Write configuration string to file.
        configStrings = []
        configStrings.append(configuration.toString())
        wunicode.writerow(configStrings);
        
        for topic in lda.show_topics(topics=configuration.k, formatted=False, topn=numberOfTerms):
                
            elementList = []
            i = i + 1
            
            for p, word in topic:
                elementList.append(word + '|' + str(p))
            
            # Write line to file.
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
def executeLDA(configuration, location, pathMode, writeToFile = False):
    # Filepath variables
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    # Load id2word Dictionary
    dictionary  = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))
    # Load Corpus iterator
    mm          = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))
    
    # Train LDA model
    lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=configuration.k, update_every=configuration.update_every, 
                                   passes=configuration.passes, alpha=configuration.alpha, eta=configuration.eta)
    
    if writeToFile == True:
        nOfTerms = len(dictionary)
        #print ""
        #Visualize Topics
        #visualizeTopics(lda, k, nOfTerms)
        #Save topics to csv
        if pathMode == "relative":
            fileLocation = os.path.join(__location__, location)
        elif pathMode == "absolute":
            fileLocation = location
            
        # Use horizontal topic/keyword alignment as default value.
        writeTopics(sqlite3.connect(configuration.dbPath), lda, configuration, nOfTerms, 'horizontal')
        #writeTopicsToCSVFiles(fileLocation, lda, configuration, nOfTerms, 'horizontal')
    return lda