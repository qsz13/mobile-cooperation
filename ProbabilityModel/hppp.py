''' Generate homogeneous Poisson Point Process in a Circle '''
import numpy as np

LAMBDA = 2 # the coefficient
PI = np.pi # or put PI = 3.14

# def generate_PPP(N): # N: number of nodes
    # n = np.random.poisson(N) * LAMBDA # size of the circle C
    # r = np.sqrt(n/PI) # radius of the circle C
    # x = np.zeros(N) # Cartesian Coordinate x
    # y = np.zeros(N) # Cartesian Coordinate y
    # u_1 = np.random.uniform(0.0, 1.0, N) # generate n uniformly distributed points
    # u_2 = np.random.uniform(0.0, 1.0, N) # generate n uniformly distributed points
    # for i in xrange(N):
    #     angle = 2 * PI * u_2[i]
    #     radii = r * (np.sqrt(u_1[i]))
    #     x[i] = radii * np.cos(angle)
    #     y[i] = radii * np.sin(angle)
    # return [x, y, r]



def cirrdnPJ(x1, y1, rc):

    a = 2*np.pi*np.random.uniform(0.0, 1.0, len(x1))
    r = np.sqrt(np.random.uniform(0.0, 1.0, len(x1)))
    x = (rc*r)*np.cos(a)+x1
    y = (rc*r)*np.sin(a)+y1
    data = np.array([x,y])
    return data.T


""" Plotting """
"""
import matplotlib.pyplot as plt
[x, y, r] = generate_PPP(100)
print r
print len(x)
fig = plt.gcf()
ax = fig.gca()
plt.xlim(-r, r)
plt.ylim(-r, r)
c = plt.Circle((0, 0), radius=r, color='r', linewidth=1, fill=False)
ax.add_artist(c)
plt.plot(x,y,'bo')
plt.show()
"""