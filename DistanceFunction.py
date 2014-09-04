'''
Created on 04.09.2014

@author: RM
'''

from abc import ABCMeta, abstractmethod

class DistanceFunction(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta

    
    def __init__(self):
        '''
        Constructor
        '''
     
    @abstractmethod
    def calculateDistance(self, keywordProbability_map1, keywordProbability_map2):
        print "\ncompareTopics()."


class NaiveDistanceFunction(DistanceFunction):
    def __init__(self):
        '''
        Constructor
        '''
            
    def calculateDistance(self, keywordProbability_map1, keywordProbability_map2):
        print "\ncompareTopics() with a naive distance function."      