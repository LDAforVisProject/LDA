'''
Created on 24.10.2014

@author: RM
'''

from Point import Point
import numpy as np
import matplotlib.pyplot as plt
import math

# Number of points
numberOfPoints      = 20
# Number of distances between numberOfPoints points (Gaussian sum formula)
numberOfDistances   = ( ( (numberOfPoints - 1) * (numberOfPoints - 1) + numberOfPoints - 1) / 2)
# Number of dimensions
numberOfDimensions  = 10

# Coordinate space base ('cube')
shape = 'cube'
# Distance function ('L2', 'Bhattacharyya', 'Hellinger', 'KullbackLeibler', 'JensenShannon')
distanceFunctionName = 'JensenShannon'

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
