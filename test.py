# temp file for testing stuff
import numpy as np
layerData = [9,10,9]
rows, cols = 3,3
a = np.full((rows,cols), 0.5)#.reshape(-1,1)


a[0][0] = 0
a[0][1] = 0
a[1][2] = 0
a[1][1] = 0



zeros = np.where(a==0)
r = np.random.randint(len(zeros[0]))
z1 = zeros[0][r]
z2 = zeros[1][r]
a[z1,z2] = 1
print(a)