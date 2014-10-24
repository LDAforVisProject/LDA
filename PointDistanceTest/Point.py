'''
Created on 24.10.2014

@author: RM
'''

import math
import random
import logging

'''
Point coordinates use a unit (hyper-)cube.
'''
class Point(object):
    def __init__(self, dimension, base='cube'):
        self.logger         = logging.getLogger(__name__)
        
        self.dimension      = dimension
        self.base           = base
        self.coordinates    = [None] * self.dimension
            
        # Generate random numbers between for coordinates
        if self.base == 'cube':
            for index, coordinate in enumerate(self.coordinates):
                self.coordinates[index] = random.random()
                #print self.coordinates[index]
                
        else:
            raise Exception("This shape is not supported. Terminating program.")
        
    # ---------------------------------------
    # Distance functions
    
    def calculateDistance(self, pointToCompare, mode):
        if mode == "L2":
            return self.calculateL2Distance(pointToCompare)
        elif mode == "Hellinger":
            return self.calculateHellingerDistance(pointToCompare)
        elif mode == "Bhattacharyya":
            return self.calculateBhattacharyyaDistance(pointToCompare)
        elif mode == "KullbackLeibler":
            return self.calculateKullbackLeiblerDistance(pointToCompare)
        elif mode == "JensenShannon":                
            return self.calculateJensenShannonDivergence(pointToCompare)
    
    # Euclidean distance / L2-norm
    def calculateL2Distance(self, pointToCompare):
        self.logger.info("Calculating L2 distance/norm.")
        
        squaredSum = 0
        # Assume all words are present in self._keywordProbabilityMap as well as pointToCompare._keywordProbabilityMap.
        
        for index, coordinate in enumerate(self.coordinates):
            diff = self.coordinates[index] - pointToCompare.coordinates[index]
            squaredSum = squaredSum + diff * diff
            
        return math.sqrt(squaredSum)
        
    def calculateHellingerDistance(self, pointToCompare):
        self.logger.info("Calculating Hellinger distance.")
        
        result = 0
        # Assume all words are present in self._keywordProbabilityMap as well as pointToCompare._keywordProbabilityMap.
        for index, coordinate in enumerate(self.coordinates):
            tempResult = math.sqrt(self.coordinates[index]) - math.sqrt(pointToCompare.coordinates[index]) 
            
            result = result + tempResult * tempResult
            
        result = result / math.sqrt(2)
        
        return result
        
    
    # Bhattacharyya distance
    def calculateBhattacharyyaDistance(self, pointToCompare):
        self.logger.info("Calculating Bhattacharyya distance.")
        
        result = 0
        # Assume all words are present in self._keywordProbabilityMap as well as pointToCompare._keywordProbabilityMap.
        for index, coordinate in enumerate(self.coordinates):
            result = result + math.sqrt(self.coordinates[index] * pointToCompare.coordinates[index])

        result = math.log(result, 2) * (-1)
         
        return result 
    
    # Kullback-Leibler distance to base 2        
    def calculateKullbackLeiblerDistance(self, pointToCompare):
        self.logger.info("Calculating Kullback-Leibler distance.")
        
        result = 0
        # Assume all words are present in self._keywordProbabilityMap as well as pointToCompare._keywordProbabilityMap.
        for index, coordinate in enumerate(self.coordinates):
            result = result + self.coordinates[index] * math.log(self.coordinates[index] / pointToCompare.coordinates[index], 2)
            
        return result
    
    # Jensen-Shannon distance to base 2    
    def calculateJensenShannonDivergence(self, pointToCompare):
        self.logger.info("Calculating Jensen-Shannon divergence.")
        
        tempSum_P = 0
        tempSum_Q = 0
        # Assume all words are present in self._keywordProbabilityMap as well as pointToCompare._keywordProbabilityMap.
        for index, coordinate in enumerate(self.coordinates):
            # Value for "distribution" P (~ self) for this keyword
            currentValue_P = self.coordinates[index]
            # Value for "distribution" Q (~ pointToCompare) for this keyword
            currentValue_Q = pointToCompare.coordinates[index]
            # Value for mixture "distribution" M for this keyword
            currentValue_M = (currentValue_P + currentValue_Q) / 2
            
            tempSum_P = tempSum_P + currentValue_P * (math.log(currentValue_P, 2) - math.log(currentValue_M, 2))
            tempSum_Q = tempSum_Q + currentValue_Q * (math.log(currentValue_Q, 2) - math.log(currentValue_M, 2))
            
        # Calculate and return final results
        return (0.5 * (tempSum_P + tempSum_Q))
        