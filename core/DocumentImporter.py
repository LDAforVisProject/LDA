''' AbstractMTKJoiner

@file:        DocumentImporter.py
@author:      Raphael Mitsch

Imports abstracts in their original form in the database.

'''

import os, csv, re
import time
import sqlite3
import logging
#from utils.unicodeHandling.UnicodeCSVHandler import *
from Crypto.PublicKey import pubkey

'''
    Imports documents (original and refined version) in specified database.
    Dev. function, not intended to be used in production.
    @param configuration Configuration object, holding e.g. the path to the used database file.   
'''
def importAbstractsInDB(configuration):

    # Define collection of data to import into DB.
    abstractDict        = {}
    keywordsDict        = {}
    conferenceDict      = {}
    dateDict            = {}
    titleDict           = {}
    doiDict             = {}
    publinkDict         = {}
    authorsDict         = {}
    refinedAbstractDict = {}

    # Get logger.
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Define target location.
    __location__    = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    corporaFolder   = os.path.join(__location__, 'KeyVisCorpora')
    
    try:
        '''
            1. Connect to database.
        '''
        dbConn              = sqlite3.connect(configuration.dbPath)

        # Change DB connection's text factory.
        dbConn.text_factory = str
        
        # Keeps track of which element is currently processed.
        # Note that this assumes equality of order in original and refined abstracts, which
        # (after thorough inspection) seems to be given.
        elementID   = 0
        # Auxiliary variable used to compare number of refined and number of original items.
        count       = 0
    
        '''
            2. If connected to database: Read documents (both original and refined).
        '''

        # Get list of files in directory.
        publications = os.listdir(corporaFolder)
        publications.sort()

        # Read original paper data.
        for publication in publications:
            if publication.endswith('.csv'): #only read csv-files!
                with open(os.path.join(corporaFolder, publication), 'rU') as csvfile:
                    #csvHandler = UnicodeCSVHandler()
                    #cr = csvHandler.read(open(os.path.join(corporaFolder, publication), 'rU'))
                    cr          = csv.reader(csvfile, delimiter='\t') #use tabstops delimiters!
                    
                    for document in cr:
                        if (len(document) >= 13):
                            keywords    = document[12] # keywords are in the csv-files' column 13
                            abstract    = document[13] # abstracts are in the csv-files' column 14
                            conference  = document[1]
                            date        = document[2]
                            title       = document[3]
                            doi         = document[4]
                            publink     = document[5]
                            authors     = document[14]

                            # Use only papers with existing abstracts, ignore non-content lines.
                            if abstract != "Abstract" and len(abstract) > 0:
                                abstractDict[elementID]         = str(abstract)
                                
                                # Add author information.
                                if keywords != "Author Keywords" and len(keywords) > 0:
                                    keywordsDict[elementID]     = str(keywords)
                                
                                # Add conference information.
                                if len(conference) > 0:
                                    conferenceDict[elementID]   = str(conference)
                                    
                                # Add date information.
                                if len(date) > 0:
                                    dateDict[elementID]         = str(date)
                                    
                                # Add title information.
                                if len(title) > 0:
                                    titleDict[elementID]        = str(title)

                                # Add DOI information.
                                if len(doi) > 0:
                                    doiDict[elementID]          = str(doi)

                                # Add publication link information.
                                if len(publink) > 0:
                                    publinkDict[elementID]      = str(publink)
                                    
                                # Add author information.
                                if len(authors) > 0:
                                    authorsDict[elementID]      = str(authors)

                                # Keep track of processed elements.
                                elementID += 1
                            
        # Read refined paper data.
        # Reset element ID.
        count       = elementID
        elementID   = 0

        with open(os.path.join(__location__, configuration.refinedAbstractsSummaryPath),'rU') as input:    
            cr = csv.reader(input)
            
            for line in cr:
                refinedAbstractDict[elementID] = str(line[0])
                elementID += 1
                
        # Number of original and refined items equal? If not, abort operation.
        if elementID != count:
            logger.critical("### ERROR ### Number of original items (papers) and refined abstracts is not equal: " + str(count) + " to " + str(elementID))
        
        '''
            3. Iterate through all documents - aggregate all information and insert them into the database.
        '''
        
        documentData = []
        for i in range(0, elementID):
            abstract        = abstractDict[i]
            refinedAbstract = refinedAbstractDict[i]
            keywords        = keywordsDict[i]       if i in keywordsDict else ""
            conference      = conferenceDict[i]     if i in conferenceDict else ""
            date            = dateDict[i]           if i in dateDict else ""
            title           = titleDict[i]          if i in titleDict else ""
            doi             = doiDict[i]            if i in doiDict else ""
            publink         = publinkDict[i]        if i in publinkDict else ""
            authors         = authorsDict[i]        if i in authorsDict else ""
            
            # Append tupel to document data collection.
            documentData.append((i, abstract, refinedAbstract, keywords, conference, date, title, doi, publink,  authors))
        
        # Insert collected data.
        dbConn.executemany("insert into documents (id, abstract, refinedAbstract, keywords, conference, date, title, doi, publication_link, authors) " +
                           "    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", documentData)
        
        # Commit transaction.
        dbConn.commit()
        # Close database.
        dbConn.close()
        
        logger.info("Finished import of documents.")
        
    except IOError:
        logger.critical("Failed database operation.\n")