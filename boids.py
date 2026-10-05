import numpy as np

#defining variables
n = 50
x = 10
y = 10
pos = 10 * np.random.random((50,2))
veloc = 1 * np.random.random((50,2))
dt = 0.1

#define function that take one step moving forward in time
def step(pos,veloc,dt):
    pos = pos + dt * veloc
    return pos

# the caes when agent hits the world boundary and spawn periodic
# periodic boundary
def spawn(pos,x,y):
	pos[:,0] = pos[:,0]%x
	pos[:,1] = pos[:,1]%y
	return pos
	
import matplotlib.pyplot as plt

def plot_boids(pos):
    fig, ax = plt.subplots()
    ax.set(xlabel="X", ylabel="Y", xlim=(0,10), ylim=(0,10), title="Boids")
    ax.scatter(pos[:,0], pos[:,1], color="green")
    return fig

for i in range (50):
    fig = plot_boids(pos)
    pos = step(pos,veloc,dt)
    pos = spawn(pos,x,y)
    fig.savefig(f"figure_{i+1}")
