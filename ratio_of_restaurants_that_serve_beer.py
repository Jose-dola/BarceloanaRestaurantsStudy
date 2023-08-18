import gmapsdatalib as gmd
import restaurantManaging as rman
import pandas as pd
import numpy as np

# Function to know if a restaurant serves beer or not
def check_beer(restaurant):
    if 'serves_beer' in restaurant.keys():
        if str(restaurant['serves_beer']) == "True":
            return 1
        else:
            return 0 
    else:
        return -1

# Function to compute the ratio of restaurants that serve beer after groupying by geo point
def ratio_server_beer(serves_beer_list):
    total = 0
    serves_beer = 0
    for serves_beer_element in serves_beer_list:
        if serves_beer_element == 1:
            total += 1
            serves_beer += 1
        elif serves_beer_element == 0:
            total += 1
    if total > 0:
        return serves_beer / total
    else:
        return 0

# Getting restaurant dictionaries from stored .pkl files
restaurants = gmd.pkl_files_to_list_of_dicts("ids_full_info")

# Filtering to have only restaurants in Barcelona
restaurants = rman.get_restaurants_in_barcelona(restaurants)

# Getting geo points and selections according to this geo points from stored .pkl files
selections, geo_points = rman.get_selections_from_pkl_files("filtering_grid")

# Filtering geo points and selections with postal codes in Barcelona
pcodes_filter = rman.get_barcelona_postalcodes()
df = pd.read_csv("grid_postalcodes.csv")
pcodes = df[df.columns[2]]
pcodes = [str(pc) for pc in pcodes.values]
postal_code_selection = rman.filter_by_postalcode(pcodes, pcodes_filter)
geo_points = list(np.array(geo_points)[postal_code_selection])
selections = list(np.array(selections)[postal_code_selection])

# Computing the ratio of restaurants that serve beer around each geo point (250m aprox) 
# and generating a CSV file
headers = ["latitude","longitude","ratio_of_restaurants_that_serve_beer_around(250m)_this_point"]
values = rman.grid_group_by(restaurants, selections, check_beer, ratio_server_beer)
file_name = "ratio_serve_beer.csv"
rman.geopoints_values_to_csv(geo_points,values,headers=headers,file_name=file_name)