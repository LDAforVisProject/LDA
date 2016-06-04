''' AbstractMTKJoiner

@file:        DocumentImporter.py
@author:      Raphael Mitsch

Imports abstracts in their original form in the database.

'''

import os, csv, re
import time
#from utils.unicodeHandling.UnicodeCSVHandler import *

# Dev. function, not intended to be used in production. 
def importAbstractsInDB():
    print "Reading abstracts ..."
    
    abstractList = []
    keywordsList = []
    
    # Define target location.
    __location__    = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    corporaFolder   = os.path.join(__location__, 'KeyVisCorpora')

    # Use document ID for later references.
    documentID      = 0
    
    # Iterate through all documents.
    for publication in os.listdir(corporaFolder):
        if publication.endswith('.csv'): #only read csv-files!
            with open(os.path.join(corporaFolder, publication), 'rU') as csvfile:
                #csvHandler = UnicodeCSVHandler()
                #cr = csvHandler.read(open(os.path.join(corporaFolder, publication), 'rU'))
                cr          = csv.reader(csvfile, delimiter='\t') #use tabstops delimiters!
                
                for document in cr:
                    if (len(document) >= 13):
                        keywords = document[12] # keywords are in the csv-files' column 13
                        abstract = document[13] # abstracts are in the csv-files' column 14
                        if (keywords != "Author Keywords" and len(keywords) > 0): 
                            keywordsList.append(keywords)
                        if (abstract != "Abstract" and len(abstract) > 0): 
                            abstractList.append(abstract)
                            print '#' + str(documentID) + '* ' + abstract + '\n'
                            #target.write('#' + str(documentID) + '* ' + abstract + '\n')
                            documentID = documentID + 1
                        
    
    print "Finished reading  %i abstracts!" % len(abstractList)
    print "Finished reading  %i keyword sets!" % len(keywordsList)
    
    '''
        Current status: Order of papers in refined abstract list is the same as used in CorporaReader and, presumably, in used market matrix.
                        Consequently the n-th entry in gensim's topic-to-document transformation may be used to refer to the n-th abstract in the abstracts list.
                        Note: Pay attention to number of abstracts (2019 vs. multiples?).
                        
        Next steps:     
                        x Define and create document table in DB.
                        * Execute tag refinery postprocessing again.
                        * Continue work on DocumentImporter.py; import all documents in the DB.
                            - Refined text used for topic modelling (tagRefineryData.csv)
                            - Original text (as in original, primitive abstract list)
                        * topics_in_documents:
                            x Create topic_in_document table; 
                            - store relevant values when generating topic models.
                        * After that (testing!): Continue with GUI.
                            - Create component structure
                            - Add interactivitiy
    '''
    
    #target.close()