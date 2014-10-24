'''
Created on 24.10.2014

@author: RM
'''

from Point import Point
import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters
numberOfPoints      = 100
# Number of distances between numberOfPoints points (Gaussian sum formula)
numberOfDistances   = ( ( (numberOfPoints - 1) * (numberOfPoints - 1) + numberOfPoints - 1) / 2)
print numberOfDistances
# Number of dimensions
numberOfDimensions  = 100

# Coordinate space base ('cube')
shape = 'cube'
# Distance function ('L2', 'Bhattacharyya', 'Hellinger', 'KullbackLeibler', 'JensenShannon')
distanceFunctionName = 'L2'

# Data
points = [Point(dimension=numberOfDimensions, base=shape) for x in range(numberOfPoints)]
distances = [0] * numberOfDistances 

# Calculate distances
currentDistanceIndex = 0
for outerIndex in np.arange(0, numberOfPoints - 1):
    #print outerIndex
    for innerIndex in np.arange(outerIndex + 1, numberOfPoints):
        #print "  " + str(innerIndex)
        distances[currentDistanceIndex] =  points[outerIndex].calculateDistance(points[innerIndex], distanceFunctionName)
        currentDistanceIndex = currentDistanceIndex + 1 
        #print distances[currentDistanceIndex]


# https://stackoverflow.com/questions/11750276/matplotlib-how-to-convert-a-histogram-to-a-discrete-probability-mass-function
#distancesNormalized = np.histogram(distances,bins=50,normed=0)[0]/float(len(distances))
n, bins, patches = plt.hist(distances, bins=50, normed=0, facecolor='g', alpha=0.75)
plt.xlabel('Distance')
plt.ylabel('Count')
#plt.ylim(0, max(distances))
plt.ylim(0, numberOfDistances / 10)
plt.title('Point distances with distance function ' + distanceFunctionName + ' (k = ' + str(numberOfDimensions) + ', n = ' + str(numberOfPoints) + ')')
plt.grid(True)
plt.show()