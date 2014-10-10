'''
Created on 08.10.2014

@author: RM
'''

import logging
from dataModel.ObjectWithDistanceFunction import *

class Topic(ObjectWithDistanceFunction):
    '''
    Class for topic data and corresponding methods.
    '''
    
    # Data
    _keywordProbabilityMap = dict()
    
    # Constructor
    def __init__(self):
        self.logger = logging.getLogger(__name__)
 
    ''' 
    Add keyword data set to map.
    Returns 1 if keyword dataset contains resonable content. 
    '''
    def addKeywordDataset(self, keywordDataset):
        # data contains [0]: keyword and [1]: probability
        data = keywordDataset.split('|')
        # Store keyword as key, probability as value
        # Temporary workaround: Only execute if branch if STRING|FLOAT existent. Then remove " from data 
        # (should be cleared once encoding - on workflow-scope - is fixed).
        if len(data) > 1:
            data[1] = data[1].replace('"', '')
            self._keywordProbabilityMap[data[0]] = float(data[1])
        
            #print self._keywordProbabilityMap
            print keywordDataset
            #print data
            return 1
        
        return 0
            
 
    # Distance functions
    
    def calculateL2Distance(self, objectToCompare):
        self.logger.info("\nCalculating L2 distance/norm.")
        
    def calculateHellingerDistance(self, objectToCompare):
        self.logger.info("\nCalculating Hellinger distance.")
    
    def calculateMahalanobisDistance(self, objectToCompare):
        self.logger.info("\nCalculating Mahalanobis distance.")
        
    def calculateKullbackLeiblerDistance(self, objectToCompare):
        self.logger.info("\nCalculating Kullback-Leibler distance.")
        
    def calculateJensenShannonDivergence(self, objectToCompare):
        self.logger.info("\nCalculating Jensen-Shannon divergence.")