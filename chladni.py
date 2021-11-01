import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Grid of cells
WIDTH = 100
HEIGHT = 100
fixed = np.ones((HEIGHT, WIDTH)) # Array of 0s and 1s indicating 0 for a cell fixed in place and 1 for free
fixed[20, 0:40] = 0
active = np.zeros((HEIGHT, WIDTH)) # Array of 0s and 1s indicating which cells are being actively vibrated
active[0, 0] = 1
influ = np.ones((HEIGHT, WIDTH)) # Influence coefficient of how strongly a cell affects its neighbors
displ = np.zeros((HEIGHT, WIDTH)) # Displacement of cells
veloc = np.zeros((HEIGHT, WIDTH)) # Velocity of cells
accel = np.zeros((HEIGHT, WIDTH)) # Acceleration of cells
mass = 40 # mass of each cell

# Variables for active vibration
time = 0
period = 10

# Variables for plotting
epsilon = 100 # Consider the cell to be stationary if the magnitude of its average velocity is below epsilon
steps_per_plot = 100 # number of iterations between each plot frame

# Determines stationary cells from their average velocities
def stationary(v):
    global epsilon
    if abs(v) < epsilon:
        return 1
    return 0

# Grid update function
def updatefig(*args):
    global fixed, active
    global influ, displ, veloc, accel, mass
    global time, period
    global steps_per_plot

    average_vel = veloc
    step = 0
    
    for i in range(steps_per_plot):
        # Update displacement
        displ += veloc
        displ *= fixed
        # clip displacement values to range
        displ = np.clip(displ, -10000, 10000)
        # Update velocity
        veloc += accel
        veloc *= fixed
        # Update acceleration
        # Use displacement and influences of cells to north, south, east, west
        dn = np.roll(displ, 1, axis=0)
        dn[0, :] = 0
        fn = np.roll(influ, 1, axis=0)
        fn[0, :] = 0
        ds = np.roll(displ, -1, axis=0)
        ds[HEIGHT - 1, :] = 0
        fs = np.roll(influ, -1, axis=0)
        fs[HEIGHT - 1, :] = 0
        dw = np.roll(displ, 1, axis=1)
        dw[:, 0] = 0
        fw = np.roll(influ, 1, axis=1)
        fw[:, 0] = 0
        de = np.roll(displ, -1, axis=1)
        de[:, WIDTH - 1] = 0
        fe = np.roll(influ, -1, axis=1)
        fe[:, WIDTH - 1] = 0
        # New acceleration is dependent on how relatively displaced each neighbor is and influence
        accel = (dn - displ) * fn + (ds - displ)* fs + (de - displ) * fe + (dw - displ) * fw
        accel /= mass
        accel *= fixed
        # Update active cells
        displ += active * np.sin(time / period) - active * displ
        # Update time
        time = time + 1
        step = step + 1
        # Update rolling average velocity value
        average_vel = (average_vel * step + veloc) / (step + 1)

    # Plot cells with average velocity below epsilon
    vstationary = np.vectorize(stationary)
    nodes = vstationary(average_vel)
    # Change this to plot different things
    im.set_array(nodes)
    return im,

# Plot and animate the grid

fig = plt.figure()

# Change this to make the plot sensitive to different ranges
nodes = np.zeros((HEIGHT, WIDTH))
nodes[0, 0] = 1
im = plt.imshow(nodes, animated=True)

ani = animation.FuncAnimation(fig, updatefig, interval=16, blit=True)
plt.show()
