import numpy as np
from ProcessCommands import processgcode
from ExtractCommands import extractgcode


extractgcode('benchy', 'extractedbenchy')
print('Data Extracted')
printcommands = np.load('extractedbenchy.npy')
processgcode('processedbenchy', printcommands, [2.5, 5], 3, 5)
print('Data Processed')
