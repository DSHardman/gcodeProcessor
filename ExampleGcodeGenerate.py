import numpy as np
from ProcessCommands import processgcode
from ExtractCommands import extractgcode


extractgcode('string', 'extractedstring')
print('Data Extracted')
printcommands = np.load('extractedstring.npy')
processgcode('processedstring', printcommands)
print('Data Processed')
