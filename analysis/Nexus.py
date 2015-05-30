'''
Created on 19.11.2014

@author: RM
'''

import os, csv
import sys
import logging
import utils.Utils as Utils
import utils.Configuration as Configuration
import utils.SimplifiedConfiguration as SimplifiedConfiguration
import core.ParametrizedLDA as ParametrizedLDA
import core.TextProcessor as TextProcessor
import core.CorporaReader as CorporaReader


# Set maximal CSV field size
csv.field_size_limit(sys.maxsize)

# --------------------------------
# Get file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print __location__

# Get logger
logger = Utils.initLogging()

# Parse arguments
configuration = SimplifiedConfiguration.SimplifiedConfiguration()
configuration.parseOptions()

# Set configuration options manually for test purposes.
#configuration.mode              = "sample"
#configuration.passes            = 1

logger.info(configuration.mode)
logger.info(configuration.passes)
logger.info(configuration.inputPath)
logger.info(configuration.outputPath)

''' 
# Test reading of file with horizontal data alignment.
relativeLocation = 'data/sampling/LDATopics_test.csv'
#ParametrizedLDA.executeLDA(configuration.k, 1, configuration.passes, relativeLocation, True)
topicList = Topic.generateTopicsFromFile(os.path.abspath(os.path.join(__location__, os.pardir, 'core/' + relativeLocation)), configuration.k, 'horizontal')


for topic in topicList:
    for keyword, p in topic._sortedTupleList[:5]:
        print keyword + "|" + str(p)
    print '\n'
'''
        

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
            location = configuration.outputPath + '\\' + str(index) + '.csv'
            
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