'''
Created on 19.11.2014

@author: RM
'''

import os, csv
import sys
import logging
import hashlib

# Add paths to libraries (needed for pyinstall.py to work properly).
python_path      = "D:\Programme\Python27\\"
dependency_path  = "D:\Workspace\Eclipse\VKA_TopicMining\\"

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(python_path + "DLLs")
sys.path.append(python_path + "Lib")
sys.path.append(python_path + "Lib\multiprocessing")
sys.path.append(python_path + "Lib\site-packages")
sys.path.append(python_path + "Lib\site-packages\gensim-0.10.0-py2.7.egg")
sys.path.append(python_path + "Lib\site-packages\six-1.7.3-py2.7.egg")
sys.path.append(dependency_path + "pattern-2.6")
sys.path.append(dependency_path + "python-unicodecsv-0.9.4")

#from utils import Utils
from utils import SimplifiedConfiguration
from core import ParametrizedLDA
from core import CorporaReader
from core import TextProcessor

#import core.TextProcessor as TextProcessor
#import core.CorporaReader as CorporaReader


# Set maximal CSV field size
csv.field_size_limit(sys.maxsize)

# --------------------------------
# Get file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Get logger
#logger = Utils.initLogging()
# Set up logger
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)

# Parse arguments
configuration = SimplifiedConfiguration()
configuration.parseOptions()

# Set configuration options manually for test purposes.
#configuration.mode              = "sample"
#configuration.passes            = 1

logger.info(configuration.mode)
logger.info(configuration.passes)
logger.info(configuration.inputPath)
logger.info(configuration.outputPath)

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
            
    '''
    alphaValues     = [0.1, 0.5, 1, 5, 10]
    etaValues       = [0.1, 0.5, 1, 5, 10]
    fileLocations   = dict()
    
    relativeLocationPrefix = 'data/sampling/LDATopics';
    
    for eta in etaValues:
        configuration.eta   = eta;
        
        for alpha in alphaValues:
            relativeLocation    = relativeLocationPrefix + '_eta' + str(eta) + '_alpha' + str(alpha) + '.csv'
            configuration.alpha =  alpha;
            
            # Save location of result file
            fileLocations[alpha] = os.path.abspath(os.path.join(__location__, os.pardir, 'core/' + relativeLocation))
            
            if (configuration.useExistingData == False):
                logger.info("Applying LDA with eta = " + str(eta) + ", alpha = " + str(alpha))
                ParametrizedLDA.executeLDA(configuration, relativeLocation, True)
            else:
                logger.info("Using existing data for eta = " + str(eta) + ", alpha = " + str(alpha))
                
        #sampleAnalysis = Analysis(__location__, logger)
        #sampleAnalysis.compareSampledData(fileLocations, configuration.k, 'horizontal')
    '''
        
elif configuration.mode == "pre":
    logger.info("Preprocessing data.\n")
    CorporaReader.readCorpora()
    TextProcessor.processText()