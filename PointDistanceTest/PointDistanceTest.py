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
import time


# ------------------------------------------------------------------------------------
# Functions used in script
# ------------------------------------------------------------------------------------

'''
Prepare option parser.
@return Configured option parser.
'''        
def createConfiguredOptionParser():
    parser = OptionParser()
    parser.add_option("-k", "--k_dimensions", dest="k", type="int", help="Number of dimensions.")
    parser.add_option("-n", "--n_points", dest="n", type="int", help="Number of points.")
    parser.add_option("-t", "--timeTest", action="store_false", dest="t", default=True, help="Enable test mode (plot closes immediately.")
    
    return parser

'''
Calculate distances.
@param points Point data, including coordinates.
@param distances Calculated distances are stored here.
'''
def calculateDistances(points, distances, distanceFunctionName):
    currentDistanceIndex = 0
    for outerIndex in np.arange(0, numberOfPoints - 1):
    #print outerIndex
        for innerIndex in np.arange(outerIndex + 1, numberOfPoints):
            distances[currentDistanceIndex] =  points[outerIndex].calculateDistance(points[innerIndex], distanceFunctionName)
            currentDistanceIndex = currentDistanceIndex + 1 



# ------------------------------------------------------------------------------------
# Point distance function (start of script)
# ------------------------------------------------------------------------------------

# Start timer
timeStart       = time.time()
timeEnd         = 0
calculationTime = 0
plotTime        = 0

# Get logger
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------
# Init option parser
# ------------------------------------------------------------------------------------

parser = createConfiguredOptionParser() 

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
# Determine whether to enable test mode
if options.t == True:
    logger.info("Time test mode disabled by default).")
    blockPlot = True
else:
    logger.info("Time test mode enabled.")
    blockPlot = False
        
# Number of distances between numberOfPoints points (Gaussian sum formula)
numberOfDistances = ( ( numberOfPoints * (numberOfPoints - 1) ) / 2)

# Coordinate space base ('cube')
shape = 'cube'
# Distance function ('L2', 'Bhattacharyya', 'Hellinger', 'KullbackLeibler', 'JensenShannon')
distanceFunctionNames = ['L2', 'Bhattacharyya', 'Hellinger', 'JensenShannon']

# ------------------------------------------------------------------------------------
# Prepare data, calculate distances
# ------------------------------------------------------------------------------------

# Data
points = [Point(dimension=numberOfDimensions, base=shape) for x in range(numberOfPoints)]
distances = [0] * numberOfDistances 

# ------------------------------------------------------------------------------------
# Plot data
# ------------------------------------------------------------------------------------

# Instantiate new figure
fig = plt.figure()
plt.xlabel('\nDistance (in percent of ' + r'$\sqrt{k} = $' + str(math.sqrt(numberOfDimensions)) + ')')
plt.ylabel('Frequency (in percent of number of distances)\n\n')
fig.patch.set_alpha(0.0)
plt.hold(False)
                    
#fig.tight_layout()
plt.xticks([])
plt.yticks([])

# Define plot limits
#x_min = -math.sqrt(numberOfDimensions)
#x_max = math.sqrt(numberOfDimensions) * 4
x_min = 0
x_max = math.sqrt(numberOfDimensions)
y_min = 0
y_max = numberOfDistances / 10

# Create x-ticks (sqrt(dim) ~ 100%)
xAxis_translationFactor = 100 / math.sqrt(numberOfDimensions)
yAxis_translationFactor = 100.0 / numberOfDistances

x_ticks_range = np.arange(x_min, x_max, 0.25, dtype=np.float)
x_ticks = [int((x * xAxis_translationFactor)) for x in x_ticks_range]

y_ticks_range = np.arange(y_min, y_max, (y_max - y_min) / 10, dtype=np.float)
y_ticks = [round((y * yAxis_translationFactor), 2) for y in y_ticks_range]

# Draw plots
currentSubplotIndex = 1
plotTimeStart = time.time()
for distanceFunctionName in distanceFunctionNames:
    # Add new Subplot
    ax = fig.add_subplot(2, 2, currentSubplotIndex)
    # Set title
    ax.set_title(distanceFunctionName, fontsize=11)
    
    # Calculate distances
    calculationTimeStart = time.time()
    calculateDistances(points, distances, distanceFunctionName)
    calculationTime = calculationTime + time.time() - calculationTimeStart
    
    # https://stackoverflow.com/questions/11750276/matplotlib-how-to-convert-a-histogram-to-a-discrete-probability-mass-function
    #distancesNormalized = np.histogram(distances,bins=50,normed=0)[0]/float(len(distances))
    n, bins, patches = ax.hist(distances, bins=50, normed=0, facecolor='g', alpha=0.75)
    
    # Mark 0 and sqrt(numberOfDimensions)
    ax.axvline(x=0, ymin=0, ymax = 100, linewidth=3, color='r')
    ax.axvline(x=math.sqrt(numberOfDimensions), ymin=0, ymax = 100, linewidth=3, color='r')
    
    # Set tick labels and range/axis limits
    ax.set_ylim(y_min, y_max)
    ax.set_xlim(x_min, x_max)
    
    #ax.set_xticks(x_ticks_range, x_ticks)
    plt.xticks(x_ticks_range, x_ticks, fontsize=8)
    plt.yticks(y_ticks_range, y_ticks, fontsize=8)
    
    ax.grid(True)
    
    # Increment index
    currentSubplotIndex = currentSubplotIndex + 1

plt.suptitle('Point distances with k = ' + str(numberOfDimensions) + ', n = ' + str(numberOfPoints), fontsize=15)
plt.show(block=blockPlot)

plotTime = time.time() - plotTimeStart   - calculationTime

# ------------------------------------------------------------------------------------
# Print measured execution time(s)
# ------------------------------------------------------------------------------------

timeEnd = time.time()
logger.info("Elapsed time in total: " + str(timeEnd - timeStart) + " seconds.")
logger.info("    Time needed for calculation of distances: " + str(calculationTime) + " seconds.")
logger.info("    Time needed for plotting: " + str(plotTime) + " seconds.")