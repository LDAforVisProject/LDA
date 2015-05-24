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
        self.eta            = 0
        self.mode           = ""
        self.samplingMode   = ""
        self.passes         = 0;
        self.outputPath     = "";
        
        self.update_every   = 5;
        self.chunksize      = 100;
        
        # Configure options
        self.configureOptions()
        
    def configureOptions(self):
        self.optionParser.add_option("-k", "--k_clusters", dest="k", type="int", help="Number of clusters.")
        self.optionParser.add_option("-a", "--alpha", dest="alpha", type="float", help="Symmetric alpha value.")
        self.optionParser.add_option("-e", "--eta", dest="eta", type="float", help="Symmetric eta value.")
        self.optionParser.add_option("-p", "--passes", dest="passes", type="int", help="Number of passes. Default to 10.")
        self.optionParser.add_option("-x", "--exists", dest="useExistingData", action='store_true', help="Use existing data. Don't generate topic data using LDA preprocessing on data found in /core/data/sampling/.")
        self.optionParser.add_option("-m", "--mode", dest="mode", type="string", help="Mode. Use 'pre' for data preprocessing, '" + 
                                     "'lda' for a single LDA run, 'sample' to sample parameter space, 'pre' to preprocess data.")
        self.optionParser.add_option("-s", "--samplingMode", dest="samplingMode", type="string", help="Sampling Mode. Ignored if mode doesn't equal " + 
                                     "'sample'. Possiblities: 'cartesic', 'random', 'hypercube'.")
        self.optionParser.add_option("-o", "--outputPath", dest="outputPath", type="string", help="Path under which the final topic data files will be stored.")
        
    def parseOptions(self):
        (options, args)         = self.optionParser.parse_args()
        self.k                  = options.k
        self.alpha              = options.alpha
        self.eta                = options.eta
        self.mode               = options.mode
        self.samplingMode       = options.samplingMode
        self.passes             = options.passes
        self.useExistingData    = options.useExistingData
        self.outputPath         = options.outputPath
        
    def toString(self):
        # For now: Consider only k, eta and alpha.
        return "k=" + str(self.k) + "|eta=" + str(self.eta) + "|alpha=" + str(self.alpha)