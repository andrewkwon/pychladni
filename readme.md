Python script to simulate vibrations travelling in a material. The goal was to generate some nice Chladni patterns.

The material is modeled by a grid of cells. Each cell has a displacement, velocity, and acceleration. Acceleration is a function of the relative displacement of the cell to its Von Neumann neighbors. The script finds the average velocity of each cell over a given number of past steps, then plots whether or not that cell is "stationary" or not by the magnitude of that average velocity.

Which cells are fixed and which are actively vibrating can be configured in the code.

I don't think that I succeeded in accurately simulating how Chladni figures actually arise, but there are some interesting results nonetheless.

![./Animation_1.gif]