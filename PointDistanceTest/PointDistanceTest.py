'''
Created on 24.10.2014

@author: RM
'''

from Point import Point
import numpy as np
import matplotlib.pyplot as plt
import math
from optparse import OptionParser
import logging

logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------
# Init option parser
# ------------------------------------------------------------------------------------

parser = OptionParser()
parser.add_option("-k", "--k_dimensions", dest="k", type="int", help="write report to FILE", metavar="FILE")
parser.add_option("-n", "--n_points", dest="n", type="int", help="write report to FILE", metavar="FILE")

# Parse arguments
#    Determine number of dimensions
(options, args) = parser.parse_args()
if options.k == None:
    logger.info("WARNING: No option given for k (number of dimension. Assuming k = 10).")
    numberOfDimensions = 50
else:
    numberOfDimensions = options.k
#    Determine number of points     
if options.k == None:
    logger.info("WARNING: No option given for n (number of points. Assuming n = 50).")
    numberOfPoints = 50
else:
    numberOfPoints = options.n
    
# Number of distances between numberOfPoints points (Gaussian sum formula)
numberOfDistances = ( ( (numberOfPoints - 1) * (numberOfPoints - 1) + numberOfPoints - 1) / 2)

# Coordinate space base ('cube')
shape = 'cube'
# Distance function ('L2', 'Bhattacharyya', 'Hellinger', 'KullbackLeibler', 'JensenShannon')
#distanceFunctionNames = ['L2', 'Bhattacharyya', 'Hellinger', 'KullbackLeibler', 'JensenShannon']
distanceFunctionName = 'JensenShannon'

# ------------------------------------------------------------------------------------
# Prepare data, calculate distances
# ------------------------------------------------------------------------------------

# Data
points = [Point(dimension=numberOfDimensions, base=shape) for x in range(numberOfPoints)]
distances = [0] * numberOfDistances 

currentDistanceIndex = 0
for outerIndex in np.arange(0, numberOfPoints - 1):
    #print outerIndex
    for innerIndex in np.arange(outerIndex + 1, numberOfPoints):
        #print "  " + str(innerIndex)
        distances[currentDistanceIndex] =  points[outerIndex].calculateDistance(points[innerIndex], distanceFunctionName)
        currentDistanceIndex = currentDistanceIndex + 1 
        #print distances[currentDistanceIndex]


# ------------------------------------------------------------------------------------
# Plot data
# ------------------------------------------------------------------------------------

# Create x-ticks (sqrt(dim) ~ 100%)
xAxis_translationFactor = 100 / math.sqrt(numberOfDimensions)
x_ticks_range = range(numberOfDimensions)
x_ticks = [int((x * xAxis_translationFactor)) for x in x_ticks_range]
print xAxis_translationFactor
print x_ticks
print range(numberOfDimensions)

# https://stackoverflow.com/questions/11750276/matplotlib-how-to-convert-a-histogram-to-a-discrete-probability-mass-function
#distancesNormalized = np.histogram(distances,bins=50,normed=0)[0]/float(len(distances))
n, bins, patches = plt.hist(distances, bins=50, normed=0, facecolor='g', alpha=0.75)
plt.xlabel('Distance (in percent of ' + r'$\sqrt{k} = $' + str(math.sqrt(numberOfDimensions)) + ')')
plt.ylabel('Count')

# Mark sqrt(numberOfDimensions)
plt.axvline(x=math.sqrt(numberOfDimensions), ymin=0, ymax = 100, linewidth=3, color='r')

# Set tick labels and range/axis limits
#plt.ylim(0, max(distances))
plt.ylim(0, numberOfDistances / 10)
plt.xticks(x_ticks_range, x_ticks)
plt.xlim(0, math.sqrt(numberOfDimensions * 2) * 1)
plt.title('Point distances with distance function ' + distanceFunctionName + ' (k = ' + str(numberOfDimensions) + ', n = ' + str(numberOfPoints) + ')')
plt.grid(True)
plt.show()
