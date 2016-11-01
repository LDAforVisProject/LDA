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
#from utils.unicodeHandling.UnicodeCSVHandler import *

def readCorpora():
	# Filepath variable
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
							'''
							@todo: Numbers/years to remove?
							''' 
							keywords = re.sub('[;]', ' ', keywords)
							keywords = re.sub('[\']', '', keywords)
							# Remark: ['('], [')'] untested.
							keywords = re.sub('[(]', '', keywords)
							keywords = re.sub('[)]', '', keywords)
							keywords = re.sub('["]', '', keywords)
							keywords = re.sub('[:|.|[|]|]', '', keywords)
							keywords = re.sub('[0-9]+', '', keywords) #remove integers
							#keywords = re.sub('[a-z]', '', keywords) #remove single chars
						if (abstract != "Abstract" and len(abstract) > 0): 
							abstract = abstract.lower() #convert to lowercase
							#Using RegEx to clean up the data
							abstract = re.sub('[;|,|:|.|?|!|(|)|\'|"]', '', abstract)
							abstract = re.sub('[;]', '', abstract)
							abstract = re.sub('[,]', ' ', abstract)
							abstract = re.sub('["]', '', abstract)
							abstract = re.sub('[\']', '', abstract)
							abstract = abstract + ' ' + keywords #concatenate abstracts and keywords)
							abstractList.append(abstract)
						
	
	print "Finished reading  %i abstracts!" % len(abstractList)
	
	
	"""(2) Keywords dict (for swapping with low-freq single word terms)"""
	"""key value is the string length of the keyword, so we can sort by longest term"""
	print "Building keyword dictionary ..."
	keywordDict = {}
	with open(os.path.join(__location__,'data/KeyVisData.csv'),'rU') as input:
		#csvHandler = UnicodeCSVHandler()
		#cr = csvHandler.read(input, 'rU')
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
	#newAbstractList = []
	#for abstract in abstractList:
	#	for keyword in sortedList:
	#		tokenlist = keyword.split()
	#		joinedKeyword = '_'.join(tokenlist)
	#		print keyword + " -> " + joinedKeyword
	#		if (keyword != joinedKeyword):
	# 			abstract = re.sub(keyword, joinedKeyword, abstract.strip())
	# 			# the following line is a workaround needed to fix issues with missing ' ' separation after 
	# 			# keyword replacement
	# 			abstract = re.sub('(?<=[a-z])visual', ' visual', abstract) #lookbehind for visualization_***
	#	newAbstractList.append(abstract)
	#print "Finished joining multi-word terms after", time.time() - start, "seconds!"

	# Prepare finished joined keyword list. Should be faster than
	# joining all keywords for each abstract (remains to be seen).
	
	joinedKeywordMap = {}
	for keyword in sortedList:
			tokenlist = keyword.split()
			joinedKeyword = '_'.join(tokenlist)
			joinedKeywordMap[keyword] = joinedKeyword
			
	#start replacment process with longest multi-word terms 
	# To test
	newAbstractList = [] # ['' for x in range(len(abstractList))]
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
		
		'''
			@todo: Check if line below is necessary (in addition to .append). 
		'''
		#newAbstractList[i] = strippedAbstract
		
		#print abstract
		i = i + 1
	print "Finished joining multi-word terms after", time.time() - start, "seconds!"
	print "Replaced = " + str(repl)

	
	"""(4) Write to file"""		
	print "Writing to file ..."
	
	with open(os.path.join(__location__, 'KeyVisCorpora', 'abstracts.txt'), 'w') as file:
		for abstract in newAbstractList:
			output = abstract + '\n'
			file.write(output)
	print "Pre-processing done!"