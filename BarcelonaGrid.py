import gmapsdatalib as gmd
import geopy.point
import pickle

# Barcelona vertexes for the grid
center = geopy.point.Point(41.3054, 2.1334)
tl = geopy.point.Point(41.3844, 2.0675)
br = geopy.point.Point(41.44,2.25)
# Distances between points in the grid
x_step = 90
y_step = 90

# Make the Barcelona grid 
grid = gmd.gridMaker(center, tl, br, x_step, y_step)

# Save grid variable to a file
with open('grid.pkl', 'wb') as file:
    pickle.dump(grid, file)

