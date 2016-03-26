'''
Created on 19.11.2014

@author: RM
'''

import os, csv
import sys
import logging
import hashlib

# Add paths to libraries (needed for pyinstall.py to work properly).
#python_path      = "D:\Programme\Python27\\"
#dependency_path  = "D:\Workspace\Eclipse\VKA_TopicMining\\"

#sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
#sys.path.append(python_path + "DLLs")
#sys.path.append(python_path + "Lib")
#sys.path.append(python_path + "Lib\multiprocessing")
#sys.path.append(python_path + "Lib\site-packages")
#sys.path.append(python_path + "Lib\site-packages\gensim-0.10.0-py2.7.egg")
#sys.path.append(python_path + "Lib\site-packages\six-1.7.3-py2.7.egg")
#sys.path.append(dependency_path + "pattern-2.6")
#sys.path.append(dependency_path + "python-unicodecsv-0.9.4")

#from utils import Utils
from utils import SimplifiedConfiguration
from core import ParametrizedLDA
from core import CorporaReader
from core import TextProcessor
from core import AbstractMTKJoiner
from gensim import corpora
import sqlite3

# Set maximal CSV field size
csv.field_size_limit(sys.maxsize)

# --------------------------------

# Get file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Set up logger
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.CRITICAL)
logger = logging.getLogger(__name__)

# Parse arguments
configuration = SimplifiedConfiguration()
configuration.parseOptions()

logger.info(configuration.mode)
logger.info(configuration.passes)
logger.info(configuration.update_every)
logger.info(configuration.inputPath)
logger.info(configuration.outputPath)
logger.info(configuration.dbPath)

# Prepare settings for import of keywords.
#configuration.mode          = "importKeywords"
#configuration.dbPath        = "D:\\Workspace\\Scientific Computing\\VKPSA_data - Copy\\vkpsa.db"

# Determine mode, start corresponding tasks.
if configuration.mode == "sample":
    logger.info("Sampling values as listed in " + configuration.inputPath + ".\n")
    
    # Read input file.
    with open(configuration.inputPath) as f:
        content = f.readlines()
        content = [x.strip('\n') for x in content] 
        
        index = 0
        for line in content:
            parameters = str.split(line, '|')
            
            # Gather data from current line.
            configuration.k     = int(str.split(parameters[0], '=')[1])
            configuration.alpha = float(str.split(parameters[1], '=')[1])
            configuration.eta   = float(str.split(parameters[2], '=')[1])
            
            # Determine file name.
            filename = (hashlib.sha1(configuration.toString().encode())).hexdigest()
            location = configuration.outputPath + '\\' + filename + '.csv'
            
            ParametrizedLDA.executeLDA(configuration, location, "absolute", True)
            
            # Increment file index.
            index += 1
        
elif configuration.mode == "pre":
    logger.info("Preprocessing data.\n")
    CorporaReader.readCorpora()
    TextProcessor.processText()
    
# Postprocess result of TagRefinery. Dev. function, not intended to be used in production.
# Uses existing abstracts.txt file.
elif configuration.mode == "pre_tagRefineryPostprocessing":
    logger.info("Preprocessing: Postprocessing TagRefinery data.")
    #AbstractMTKJoiner.processTagRefineryData("D:\\Workspace\Scientific Computing\\VKPSA_data - Copy\\tagRefineryData.csv")
    TextProcessor.processText()
    
elif configuration.mode == "importKeywords":
    logger.info("Importing keywords.\n")
    
    # Connect to DB.
    dbConn          = sqlite3.connect(configuration.dbPath)
    # Load dictionary.
    dictionary      = corpora.Dictionary.load(os.path.join(__location__ + "\\..\\core\\", 'data/KeyVis.dict'))
    # Initialize container for new keywords.
    wordsToInsert   = []
    
    # Loop through all words in dictionary.
    for id, word in dictionary.items():
        #print word
        wordsToInsert.append( (word,) )   
    # Commit changes to DB.
    dbConn.executemany("insert into keywords (keyword) VALUES (?)", wordsToInsert)
    # Commit query. 
    dbConn.commit()