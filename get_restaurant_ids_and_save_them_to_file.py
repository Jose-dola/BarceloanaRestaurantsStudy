import gmapsdatalib as gmd
import pickle

# Get grid from file
grid_file_name = "grid.pkl"
with open(grid_file_name,'rb') as file:
    grid = pickle.load(file)

# Request ids from google and save them to a file
API_key = "AIzaSyAfPSVFq_woTIxoa0u8FJRXdN647sEra4Y"
ids_file_name = "list_of_ids.txt"
place_type = "restaurant"
gmd.ids_to_file_from_grid(grid, place_type, ids_file_name, API_key)
