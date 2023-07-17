import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D

''' 
Key:

m = Mandlebrot set

jr = Julia set from randon starting position or enter j + (1-9)
to pick from preselected starting coordinates ex j1

l = lorenz-96 system

b = barnsley fern (broken)

circle = will draw a circle (over 40 hours of optimization went into this function)

pe = visualization of positional embeddings in transformers

q = quit
'''

def mandy(resolution=10000):
    xMin, xMax = (-1.80, 1)
    yMin, yMax = (-1.5, 1.25)

    xval = np.linspace(xMin, xMax, resolution)
    yval = np.linspace(yMin, yMax, resolution)

    x, y = np.meshgrid(xval, yval) # array of all xy
    c = x + complex(0, 1) * y # array of c for all possible xy - 1j*(i) is to avoid getting error for multiplying sequence by complex

    z = np.zeros_like(c) #makes arrary of zeros same shape and data type as c
    colors = np.zeros((resolution, resolution))

    for i in range(100):
        z = z**2 + c
        escaped = np.abs(z) > 2 #boolean array of same shape and size of z
        colors[escaped] = i #color at escaped = number of iterations it took to escape = i

    plt.figure(figsize=(10,10))
    plt.imshow(colors, cmap='plasma')
    plt.show()

def jules(resolution, maxepoch, threshold, c): #z should be tuple of (a,b)
    xMin, xMax = -1.5, 1.5
    yMin, yMax = -1.5, 1.5

    x = np.linspace(xMin, xMax, resolution)
    y = np.linspace(yMin, yMax, resolution)

    a, bi = tuple(c)
    c = complex(a,bi)

    julia = np.zeros((resolution, resolution))

    for i in range(resolution):
        for j in range(resolution):
            z = complex(x[i], y[j])
            for k in range(maxepoch):
                z = z ** 2 + c
                if abs(z) > threshold:
                    julia[i,j] = k
                    break
                else:
                    julia[i, j] = maxepoch

    plt.imshow(julia, cmap='plasma')

    plt.show()

def juliesStarters(req):
    try:
        req = int(req)
    except:
        starter = (np.random.uniform(-1,1),np.random.uniform(-1,1))
    pairs = [(-0.4,0.6), (0.285,0.01), (0.3,0.01), (-0.835,0.2321), (-0.70176, 0.3842), (-0.8, 0.156), (-0.4, 0.6), (0.4, 0.4), (0.4, 0.59), (-.778, -.132)]

    if req == 'r':
        starter = starter
    else:
        starter  = pairs[req]
    return starter

def lorenz(t, s, sigma, rho, beta):
    dxdt = sigma * (s[1] - s[0])
    dydt = rho * s[0] - s[1] - s[0] * s[2]
    dzdt = s[0] * s[1] - beta * s[2]
    return [dxdt, dydt, dzdt]

def lennySalva(resolution):
    starting = [1,1,1]
    sigma = 10
    rho = 28
    beta = 8/3

    timeSpan = [0, 50]
    timeline = np.linspace(timeSpan[0], timeSpan[1], resolution)

    solution = solve_ivp(lorenz, timeSpan, starting, t_eval=timeline, args=(sigma, rho, beta))
    #solution.y should be 3xlen(t_eval) array where each of the 3 represent x,y,z
    print(solution, '\n', solution.y)

    fig = plt.figure()
    graph = fig.add_subplot(111, projection='3d') #gca = get current axes and specifies to make 3d plot
    graph.plot(solution.y[0], solution.y[1], solution.y[2], color='purple')
    plt.show()

def circy():
    i = np.linspace(0, 2*np.pi, 1000)

    x = np.cos(i)
    y = np.sin(i)

    plt.plot(x, y)
    plt.axis('equal')
    plt.show()

def sin():
    x = np.linspace(0, 6*np.pi, 1000)
    y = np.sin(x)

    plt.plot(x, y)
    plt.show()

def barnsley(n=5000):
    f1 = lambda x, y: (0, 0.16 * y)
    f2 = lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6)
    f3 = lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6)
    f4 = lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)

    functions = [f1, f2, f3, f4]
   # j = functions[2](8,9)
  #  print(j)

    x = np.zeros(n)
    y = np.zeros(n)

    width, height = 600, 600
    points = np.zeros((width, height))

    for i in range(n-1):
        xval = x[i]
        yval = y[i]
        print("I IS HERE = ", i)
        lamma = np.random.randint(1, 5)
        print("LAMMA", lamma)
        if lamma == 1:
            xx, yy = functions[0](x[i], y[i])
            print('f1 ===== ')
        elif lamma == 2:
            xx, yy = functions[1]( x[i], y[i])
            print('f2 ==== ')
        elif lamma == 3:
            xx, yy = functions[2](x[i], y[i])
            print( 'f3 ==== ')
        else:
            print('else')
            xx, yy = functions[3](x[i], y[i])
            print(xx, yy)

        print("XXYY ==== ", xx, yy)

    print(points)
    plt.imshow(points[::-1, :])
    plt.show()

'''
Positional Encoding

PE(pos, 2i) = sin(10000^(2i/d)
PE(pos, 2i+1) = cos(10000^(2i/d)

These functions are used to give each vector in the input to a language transformer a unique position as to capture
context of each word
'''

def posEncoding(length=2048, depth=512):
    depth = depth/2

    positions = np.arange(length)[:, np.newaxis] #1d of length lenth which has axis added to it to become size (length, 1)
    depths = np.arange(depth)[np.newaxis, :] / depth #same but (1, depth) also takes care of (2i/d) to make next line easier

    angleRates =  1/(10000**depths) #(1, depth)
    angleRadians = positions * angleRates

    encoding = np.concatenate([np.sin(angleRadians), np.cos(angleRadians)], axis=-1)
    print(encoding.shape)

    plt.pcolormesh(encoding.T, cmap='RdBu') # .T = transpose, aka: swap columns and rows
    plt.colorbar()
    plt.ylabel('Depth')
    plt.xlabel('Position')
    plt.show()

def terms():
    while True:
        fucky = input('Command or enter "help" to see a list of commands ===> ')
        if fucky.startswith('j'):
            order = fucky.strip('j')
            starter = juliesStarters(order)
            jules(1000, 100, 4, starter)
            fucky = None
        elif fucky.startswith('m'):
            mandy()
        elif fucky.startswith('l'):
            reso = fucky.strip('l')
            reso = int(reso)
            lennySalva(reso)
        elif fucky.startswith('b'):
            barnsley()
        elif fucky == 'circle':
            circy()
        elif fucky == 'pe':
            posEncoding()
        elif fucky == 'q':
            break
        elif fucky == "help":
            print(key)
        else:
            try:
                exec(fucky)
            except:
                print('Kill Yourself')

if __name__ == '__main__':
    terms()
#barnsley()



