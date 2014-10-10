'''
Created on 04.09.2014

@author: RM
'''

from abc import ABCMeta, abstractmethod

# Use ObjectWithDistanceFunction as interface for class Topic.
class ObjectWithDistanceFunction(object):
    '''
    Interface for various distance functions for class Topic.
    '''
    __metaclass__ = ABCMeta

    
    def __init__(self):
        '''
        Constructor
        '''
    
    # Function definitions for distance functions, to be implemented in inheriting class.
     
    @abstractmethod
    def calculateL2Distance(self, objectToCompare):
        print "\ncompareTopics()."
        
    @abstractmethod
    def calculateHellingerDistance(self, objectToCompare):
        print "\ncompareTopics()."
    
    @abstractmethod
    def calculateMahalanobisDistance(self, objectToCompare):
        print "\ncompareTopics()."
        
    @abstractmethod
    def calculateKullbackLeiblerDistance(self, objectToCompare):
        print "\ncompareTopics()."
        
    @abstractmethod
    def calculateJensenShannonDivergence(self, objectToCompare):
        print "\ncompareTopics()."                

'''
class NaiveDistanceFunction(DistanceFunction):
    def __init__(self):
'''
        
'''
            
    def calculateDistance(self, keywordProbability_map1, keywordProbability_map2):
        print "\ncompareTopics() with a naive distance function." 
        
'''     