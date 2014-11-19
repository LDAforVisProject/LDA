'''
Created on 08.10.2014

@author: RM
'''

import csv
import codecs

# Source: https://stackoverflow.com/questions/904041/reading-a-utf8-csv-file-with-python
class UnicodeCSVHandler(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        classdocs
        '''
        
    def read(self, utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect=csv.excel, delimiter='\t', **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]
                    