#Keyvis Copora Reader
#reads through the KeyVisCopora folder and creates a single text file with one abstract per line
"""Todo:
#ensure comma separation in source files
#deal with non-ascii encoding
"""
import os, csv

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

with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'w') as file:
	for abstract in abstractList:
		output = abstract + '\n'
		file.write(output)