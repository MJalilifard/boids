import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv


#defining variables

number_of_agents = 50 # number of agents
width = 10 # width of the world
height = 10 # height of the world
neighborhood = 2 # radius of neighborhood
seed = 1
np.random.seed(seed)
pos = 10 * np.random.random((number_of_agents,2)) # the matrix of agents's positions
veloc = 1 * np.random.random((number_of_agents,2)) # the matrix of agents's velocities
dt = 0.1 # time step
time = 50 # number of iteration or time duration
alpha = .01 # separation influence factor
beta = .05 # alignment influence factor
gamma = .01 # cohesion influence factor


#define function that take one step moving forward in time

def step(pos,veloc,dt):
    pos = pos + dt * veloc
    return pos


# handling the cases when an agent hits the world boundary and spawn periodic

def spawn(pos,width,height):
    pos[:,0] = pos[:,0]%width
    pos[:,1] = pos[:,1]%height
    return pos

def plot_boids(pos):
    fig, ax = plt.subplots()
    ax.set(xlabel="X", ylabel="Y", xlim=(0,width), ylim=(0,height), title="Boids: Agent's positions")
    ax.scatter(pos[:,0], pos[:,1], color="green")
    return fig


# give the list of neighbors of all agents

def find_neighbors(pos,neighborhood,width,height):
    all_neighbors = []
    for j in range(pos.shape[0]):
        neighbors = [] # neighbors of one particular agent
        for i in range(pos.shape[0]):
            dx = ((pos[j,0]-pos[i,0]+width/2)%width)-(width/2) # defining distance for periodic boundary
            dy = ((pos[j,1]-pos[i,1]+height/2)%height)-(height/2) # defining distance for periodic boundary
            d = np.sqrt( (dx)**2 + (dy)**2 )
            if d < neighborhood and i != j:
                neighbors.append(i)
        all_neighbors.append(np.array(neighbors))
    return all_neighbors


# separation rule 
# give the list of all separation vectors of agents

def find_separations(pos):
    neighbors = find_neighbors(pos,neighborhood,width,height)
    all_separations = []
    for j in range(pos.shape[0]):
        separations = [] 
        for i in neighbors[j]:
            dx = ((pos[j,0]-pos[i,0]+width/2)%width)-(width/2)
            dy = ((pos[j,1]-pos[i,1]+height/2)%height)-(height/2)
            separations.append(np.array([-dx,-dy])) # vectors from the agent toward each neighbor


        if separations: # if separation was empty it returns False
            separations = np.sum(separations,axis=0) # separation vector of an agent
        else:
            separations = np.array([0, 0])

        all_separations.append(separations)
    return all_separations


# alignment rule
# give the list of all alignments vectors of agents

def find_alignments(pos):
    neighbors = find_neighbors(pos,neighborhood,width,height)
    all_alignments = []
    for j in range(pos.shape[0]):
        alignments = [] 
        for i in neighbors[j]:
            alignments.append(veloc[i])

        if alignments:
            alignments = (1/len(alignments)) * np.sum(alignments,axis=0)
        else:
            alignments = np.array([0,0])

        all_alignments.append(alignments)
    return all_alignments


# cohesion rule
# give the list of all cohesion vectors of agents

def find_cohesions(pos):
    neighbors = find_neighbors(pos,neighborhood,width,height)
    all_cohesions = []
    for j in range(pos.shape[0]):
        cohesions = [] 
        for i in neighbors[j]:
            dx = ((pos[j,0]-pos[i,0]+width/2)%width)-(width/2)
            dy = ((pos[j,1]-pos[i,1]+height/2)%height)-(height/2)
            cohesions.append(np.array([-dx,-dy])) # vectors from the agent toward each neighbor

        if cohesions:
            cohesions = (1/len(cohesions)) * np.sum(cohesions,axis=0) # cohesion vector of an agent
        else:
            cohesions = np.array([0, 0])

        all_cohesions.append(cohesions)
    return all_cohesions


# implementing three rules
# and update the velocity

def update_veloc(pos,veloc):
    all_separations = find_separations(pos)
    all_alignments = find_alignments(pos)
    all_cohesions = find_cohesions(pos)
    for i in range(pos.shape[0]):
        veloc[i] = veloc[i] + alpha * all_separations[i] + beta * (all_alignments[i]-veloc[i]) + gamma * all_cohesions[i]
    return veloc


# crating directories for storing data and figures for each run
# i manually change run_*** (e.g. run_001) considering the number
# of last run 

figures_dir = Path('./results/run_001/figures')
figures_dir.mkdir(parents=True, exist_ok=True)
run_dir = Path('./results/run_001')
polarization_file = run_dir / "polarization.csv"
parameters_file = run_dir / "parameters.txt"

# creating images and calculate polarization of each iteration
# polarization is a quantity that evaluate collective motion

polarization = [] # for storing polarization
for i in range (time):
    # plot and save figures
    fig = plot_boids(pos)
    fig.savefig(figures_dir / f"figure_{i+1}.png")
    plt.close(fig)
    # calcualting polarization
    p = veloc.copy()
    for j in range(pos.shape[0]):
        speed = np.sqrt( p[j][0]**2 + p[j][1]**2 )
        if speed != 0:  
            p[j] /= speed
    p = np.sum(p, axis=0)
    p = (1/veloc.shape[0]) * np.sqrt( p[0]**2 + p[1]**2 )
    polarization.append(p)
    # udate veloc and then move them
    update_veloc(pos,veloc)
    pos = step(pos,veloc,dt)
    pos = spawn(pos,width,height)


# storing polarization in a csv file

with open(polarization_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["iteration","polarization"])
    for i in range(len(polarization)):
        writer.writerow([i,polarization[i]])


# storing parameters in a txt file

with open(parameters_file, "w") as file:
    file.write(f"number of agents = {number_of_agents}\nwidth of the world = {width}\nheight of the world = {height}\nneighborhood radius = {neighborhood}\nseed = {seed}\ntime step = {dt}\ntime duration = {time}\nalpha = {alpha}\nbeta = {beta}\ngamma = {gamma}")


# plotting changes of polarization over time

fig, ax = plt.subplots()
ax.set(ylabel="Polarization", xlabel="Time", title="Polarization over time")
ax.plot(range(len(polarization)),polarization)
fig.savefig(figures_dir / "polarization.png")
plt.close(fig)

