import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


'''
A few random functions for plotting surfaces and others


'''

gravity = 9.81

def insaneoStyle(x, y):
    return (x*y)**3 + x**3 - y**3 + (y-2)**2 - (x+2)**2 + 3*x - 2*x + 7

def frick(x, y):
    return ((x*y)**4 - np.arctan((y-np.pi/x))) + 14 * y**4 + x/np.exp(1)

def frack(x, y):
    return  np.sin(x)  *  np.cos(y)

def kinematic(theta, v0):
    t = np.linspace(0, 2 * v0 * np.sin(theta) / gravity, 100)

    x = v0 * np.cos(theta) * t
    y = np.sin(theta) * t - .5 * gravity * t**2

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()

def rosenbrock(x, y):
    return (1 - x)**2 + 100*(y - x**2)**2

def basic(x, y):
    return x**2 + y**2

def randoMutiti(x, y):
    return (x-2)**2 +(y+2)**2 + 2

def rastrigin(x, y):
    return 20 + (x**2 + 10 * np.cos(2*np.pi * x)) + (y**2 + 10 * np.cos(2*np.pi * y))

def plottasurface(funky, X=None, Y=None, a=None, b=None, c=None, theta=None, xlbound=-10, xubound=10, ylbound=-10, yubound=10, reso=1000):
    if X is None and Y is None:
        X = np.linspace(xlbound, xubound, reso)
        Y = np.linspace(ylbound,yubound, reso)

    x, y = np.meshgrid(X, Y)

    z = funky(x, y)

    fig = plt.figure() # makes new figure object that contains all information about figure including things like legend labels etc
    ax = fig.add_subplot(projection='3d') # get current axes from figure object and make 3d plot
    ax.plot_surface(x,y,z, cmap='plasma') # plot a surface based on xyz, x and y are given and z is calculated from them
    plt.show()

