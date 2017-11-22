"""Train an MLP on MNIST using K-FAC.
This MLP fits a 3-layer, tanh-activated MLP on MNIST using K-FAC. After
200 iterations, this should reach ~99% accuracy on the training set and
~98% on the testing set.
"""
from K_FAC import KFAC
import autograd.numpy as np
import autograd.numpy.random as npr
from autograd.scipy.misc import logsumexp
from data import load_mnist

# This K-FAC implementation is easy to use, you don't need to construct the neural network on your own. Instead, just
# specify the activation types and sizes of layers, and the optimizer will construct the neural network inside.
# (Unlike other optimizers, K-FAC explores the structure of the neural network, that's why layer types and sizes are needed)


# This implementation supports initial weights in the following shape:[([W1],[b1]),([W2],[b2])...([Wl],[bl])],
# which can be easily generated by the following function.
def init_random_params(scale, layer_sizes, rs=npr.RandomState(0)):
    """Build a list of (weights, biases) tuples,
       one for each layer in the net."""
    return [(scale * rs.randn(m, n),  # weight matrix
             scale * rs.randn(n))  # bias vector
            for m, n in zip(layer_sizes[:-1], layer_sizes[1:])]

# the following three functions are used for printing the results as the training goes, not needed for the optimizer
def neural_net_predict(params, inputs):
    """A deep neural network for classification.
       params is a list of (weights, bias) tuples.
       inputs is an (N x D) matrix.
       returns normalized class log-probabilities,
       and preactivations of the last layer.

       you don't need to create it if you are not interested 
       in seeing the printed results.
       """
    for W, b in params:
        outputs = np.dot(inputs, W) + b
        inputs = np.tanh(outputs)
    return outputs - logsumexp(outputs, axis=1, keepdims=True)

def accuracy(params, inputs, targets):
    """
    Evaluate accuracy of prediction given current parameters
    params: current parameters
    inputs: training inputs or testing inputs
    targets: targets corresponding to training inputs or testing inputs
    """
    target_class = np.argmax(targets, axis=1)
    predicted_class = np.argmax(neural_net_predict(params, inputs), axis=1)
    return np.mean(predicted_class == target_class)

def show_results(i, params,minibatch_size):
    """
    Print the results every 100 iterations
    """
    if i % 100 == 0:
        train_acc = accuracy(params, train_inputs, train_targets)
        test_acc = accuracy(params, testing_inputs, testing_targets)
        print("{:15}|{:20}|{:20}|{:20}".format(i, minibatch_size, train_acc, test_acc))


# Model parameters
layer_sizes = [784, 200, 100, 10] # the first number 784 is the dimension of a single input
layer_types = ['tanh', 'tanh', 'softmax']     
L2_reg = 1.0                    
param_scale = 0.1 # parameter for generating initial variables
init_params = init_random_params(param_scale, layer_sizes)
num_iter = 1000
print("Loading training data...")
N, train_images, train_labels, test_images, test_labels = load_mnist() # loading data
train_inputs = train_images         # all data need to be in the shape: num_of_samples * dimension.
train_targets = train_labels
testing_inputs = test_images
testing_targets = test_labels
train_with_increasing_batch_size = True # if False, then will train with fixed batch size of 256.

print('Results from KFAC')
print( "   Iterations  |    Minibatch size  |    Train accuracy  |    Test accuracy    ")

# The initial lambda value is the only parameter you need to adjust for now. This adjustment will be automated in the future.
# The choice of initial lambda is problem-dependent and can be adjusted based on behavior of the first few iterations.
initlambda = 1   #  1 is more appropriate for classification nets. For an autoencoder, you may want to try initlambda = 150

optimized_params = KFAC(num_iter, init_params, initlambda, layer_sizes,layer_types, train_inputs, train_targets, testing_inputs, testing_targets, train_with_increasing_batch_size, L2_reg = 1, callback = show_results)
