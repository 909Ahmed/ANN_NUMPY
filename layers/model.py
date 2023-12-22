import numpy as np
import math
from sigmoid import der_sigmoid

class Model():

    def __init__(self, input_layer, output_layer):
        
        self.input_layer = input_layer
        self.output_layer = output_layer
        self.layers = self.get_layers()


    def forward_pass (self, sample):

        pre_layer = self.input_layer
        pre_layer.output = sample

        for layer in self.layers:
            layer.update(pre_layer.output)
            pre_layer = layer

    def get_embed (self, logits):
        temp = [0] * 10
        temp[logits] = 1
        return temp

    def softmax(self, ):
        
        sum = 0
        res = []
        
        for i in range(len(self.output_layer.output)):
            out = self.output_layer.output[i]
            exp_out = math.exp(out)
            sum += exp_out

        for i in range(len(self.output_layer.output)):
            out = self.output_layer.output[i]
            res.append(math.exp(out) / sum)
        
        return res

    def backward_pass(self, logits):
        
        logits = self.get_embed (logits)
        self.softmax()
        grad_mat = [x - y for x, y in zip(self.output_layer.output, logits)]
        der_Z = [der_sigmoid(x) for x in self.output_layer.values]

        del_curr = [x * y for x, y in zip(grad_mat, der_Z)]

        curr_layer = self.output_layer

        while curr_layer != self.input_layer:
            
            del_curr = self.calc_delta(curr_layer, del_curr)

            lr = 0.001
            for i in range(len(curr_layer.layer)):
                
                neuron = curr_layer.layer[i]
                
                for j in range(len(neuron.weights)):

                    delta = curr_layer.pre_layer.output[j] * del_curr[i]
                    neuron.weights[j] = neuron.weights[j] - lr * delta

            for j in range(len(del_curr)):
                
                neuron = curr_layer.layer[i]
                neuron.bias = neuron.bias - lr * del_curr[i]

            curr_layer = curr_layer.pre_layer



    def fit (self, X, Y, epochs):
        for _ in range(epochs):
            for i in range(len(X)):

                self.forward_pass(X)
                self.backward_pass(Y)



    def get_layers (self):
        
        layers = []
        curr_layer = self.output_layer
        
        while curr_layer != self.input_layer:

            layers.append(curr_layer)
            curr_layer = curr_layer.pre_layer
        
        return layers[::-1]
    

    def calc_delta(self, curr_layer, delta_post):

        mat = [neuron.weights for neuron in curr_layer.layer]
        mat = np.array(mat)
        mat = mat.transpose()
        
        der_Z = [der_sigmoid(x) for x in curr_layer.values]
        
        dot = np.dot(mat, delta_post)
        del_curr = [x * y for x, y in zip(dot, der_Z)]

        return del_curr