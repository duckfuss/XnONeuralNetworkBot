import random
import numpy as np
import math as maths
# numpy setup
np.set_printoptions(suppress=True,linewidth=np.nan)
np.random.seed(1)
random.seed(1)

class Network():
    def __init__(self, layerData, turn) -> None:
        self.layerData = layerData # [no. neurons in layer 1, no.neurons in layer 2,...]
        self.layersList = [] # list of objects 
        self.turn = turn # 1 = X, 2 = O
        
    def generateNetwork(self):
        for i in range(1,len(self.layerData)): # don't include input layer
            self.layersList.append(Layer(self.layerData[i-1], self.layerData[i]))

    def trainNetwork(self, boardHist, winner, verbose=False):
        '''
        Trains the network from the boardHist(ory)
        Current rules (applied in a decaying fashion as per delta):
        - if win, desired state = array of (1-delta) with a "delta" on "correct choice"
        - if loss, desired state = array of "delta" with a (1-delta) on "wrong choice"
        - if draw, desired state = same as win
        '''
        rows, cols = len(boardHist[0][0]), len(boardHist[0][0][0])
        
        # FEED FORWARDS
        for i in range(self.turn-1, len(boardHist), 2):
            # loop over every other boardstate, (state 1 always goes first)
            boardState = boardHist[i][0]    # array of board state
            move = boardHist[i][1]          # tuple (row,col)
            delta = 0.5*(maths.exp(-0.2*((i-len(boardHist))/2))+0.5)
            # see https://www.desmos.com/calculator/owfq7vaas8
            
            compressed = np.divide(boardState, 2)
            output = self.compute(compressed).reshape(rows,cols)

            if winner == self.turn:
                desired = np.full((rows,cols), 1 - delta)
                desired[move[0]][move[1]] = delta
            elif winner != 0:
                desired = np.full((rows,cols), delta)
                desired[move[0]][move[1]] = 1 - delta
            else: # draw/timeout
                #desired = np.random.rand(rows,cols)
                desired = np.full((rows,cols), 1-delta)
                desired[move[0]][move[1]] = delta
            if verbose:
                print("\n\nboardState: \n", boardState)
                print("output: \n", output)
                print("desired: \n", desired)
                print("delta:", delta, " turn:", self.turn, " move", move)

            # calculate cost
            #  -> cost = self.cost(output,desired)
            layerCost = 2*(output-desired)
            layerCost = np.reshape(layerCost, (-1,1))
            for layer in self.layersList[::-1]:
                # loops through a shallow copy of reversed list
                layerCost = layer.backpropogateLayer(layerCost)

        for layer in self.layersList:
            # apply the changes
            layer.gradDesc(len(boardHist), rate=3)

    def compute(self, inputs, verbose=False):
        inputs = (inputs.flatten().reshape(-1,1))/2
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