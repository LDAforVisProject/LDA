'''
Created on 10.10.2014

@author: RM
'''


import os, csv, re
import time
import codecs
from unicodeHandling.UnicodeCSVHandler import *

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

corporaFolder = os.path.join(__location__, 'KeyVisCorpora')
publication = "articleData1997.csv"

print "Reading abstracts ..."
abstractList = []
keywordList = []

with open(os.path.join(corporaFolder, publication), 'rU') as csvfile:
    cr = csv.reader(csvfile, delimiter='\t') #use tabstops delimiters!
    
    for document in cr:
        if (len(document) >= 13):
            keywords = document[12] # keywords are in the csv-files' column 13
            abstract = document[13] # abstracts are in the csv-files' column 14
            if (keywords != "Author Keywords" and len(keywords) > 0): 
                keywords = keywords.lower() #convert to lowercase
                #Using RegEx to clean up the data
                keywords = re.sub('[;]', ' ', keywords)
                keywords = re.sub('[:|.|[|]|]', '', keywords)
                keywords = re.sub('[0-9]+', '', keywords) #remove integers
                #keywords = re.sub('[a-z]', '', keywords) #remove single chars
            if (abstract != "Abstract" and len(abstract) > 0): 
                abstract = abstract.lower() #convert to lowercase
                #Using RegEx to clean up the data
                abstract = re.sub('[;|,|:|.|?|!|(|)|]', '', abstract)
                abstract = abstract + ' ' + keywords #concatenate abstracts and keywords
                try:
                    if "interval volume is" in abstract:
                        print abstract
                except UnicodeEncodeError as e:
                    print "ERROR"
                    print abstract.encode('utf-8')
                    x = raw_input('Continue?')
                
                abstractList.append(abstract)   
                
print "len(abstractList): " + str(len(abstractList)) 
'''
with codecs.open(os.path.join(corporaFolder, publication), 'rU', 'utf-8') as csvfile:
    #csvHandler = UnicodeCSVHandler()
    #cr = csvHandler.read(open(os.path.join(corporaFolder, publication), 'rU'))
    cr = csv.reader(csvfile, delimiter='\t') #use tabstops delimiters!
    
    for document in cr:
        if (len(document) >= 13):
            keywords = document[12] # keywords are in the csv-files' column 13
            abstract = document[13] # abstracts are in the csv-files' column 14
            if (keywords != "Author Keywords" and len(keywords) > 0): 
                keywords = keywords.lower() #convert to lowercase
                #Using RegEx to clean up the data
                keywords = re.sub('[;]', ' ', keywords)
                keywords = re.sub('[:|.|[|]|]', '', keywords)
                keywords = re.sub('[0-9]+', '', keywords) #remove integers
                #keywords = re.sub('[a-z]', '', keywords) #remove single chars
            if (abstract != "Abstract" and len(abstract) > 0): 
                abstract = abstract.lower() #convert to lowercase
                #Using RegEx to clean up the data
                abstract = re.sub('[;|,|:|.|?|!|(|)|]', '', abstract)
                abstract = abstract + ' ' + keywords #concatenate abstracts and keywords
                try:
                    print abstract
                except UnicodeEncodeError as e:
                    print "ERROR"
                    print abstract.encode('utf-8')
                    x = raw_input('Continue?')
                
                abstractList.append(abstract)
'''                