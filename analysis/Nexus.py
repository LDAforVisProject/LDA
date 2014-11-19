'''
Created on 19.11.2014

@author: RM
'''

import os, csv
import logging
from core import CorporaReader, TextProcessor
from utils.Configuration import Configuration

# --------------------------------
# Get file location
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print __location__

# Set up logger
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# --------------------------------

# Parse arguments
configuration = Configuration()
configuration.parseOptions()

if configuration.mode == "sample":
    alphaValues = [0.1, 0.5, 1, 5, 10]
    
    for alpha in alphaValues:
        print alpha
        suffix = ""
    
elif configuration.mode == "pre":
    CorporaReader.readCorpora()
    TextProcessor.processText()
        