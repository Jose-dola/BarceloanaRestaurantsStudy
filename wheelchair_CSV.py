import gmapsdatalib as gmd
import restaurantManaging as rman
import pandas as pd
import numpy as np

# Function to get if a restaurant is wheelchair friendly or not
def get_wheelchair(restaurant):
    if 'wheelchair_accessible_entrance' in restaurant:
        #return restaurant['wheelchair_accessible_entrance']
        if str(restaurant['wheelchair_accessible_entrance']) == 'True':
            return True
    return False

# Function to count how many trues are in a boolean list
def count_true(list):
    return len([b for b in list if b == True])

# Getting restaurant dictionaries from stored .pkl files
restaurants = gmd.pkl_files_to_list_of_dicts("ids_full_info")

# Filtering to have only restaurants in Barcelona
restaurants = rman.get_restaurants_in_barcelona(restaurants)
print(len(restaurants))

# Getting geo points and selections according to this geo points from stored .pkl files
selections, geo_points = rman.get_selections_from_pkl_files("filtering_grid")
print(len(selections))
print(len(geo_points))

# Filtering geo points and selections with postal codes in Barcelona
pcodes_filter = rman.get_barcelona_postalcodes()
df = pd.read_csv("grid_postalcodes.csv")
pcodes = df[df.columns[2]]
pcodes = [str(pc) for pc in pcodes.values]
postal_code_selection = rman.filter_by_postalcode(pcodes, pcodes_filter)
geo_points = list(np.array(geo_points)[postal_code_selection])
selections = list(np.array(selections)[postal_code_selection])
print(len(selections))
print(len(geo_points))
# Counting the number of restaurants wheelchair friendly around each geo point (250m aprox) 
# and generating a CSV file
headers = ["latitude","longitude","number_of_wheelchair_friendly_restaurants_around(250m)_this_point"]
values = rman.grid_group_by(restaurants, selections, get_wheelchair, count_true)
file_name = "wheelchair_count_grid.csv"
rman.geopoints_values_to_csv(geo_points,values,headers=headers,file_name=file_name)