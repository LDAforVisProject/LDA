'''
Created on 19.11.2014

@author: RM
'''

from optparse import OptionParser

class Configuration():
    '''
    Class for argument parsing and storing configuration data.
    '''
    
    # Constructor
    def __init__(self):
        # Declare attributes
        self.optionParser   = OptionParser()
        self.k              = 0
        self.alpha          = 0
        self.mode           = ""
        
        # Configure options
        self.configureOptions()
        
    def configureOptions(self):
        self.optionParser.add_option("-k", "--k_clusters", dest="k", type="int", help="Number of clusters.")
        self.optionParser.add_option("-a", "--alpha", dest="alpha", type="float", help="Symmetric alpha value.")
        self.optionParser.add_option("-p", "--passes", dest="passes", type="int", help="Number of passes. Default to 10.")
        self.optionParser.add_option("-e", "--exists", dest="useExistingData", action='store_true', help="Use existing data. Don't run LDA on data found in /core/data/sampling/.")
        self.optionParser.add_option("-m", "--mode", dest="mode", type="string", help="Mode. Use 'pre' for data preprocessing, '" + 
                                     "'lda' for a single LDA run, sample' for a sampling of preprocessed data.")
        
    def parseOptions(self):
        (options, args) = self.optionParser.parse_args()
        self.k = options.k
        self.alpha = options.alpha
        self.mode = options.mode
        self.passes = options.passes
        self.useExistingData = options.useExistingData