'''
Created on 19.11.2014

@author: RM
'''

import unicodecsv
from gensim import corpora, models
import os
import sqlite3
import logging   
        
'''
Write topics to CSV
'''
def writeTopics(dbConn, lda, configuration, numberOfTerms):
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    errorCount  = 0
    ldaConfigID = -1
    
    # Get keyword IDs.
    keywordIDs  = dict()
    request     = "select * from keywords";
    for res in dbConn.execute(request):
        keywordIDs[res[1]] = int(res[0])
     
    try:
        # Write LDA configuration to file.
        ldaValues           = []
        
        ldaValues.append(configuration.alpha)
        ldaValues.append(configuration.k)
        ldaValues.append(configuration.eta)
        ldaValues.append(0)

        dbConn.execute("insert into ldaConfigurations (alpha, kappa, eta, generation_time) VALUES (?, ?, ?, ?)", ldaValues)
        # Commit query. 
        dbConn.commit()
        
    except:
        errorCount = errorCount + 1 #logger.info("ERROR")
    
    # Get ldaConfigID.
    for res in dbConn.execute(  "select ldaConfigurationID from ldaConfigurations " + 
                               "where alpha = ? and kappa = ? and eta = ?", ldaValues[:3]):
        ldaConfigID = res[0]
    

    # Store topic values.
    topicData           = []
    # Store keywordInTopic data.
    keywordInTopicData  = []
         
    # Get topics.
    topics = lda.show_topics(topics=configuration.k, formatted=False, topn=numberOfTerms)     
    
    i = 0
    # Pack topics into list.
    for topic in topics:
        topicData.append((i, ldaConfigID))
        # Increment topic counter.
        i = i + 1
    # Write topic list into DB.
    try:
        dbConn.executemany("insert into topics (topicID, ldaConfigurationID) VALUES (?, ?)", topicData)
    except IOError as error:
        print error
        
    i = 0
    # Write keyword in topic data into db.
    for topic in topics:
        keywordRank = 0
        for p, word in topic:
            # Get ID for this keyword.
            if word in keywordIDs:
                keywordInTopicData.append((i, keywordIDs[word], p, ldaConfigID, keywordRank))
            else:
                errorCount = errorCount + 1 #logger.info("ERROR / keyword not found (probably has ' or \" in it).")
            keywordRank = keywordRank + 1
        # Increment topic counter.
        i = i + 1
        
        # Write batch of topic -> keyword/probability data to database.
        #'''
        try:
            dbConn.executemany('insert into keywordInTopic VALUES (?, ?, ?, ?, ?)', keywordInTopicData)
            # Clear topic data array.
            #logger.critical("in writetopics - kit batch: " + str(i) + ", .len = " + str(len(keywordInTopicData)))
            keywordInTopicData = []
        except IOError as error:
            print error
    
    # Commit changes.
    dbConn.commit()
    
    # Output LDA configuration.
    logger.critical(configuration.toString())
    
    # Close connection to database.
    dbConn.close()


'''
Executes gensim's LDA with given arguments.
@return: Generated LDA object. 
'''
def executeLDA(configuration, location, pathMode, writeToFile = False):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Filepath variables
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    # Load id2word Dictionary
    dictionary  = corpora.Dictionary.load(os.path.join(__location__, 'data/KeyVis.dict'))
    # Load Corpus iterator
    mm          = corpora.MmCorpus(os.path.join(__location__, 'data/KeyVis_tfidf.mm'))
    
    
    # Train LDA model
    lda = models.ldamodel.LdaModel(corpus=mm, id2word=dictionary, num_topics=configuration.k, update_every=configuration.update_every, 
                                   passes=configuration.passes, alpha=configuration.alpha, eta=configuration.eta)
    
    print 'Printing corpus'
    blub = 0
    for doc in lda[mm]: 
        blub = blub + 1
    print 'count = ' + str(blub)
    
    
    #if writeToFile == True:    
        # Use horizontal topic/keyword alignment as default value.
        #writeTopics(sqlite3.connect(configuration.dbPath), lda, configuration, len(dictionary))
    
    return lda