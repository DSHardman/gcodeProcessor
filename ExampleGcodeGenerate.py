import numpy as np
from ProcessCommands import processgcode
from ExtractCommands import extractgcode


extractgcode('cube', 'extractedcube')
print('Data Extracted')
printcommands = np.load('extractedcube.npy')
processgcode('processedcube', printcommands, kd=[6.0, 6.5], speedfactor=1.5)
print('Data Processed')
