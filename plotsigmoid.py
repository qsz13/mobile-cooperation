import matplotlib.pyplot as plt
import numpy as np
import math

def sigmoid(x):
    a = []
    for item in x:
        a.append(1/(1+math.exp(-15+item)))
    return a

x = np.arange(0., 10., 0.2)
sig = sigmoid(x)
plt.plot(x,sig)
plt.show()