import numpy as np

#defining variables
n = 50 # number of agents
w = 10 # width of the world
h = 10 # height of the world
r = 2 # radius of neighborhood
# pos = 10 * np.random.random((50,2)) # the matrix of agents positions
pos = np.array([
    [0.2, 5.0],
    [9.8, 5.0],
    [5.0, 5.0]
])
veloc = 1 * np.random.random((50,2)) # the matrix of agents velocities
dt = 0.1 # time step

#define function that take one step moving forward in time
def step(pos,veloc,dt):
    pos = pos + dt * veloc
    return pos

# the caes when agent hits the world boundary and spawn periodic
# periodic boundary
def spawn(pos,w,h):
    pos[:,0] = pos[:,0]%w
    pos[:,1] = pos[:,1]%h
    return pos

import matplotlib.pyplot as plt

def plot_boids(pos):
    fig, ax = plt.subplots()
    ax.set(xlabel="X", ylabel="Y", xlim=(0,10), ylim=(0,10), title="Boids")
    ax.scatter(pos[:,0], pos[:,1], color="green")
    return fig

'''
 for i in range (50):
    fig = plot_boids(pos)
    pos = step(pos,veloc,dt)
    pos = spawn(pos,w,h)
    fig.savefig(f"figure_{i+1}")
'''

def find_neighbors(pos,r,w,h):
    all_neighbors = [] # list of neighbors of all agents
    for j in range(pos.shape[0]):
        neighbors = [] # neighbors of one particular agent
        for i in range(pos.shape[0]):
            dx = ((pos[j,0]-pos[i,0]+w/2)%w)-(w/2) # defining distance in periodic boundary world
            dy = ((pos[j,1]-pos[i,1]+h/2)%h)-(h/2) # defining distance in periodic boundary world
            d = np.sqrt( (dx)**2 + (dy)**2 )
            if d < r and i != j:
                neighbors.append(i)
        all_neighbors.append(np.array(neighbors))
    return all_neighbors

