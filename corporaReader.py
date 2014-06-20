#Keyvis Copora Reader
#reads through the KeyVisCopora folder and creates a single text file with one abstract per line

import os, csv, re

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Iterate through files in the KeyVisCorpora folder and append each abstract to abstractList
abstractList = []
corporaFolder = os.path.join(__location__, 'KeyVisCorpora')
for publication in os.listdir(corporaFolder):
	if publication.endswith('.csv'): #ONLY READS CSV
		with open(os.path.join(corporaFolder,publication), 'rU') as csvfile:
			cr = csv.reader(csvfile, delimiter=',')
			for document in cr:
				if (len(document) >= 3):
					abstract = document[2]
					if abstract != "Abstract":
						abstractList.append(abstract)

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

#Join any multi-word keywords that are also in the abstractList with 
sortedList = sorted(keywordDict, key=keywordDict.get, reverse=True)

#find and replace
newAbstractList = []
for abstract in abstractList:
	for keyword in sortedList:
		tokenlist = keyword.split()
		joinedKeyword = "_".join(tokenlist)
		abstract = re.sub(keyword, joinedKeyword, abstract.strip())
	newAbstractList.append(abstract)

#Writes to file		
with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'w') as file:
	for abstract in newAbstractList:
		output = abstract + '\n'
		file.write(output)