'''
Created on 30.05.2015

@author: RM
'''

from optparse import OptionParser


class SimplifiedConfiguration:
    '''
    Class for argument parsing and storing configuration data.
    '''
    
    # Constructor
    def __init__(self):
        # Declare attributes
        self.optionParser   = OptionParser()
        self.mode           = ""
        self.passes         = 0;
        self.dbPath         = "";
        self.inputPath      = "";
        self.outputPath     = "";
        
        self.k              = 0;
        self.alpha          = 0;
        self.eta            = 0;
        
        self.update_every   = 5;
        self.chunksize      = 100;
        
        # Configure options
        self.configureOptions()
        
    def configureOptions(self):
        self.optionParser.add_option("-p", "--passes", dest="passes", type="int", help="Number of passes. Default to 10.")
        self.optionParser.add_option("-m", "--mode", dest="mode", type="string", help="Mode. Use 'pre' for data preprocessing, '" + 
                                     "or 'sample' to sample parameter space.")
        self.optionParser.add_option("-i", "--inputPath", dest="inputPath", type="string", help="Path to file storing all LDAConfigurations to be generated.")
        self.optionParser.add_option("-o", "--outputPath", dest="outputPath", type="string", help="Path under which the final topic data files will be stored.")
        
    def parseOptions(self):
        (options, args)         = self.optionParser.parse_args()
        
        self.mode               = options.mode
        self.passes             = options.passes
        self.inputPath          = options.inputPath
        self.outputPath         = options.outputPath
        self.dbPath             = options.outputPath
        
    def toString(self):
        # For now: Consider only k, eta and alpha.
        return "k=" + str(self.k) + "|eta=" + str(self.eta) + "|alpha=" + str(self.alpha)