# temp file for testing stuff
import numpy as np
layerData = [9,10,9]
rows, cols = 3,2
a = np.full((rows,cols), 0.5)#.reshape(-1,1)
print(a)
a = np.reshape(a, (-1,1))
print(a)