import gmapsdatalib as gmd
import restaurantManaging as rman
import geopy.point
import geopy.distance
import numpy as np
import os
import pickle

# Barcelona vertexes for the grid
center = geopy.point.Point(41.3054, 2.1334)
tl = geopy.point.Point(41.3844, 2.0675)
br = geopy.point.Point(41.44,2.25)
# Distances between points in the grid
x_step = 350
y_step = 350

# Make the Barcelona grid 
grid = gmd.gridMaker(center, tl, br, x_step, y_step)

# Calculate a value for the influence radius of a point in the grid
# This value is goint to be (aprox) half of the diagonal between two points in the grid
influence_radius = np.sqrt(x_step*x_step + y_step*y_step) / 2
# Meters to kilometers
influence_radius = influence_radius / 1000

# Read restaurant dictionaries
restaurants = gmd.pkl_files_to_list_of_dicts("ids_full_info")

# Filtering restaurants inside Barcelona
restaurants = rman.get_restaurants_in_barcelona(restaurants)

# Extracting the geo points (latitude and longitude) of each restaurant
geo_points = rman.restaurants_geo_points(restaurants)

# Converting lists to numpy arrays
restaurants_np = np.array(restaurants)
geo_points_np = np.array(geo_points)

# Saving the selection of the restaurants inside the influence area of each point in the grid
folder = "filtering_grid"
for point in grid:
    file_name = f"{point[0]}-{point[1]}.pkl"
    path = os.path.join(folder,file_name)
    selection = rman.get_restaurants_selection_inside_cercle(point, influence_radius, geo_points_np)
    # Saving selection in a file
    with open(path, 'wb') as file:
        pickle.dump(selection, file)

# Saving the grid in a file
with open("grid_350.pkl",'wb') as file:
    pickle.dump(grid, file)