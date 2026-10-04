import random
import numpy as np

#defining variables
n = 50
x = 10
y = 10
pos = 10 * np.random.random((50,2))
veloc = np.random.random((50,2))
dt = 0.1

#define function that take one step moving forward in time
def step(pos,veloc,dt):
    pos = pos + dt * veloc
    return new_pos

# the caes when agent hits the world boundary and spawn periodic
# periodic boundary
def spawn(pos,x,y):
	pos[:,0] = pos[:,0]%x
	pos[:,1] = pos[:,1]%y
	return pos
	
