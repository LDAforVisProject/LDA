'''
Created on 19.11.2014

@author: RM
'''

import os, csv
import sys
import logging
import utils.Utils as Utils
import utils.Configuration as Configuration
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
configuration = Configuration.Configuration()
configuration.parseOptions()

# Set configuration options manually for test purposes.
configuration.mode              = "sample"
configuration.k                 = 20
configuration.passes            = 1
configuration.useExistingData   = False

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
    logger.info("Sampling alpha values.\n")
    
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
        
elif configuration.mode == "pre":
    logger.info("Preprocessing data.\n")
    CorporaReader.readCorpora()
    TextProcessor.processText()