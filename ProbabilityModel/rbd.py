''' Generate a list of Random Binary Decision '''
import numpy as np
import random

def generate_binDecision(N):
    l = np.zeros(N)
    for i in xrange(N):
        l[i] = bool(random.getrandbits(1))
    return l