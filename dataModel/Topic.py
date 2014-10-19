'''
Created on 08.10.2014

@author: RM
'''

import logging
import math
from dataModel.ObjectWithDistanceFunction import ObjectWithDistanceFunction

class Topic(ObjectWithDistanceFunction):
    '''
    Class for topic data and corresponding methods.
    '''
    
    # Constructor
    def __init__(self, topicNumber):
        # Data
        self.logger = logging.getLogger(__name__)
        self._topicNumber = topicNumber
        self._keywordProbabilityMap = dict()
 
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
            #print "Topic #" + str(self._topicNumber) + ":\t", keywordDataset
            #print data
            return 1
        
        return 0
            
 
    # ---------------------------------------
    # Distance functions
    
    # Euclidean distance / L2-norm
    def calculateL2Distance(self, objectToCompare):
        self.logger.info("Calculating L2 distance/norm. Using topics #" + str(self._topicNumber) + " and #" + str(objectToCompare._topicNumber) + ".")
        
        squaredSum = 0
        # Assume all words are present in self._keywordProbabilityMap as well as objectToCompare._keywordProbabilityMap.
        for keyword, p in self._keywordProbabilityMap.iteritems():
            diff = p - objectToCompare._keywordProbabilityMap[keyword]
            squaredSum = squaredSum + diff * diff
            
        return math.sqrt(squaredSum)
        
    def calculateHellingerDistance(self, objectToCompare):
        self.logger.info("Calculating Hellinger distance. Using topics #" + str(self._topicNumber) + " and #" + str(objectToCompare._topicNumber) + ".")
        
        result = 0
        # Assume all words are present in self._keywordProbabilityMap as well as objectToCompare._keywordProbabilityMap.
        for keyword, p in self._keywordProbabilityMap.iteritems():
            tempResult = math.sqrt(p) - math.sqrt(objectToCompare._keywordProbabilityMap[keyword]) 
            
            result = result + tempResult * tempResult
            
        result = result / math.sqrt(2)
        
        return result
        
    
    # Bhattacharyya distance
    def calculateBhattacharyyaDistance(self, objectToCompare):
        self.logger.info("Calculating Bhattacharyya distance. Using topics #" + str(self._topicNumber) + " and #" + str(objectToCompare._topicNumber) + ".")
        
        result = 0
        # Assume all words are present in self._keywordProbabilityMap as well as objectToCompare._keywordProbabilityMap.
        for keyword, p in self._keywordProbabilityMap.iteritems():
            result = result + math.sqrt(p * objectToCompare._keywordProbabilityMap[keyword])

        result = math.log(result, 2) * (-1)
         
        return result 
    
    # Kullback-Leibler distance to base 2        
    def calculateKullbackLeiblerDistance(self, objectToCompare):
        self.logger.info("Calculating Kullback-Leibler distance. Using topics #" + str(self._topicNumber) + " and #" + str(objectToCompare._topicNumber) + ".")
        
        result = 0
        # Assume all words are present in self._keywordProbabilityMap as well as objectToCompare._keywordProbabilityMap.
        for keyword, p in self._keywordProbabilityMap.iteritems():
            result = result + p * math.log(p / objectToCompare._keywordProbabilityMap[keyword], 2)
            
        return result
    
    # Jensen-Shannon distance to base 2    
    def calculateJensenShannonDivergence(self, objectToCompare):
        self.logger.info("Calculating Jensen-Shannon divergence. Using topics #" + str(self._topicNumber) + " and #" + str(objectToCompare._topicNumber) + ".")
        
        tempSum_P = 0
        tempSum_Q = 0
        # Assume all words are present in self._keywordProbabilityMap as well as objectToCompare._keywordProbabilityMap.
        for keyword, p in self._keywordProbabilityMap.iteritems():
            # Value for "distribution" P (~ self) for this keyword
            currentValue_P = p
            # Value for "distribution" Q (~ objectToCompare) for this keyword
            currentValue_Q = objectToCompare._keywordProbabilityMap[keyword]
            # Value for mixture "distribution" M for this keyword
            currentValue_M = (currentValue_P + currentValue_Q) / 2
            
            tempSum_P = tempSum_P + currentValue_P * (math.log(currentValue_P, 2) - math.log(currentValue_M, 2))
            tempSum_Q = tempSum_Q + currentValue_Q * (math.log(currentValue_Q, 2) - math.log(currentValue_M, 2))
            
        # Calculate and return final results
        return (0.5 * (tempSum_P + tempSum_Q))
      
    # ---------------------------------------