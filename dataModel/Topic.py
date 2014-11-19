'''
Created on 08.10.2014

@author: RM
'''

import logging
import math
import operator
import numpy as np
import matplotlib.pyplot as plt
import powerlaw as powerlaw_dedicated
from dataModel.ObjectWithDistanceFunction import ObjectWithDistanceFunction

class Topic(ObjectWithDistanceFunction):
    '''
    Class for topic data and corresponding methods.
    '''
    
    # Constructor
    def __init__(self, topicNumber):
        # Data
        self.logger                 = logging.getLogger(__name__)
        self._topicNumber           = topicNumber
        self._keywordProbabilityMap = dict()
        # To be initialized later
        self._sortedKeywordList     = None
        self._sortedProbabilityList = None
 
    ''' 
    Add keyword data set to map.
    @return 1 if keyword dataset contains resonable content. 
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
    
    '''
    Creates sorted list of keyword/probability tuples with descending probabilites, used for visualization and comparisons.
    '''
    def createdSortedListOfTuples(self):
        # Necessary to keep sortedTupleList as a attribute?
        sortedTupleList = sorted(self._keywordProbabilityMap.items(), key = operator.itemgetter(1), reverse=True)
        self._sortedKeywordList = map(operator.itemgetter(0), sortedTupleList)
        self._sortedProbabilityList = map(operator.itemgetter(1), sortedTupleList)
        
        #print sortedTupleList[1000]
        #print self._sortedKeywordList[1000]
        #print self._sortedProbabilityList[1000]
    
    ''' 
    Print object.
    @return Result to be printed. 
    '''
    def __str__(self):
        result = "Topic #" + str(self._topicNumber) + "\n"
        
        for item in self._sortedTupleList:
            result = result + item[0] + "|" + str(item[1]) + "\n"
        
        result = result + "\n"
        
        return result 
    
    # Sources: 
    #    http://matplotlib.org/examples/api/barchart_demo.html
    #    https://stackoverflow.com/questions/5207646/python-matplot-bar-function-arguments
    def plotKeywordProbabilities(self):
        self.logger.info("Drawing bar plot with probabilites of keywords, sorted descendingly.")
        probMax = max(self._sortedProbabilityList)
        self.logger.info("    Maximum in probabilities: " + str(probMax))
        
        # --------------------------------------
        
        # Instantiate new figure
        fig = plt.figure()

        # Set data
        n = len(self._sortedKeywordList)
        x = np.arange(n)
        y = self._sortedProbabilityList
        
        # --------------------------------------
        
        # Create new subplot (linear scale)
        ax_linear = fig.add_subplot(1, 2, 1)
        
        # Add a bar plot to the axis, ax.
        ax_linear.bar(x, y)
    
        ax_linear.set_ylim((0, probMax * 6 / 5))
        ax_linear.set_xlim((0, 500))

        # --------------------------------------
        
        # Create new subplot (logarithmic scale)
        ax_log = fig.add_subplot(1, 2, 2)
        
        # Add a bar plot to the axis, ax.
        ax_log.bar(x, y)
        ax_log.set_yscale('log')
        
        ax_log.set_ylim((0, probMax * 6 / 5))
        ax_log.set_xlim((0, 750))        
        
        # --------------------------------------
        
        # Fit power law parameters to distribution. 
        # Source: https://pypi.python.org/pypi/powerlaw
        fit = powerlaw_dedicated.Fit(y[:500], xmin=min(y[:500]), xmax = 1.0, estimate_discrete=False)
        print "alpha = " + str(fit.power_law.alpha)
        print "xmin = " + str(fit.power_law.xmin)
        print "xmax = " + str(fit.power_law.xmax)
        
        alpha = fit.power_law.alpha / 2.5
        print "Modified alpha = " + str(alpha)
        x_power = np.arange(1, 1000)
        y_power = [probMax * (value ** (-alpha)) for value in np.arange(1, 1000)]

        ax_linear.plot(x_power, y_power, color='y')
        ax_linear.set_ylim((0, probMax * 6 / 5))
        ax_linear.set_xlim((0, 500)) #_powerlaw
        
        plt.show()
            
    
    '''
    Print n-th most relevant keywords for easy comparisons with other topics.
    @param n Number of keywords to be printed.
    '''
#   def printLimitedKeywordList(self, n):
#       n = n + 1

       #for keyword, p in self._keywordProbabilityMap.iteritems():
       #     result = result + "     " + keyword + "|" + str(p) + "\n" 
        
 
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
    
    # Analyze LDA function output files