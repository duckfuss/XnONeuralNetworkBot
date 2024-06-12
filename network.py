import random
import numpy as np
# numpy setup
np.set_printoptions(suppress=True,linewidth=np.nan)
np.random.seed(5)
random.seed(5)

class Network():
    def __init__(self, layerData) -> None:
        self.layerData = layerData # [no. neurons in layer 1, no.neurons in layer 2,...]
        self.layersList = [] # list of objects 
        
    def generateNetwork(self):
        for i in range(1,len(self.layerData)): # don't include input layer
            self.layersList.append(Layer(self.layerData[i-1], self.layerData[i]))

    def trainNetwork(self, samples):
        '''trains the network with "samples" no. examples using data from dataType'''
        # FEED FORWARDS
        trainingIndex = random.sample(range(0,len(self.tData.trainIm)), samples)
        for i in trainingIndex:
            # calculate desired outputs
            desired = np.zeros(self.layerData[-1]).reshape(-1,1)
            desired[self.tData.trainLab[i]] = 1
            # calculate actual output
            output = self.compute(i)
            # calculate cost
            #  -> cost = self.cost(output,desired)
            layerCost = 2*(output-desired)
            for layer in self.layersList[::-1]:
                # loops through a shallow copy of reversed list
                layerCost = layer.backpropogateLayer(layerCost)
        for layer in self.layersList:
            layer.gradDesc(samples)

    def compute(self, inputIndex, verbose=False):
        inputs = (self.tData.trainIm[inputIndex].flatten().reshape(-1,1))/256
        for layer in self.layersList:
            if verbose: print("\n\nLayer no: ", self.layersList.index(layer))
            inputs = layer.computeOutput(inputs, verbose)
        return inputs # final looped input is the output

    def cost(self, actual, desired, verbose=False):
        diff = actual - desired
        if verbose:
            print("\nactual: \n", actual, "\ndesired:\n", desired)
            print("\ndifference:\n",diff)
        return np.vdot(diff,diff)

class Layer():
    def __init__(self, inputSize, outputSize) -> None:
        self.weights = np.random.normal(0,1, size=(outputSize, inputSize))
        self.biases = np.random.normal(0,1, size=(outputSize, 1))
        self.inputs = []
        self.outputs = []
        self.bufferedAdjust = [0,0] # [weightAdj, biasAdj]
    def computeOutput(self, inputs, verbose=False):
        '''
        Input numpy a 1D array
        Though inputs, weighted, biased and output arrays are 1xn matricies, and not nx1,
        nump.matmul treats them as nx1 so all is ok ;) - this may be false
        '''
        self.inputs = inputs
        weighted = np.matmul(self.weights, self.inputs)
        weightedBiased = np.add(weighted, self.biases)
        self.outputs = sigmoid(weightedBiased)
        if verbose:
            print("\ninputs:\n",self.inputs)
            print("SUM of inputs:", np.sum(self.inputs))
            print("weights: \n", self.weights)
            print("SUM of weights:", np.sum(self.weights))
            print("biases:\n",self.biases)
            print("weighted:\n",weighted)
            print("weightedBiased:\n",weightedBiased)
            print("output:\n",self.outputs)
        return self.outputs
    
    def backpropogateLayer(self, layerCost):
        backProp = self.backpropAdjust(layerCost) 
        self.bufferedAdjust[0] += backProp[0]
        self.bufferedAdjust[1] += backProp[1]
        return backProp[2] # cost of the prev layer

    def gradDesc(self, sampleSize, rate=3):
        self.weights -= (rate/sampleSize) * self.bufferedAdjust[0]
        self.biases -= (rate/sampleSize) * self.bufferedAdjust[1]
        self.bufferedAdjust = [0,0]

    def backpropAdjust(self, cost):
        '''
        Finds the derivatives for weights, biases, and prev layer

        Notation:
        w = weights     ----↘︎
        p = prev result ----→ z = wp+b  ---> a = sig(z) ----> C = cost func
        b = bias        ----↗︎
        '''
        dz_dw = self.inputs
        da_dz = self.outputs * (1-self.outputs) # this is derivative of sig(z)
        dC_da = cost
        
        dC_dw = np.outer((da_dz * dC_da), dz_dw) # "*" gives the hadamard product
        dC_db = 1 * da_dz * dC_da
        dC_dp = np.matmul(self.weights.T, (da_dz * dC_da))
        return [dC_dw, dC_db, dC_dp]

def sigmoid(x):
    '''transforms any arbritrary x value into a 0-1 output value'''
    return 1/(1+np.exp(-x))
def dsigmoid(x):
    return sigmoid(x) * (1-sigmoid(x))

