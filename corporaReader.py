''' Keyvis Copora Reader

@file: 		corporaReader.py
@author: 	Charley Wu, Matthias Hofer

Reads through the KeyVisCopora-folder and creates 
a single text file with one abstract per line using 
the article keywords provided in the same corpus 
'data/KeyVisData.csv' as a dictionary; multi-word 
terms are are joined using underscores.

Keywords are appended to the abstract, since some 
abstracts might not even use the keywords thnoteey are 
tagged with.

Writes abstract to abstracts.txt
'''

import os, csv, re
import time
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


"""(1) Iterate through files in the KeyVisCorpora-folder and append each abstract to abstractList"""
"""In addition, append keywords to the abstracts"""
print "Reading abstracts ..."
abstractList = []
keywordList = []
corporaFolder = os.path.join(__location__, 'KeyVisCorpora')
for publication in os.listdir(corporaFolder):
	if publication.endswith('.csv'): #only read csv-files!
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
        	term.strip()
        	termLength = len(term)
        	keywordDict[term] = termLength #store term it's length in a dictionary 
print "Finished building keyword dictionary with %i terms!" % len(keywordDict.keys())


"""(3) Join any multi-word keywords that are also in the abstractList"""
sortedList = sorted(keywordDict, key=keywordDict.get, reverse=True)
print "Joining multi-word terms (this takes a few minutes) ..."
start = time.time()
#TODO: find a faster method to do this
#start replacment process with longest multi-word terms 
newAbstractList = []
for abstract in abstractList:
	for keyword in sortedList:
		tokenlist = keyword.split()
		joinedKeyword = '_'.join(tokenlist)
		if (keyword != joinedKeyword):
 			abstract = re.sub(keyword, joinedKeyword, abstract.strip())
 			# the following line is a workaround needed to fix issues with missing ' ' separation after 
 			# keyword replacement
 			abstract = re.sub('(?<=[a-z])visual', ' visual', abstract) #lookbehind for visualization_***
	newAbstractList.append(abstract)
print "Finished joining multi-word terms after", time.time() - start, "seconds!"

"""(4) Write to file"""		
print "Writing to file ..."
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'w') as file:
	for abstract in newAbstractList:
		output = abstract + '\n'
		file.write(output)
print "Pre-processing done!"
