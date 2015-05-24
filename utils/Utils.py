'''
Created on 20.11.2014

@author: RM
'''
import logging

def initLogging():
    # Set up logger
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # --------------------------------
    
    # Get logger
    logger = logging.getLogger(__name__)
    
    return logger