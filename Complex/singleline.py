import numpy as np
import matplotlib.pyplot as plt
import neurolab as nl

input_data = np.loadtxt("./neural_simple.txt")
data = input_data[:, 0:2]
labels = input_data[:, 2:]

dim1_min, dim1_max = data[:,0].min(), data[:,0].max()
dim2_min, dim2_max = data[:,1].min(), data[:,1].max()

nn_output_layer = labels.shape[1]
dim1 = [dim1_min, dim1_max]
dim2 = [dim2_min, dim2_max]
neural_net = nl.net.newp([dim1, dim2], nn_output_layer)

error = neural_net.train(data, labels, epochs = 200, show = 2, lr = 0.0001)

plt.figure()
plt.plot(error)
plt.xlabel('Number of epochs')
plt.ylabel('Training error')
plt.title('Training error progress')
plt.grid()
plt.show()
