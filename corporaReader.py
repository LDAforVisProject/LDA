''' Keyvis Copora Reader

@file: 		corporaReader.py
@author: 	Charley Wu, Matthias Hofer

Reads through the KeyVisCopora-folder and creates 
a single text file with one abstract per line using 
the article keywords provided in the same corpus 
'data/KeyVisData.csv' as a dictionary; multi-word 
terms are are joined using underscores.

Keywords are appended to the abstract, since some 
abstracts might not even use the keywords they are 
tagged with.

Writes abstract to abstracts.txt
'''

import os, csv, re
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


"""(1) Iterate through files in the KeyVisCorpora-folder and append each abstract to abstractList"""
"""In addition, append keywords to the abstracts"""
print "Reading abstracts ..."
abstractList = []
corporaFolder = os.path.join(__location__, 'KeyVisCorpora')
for publication in os.listdir(corporaFolder):
	if publication.endswith('.csv'): #only read csv-files!
		with open(os.path.join(corporaFolder, publication), 'rU') as csvfile:
			cr = csv.reader(csvfile, delimiter='\t') #use tabstops delimiters!
			for document in cr:
				if (len(document) >= 13):
					keywords = document[12] # keywords are 
					abstract = document[13]
					if (keywords != "Author Keywords" and len(keywords) > 0): 
						keywords = keywords.lower() #convert to lowercase
						keywords = re.sub('[;]', ' ', keywords)
						abstract = abstract + keywords
					if (abstract != "Abstract" and len(abstract) > 0): 
						abstract = abstract.lower() #convert to lowercase
						abstract = re.sub('[;,.]', '', abstract)
						abstractList.append(abstract)
					

print "Finished reading  %i abstracts!" % len(abstractList)


"""(2) Keywords dict (for swapping with low-freq single word terms)"""
"""key value is the string length of the keyword, so we can sort by longest term"""
print "Building keyword dictionary ..."
keywordDict = {}
with open(os.path.join(__location__,'data/KeyVisData.csv'),'rU') as input:
    cr = csv.reader(input)
    for line in cr:
    	keywords = [x.lower() for x in line]
        for term in keywords:
        	termLength = len(term)
        	keywordDict[term] = termLength

print "Finished building keyword dictionary with %i terms!" % len(keywordDict.keys())


"""(3) Join any multi-word keywords that are also in the abstractList"""
sortedList = sorted(keywordDict, key=keywordDict.get, reverse=True)
print "Joining multi-word terms (this takes a few minutes) ..."
#TODO: find a faster method to do this
newAbstractList = []
for abstract in abstractList:
	for keyword in sortedList:
		tokenlist = keyword.split()
		joinedKeyword = "_".join(tokenlist)
		abstract = re.sub(keyword, joinedKeyword, abstract.strip())
	newAbstractList.append(abstract)

print "Finished joining multi_word_terms!"


"""(4) Write to file"""		
print "Writing to file ..."
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'w') as file:
	for abstract in newAbstractList:
		output = abstract + '\n'
		file.write(output)
print "Pre-processing done!"

