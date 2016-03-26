''' Keyvis Copora Reader

@file:        AbstractMTKJoiner.py
@author:      Raphael Mitsch

Reads existing abstracts.txt, joins existing
multi-keyword terms. Difference to CorporaReader:
Existing abstracts.txt file is used.

'''

import os, csv, re
import time
#from utils.unicodeHandling.UnicodeCSVHandler import *

# Dev. function, not intended to be used in production.
# @param abstractsPath Path to existing abstracts file. 
def processTagRefineryData(abstractsPath):
    # Filepath variable
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    # Store individual abstracts (incl. appended keywords).
    abstractList = []
    
    #
    # 1. Load abstracts in list.
    #
    
    with open(os.path.join(__location__, abstractsPath),'rU') as input:    
        cr = csv.reader(input)
        for line in cr:
            abstractList.append(line[0])
    
    #
    # 2. Create keyword dictionary out of existing manually defined keyword lists.
    #
    
    """(2) Keywords dict (for swapping with low-freq single word terms)"""
    """key value is the string length of the keyword, so we can sort by longest term"""
    print "Building keyword dictionary ..."
    keywordDict = {}
    with open(os.path.join(__location__,'data/KeyVisData.csv'),'rU') as input:
        #csvHandler = UnicodeCSVHandler()
        #cr = csvHandler.read(input, 'rU')
        cr      = csv.reader(input)
        
        # Create dictionary out of defined terms.
        for line in cr:
            print line
            keywords = [x.lower() for x in line]
            for term in keywords:
                term.strip()
                termLength = len(term)
                keywordDict[term] = termLength #store term it's length in a dictionary 
    print "Finished building keyword dictionary with %i terms!" % len(keywordDict.keys())
    
    #
    # 3. Join multi-term keywords - goal: replace "X Y" in abstracts.txt with "X_Y", if
    #    "X Y" is a defined keyword (see step 2).
    #
        
    """(3) Join any multi-word keywords that are also in the abstractList"""
    sortedList = sorted(keywordDict, key=keywordDict.get, reverse=True)
    print "Joining multi-word terms (this takes a few minutes) ..."
    start = time.time()
    
    joinedKeywordMap = {}
    for keyword in sortedList:
            tokenlist = keyword.split()
            joinedKeyword = '_'.join(tokenlist)
            joinedKeywordMap[keyword] = joinedKeyword
    
    #start replacment process with longest multi-word terms 
    # To test
    newAbstractList = ['' for x in range(len(abstractList))]
    i = 0
    repl = 0
    for abstract in abstractList:
        strippedAbstract = abstract.strip()
        for keyword in sortedList:
            joinedKeyword = joinedKeywordMap[keyword]
            if (keyword != joinedKeyword):
                #print keyword + " -> " + joinedKeyword
                strippedAbstract = re.sub(keyword, joinedKeyword, strippedAbstract)
                repl = repl + 1
                # the following line is a workaround needed to fix issues with missing ' ' separation after 
                # keyword replacement
                strippedAbstract = re.sub('(?<=[a-z])visual', ' visual', strippedAbstract) #lookbehind for visualization_***
        newAbstractList.append(strippedAbstract)
        newAbstractList[i] = strippedAbstract
        #print abstract
        i = i + 1
    print "Finished joining multi-word terms after", time.time() - start, "seconds!"
    print "Replaced = " + str(repl)
    
    
    #
    # 4. Write refinded abstract collection to file.
    #
    
    """(4) Write to file"""        
    print "Writing to file ..."
    
    with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts_refined.txt'), 'w') as file:
        for abstract in newAbstractList:
            output = abstract + '\n'
            file.write(output)
    print "Pre-processing done!"    