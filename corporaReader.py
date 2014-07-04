#Keyvis Copora Reader
#reads through the KeyVisCopora folder and creates a single text file with one abstract per line
#Using the article keywords provided in the same corpus 'data/KeyVisData.csv' as a dictionary, 
#multi_word_terms are are joined using underscores

import os, csv, re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

print "Reading abstracts"
#Iterate through files in the KeyVisCorpora folder and append each abstract to abstractList
abstractList = []
corporaFolder = os.path.join(__location__, 'KeyVisCorpora')
for publication in os.listdir(corporaFolder):
	if publication.endswith('.csv'): #ONLY READS CSV
		with open(os.path.join(corporaFolder,publication), 'rU') as csvfile:
			cr = csv.reader(csvfile, delimiter='\t')
			for document in cr:
				if (len(document) >= 13):
					abstract = document[13]
					if abstract != "Abstract":
						abstractList.append(abstract)

print "Finished reading  %i abstracts" % len(abstractList)

#Keywords dict (for swapping with low-freq single word terms)
#key value is the string length of the keyword, so we can sort by longest term
keywordDict = {}
with open(os.path.join(__location__,'data/KeyVisData.csv'),'rU') as input:
    cr = csv.reader(input)
    for line in cr:
    	keywords = [x.lower() for x in line]
        for term in keywords:
        	termLength = len(term)
        	keywordDict[term] = termLength

print "Finished building keyword dictionary with %i terms" % len(keywordDict.keys())

#Join any multi-word keywords that are also in the abstractList with 
sortedList = sorted(keywordDict, key=keywordDict.get, reverse=True)

print "Joining multi_word_terms (this takes a few minutes)"
#find and replace
#TODO: find a faster method to do this
newAbstractList = []
for abstract in abstractList:
	for keyword in sortedList:
		tokenlist = keyword.split()
		joinedKeyword = "_".join(tokenlist)
		abstract = re.sub(keyword, joinedKeyword, abstract.strip())
	newAbstractList.append(abstract)

print "Finished joining multi_word_terms"
#Writes to file		
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'w') as file:
	for abstract in newAbstractList:
		output = abstract + '\n'
		file.write(output)