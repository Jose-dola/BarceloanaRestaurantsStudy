import geopy.point
import geopy.distance
import numpy as np
import os
import pickle

def get_restaurants_in_barcelona(restaurants_dict: list[dict]) -> list[dict]:
    """Filtering restaurants that are located inside the Barcelona 'locality'.

    Args:
        restaurants_dict (list[dict]): list of restaurants (as dictionaries)

    Returns:
        list[dict]: List of resturants (as dictionaries) in the Barcelona 'locality'.
    """
    #Dictionary to return
    barcelona_restaurants = []

    for restaurant in restaurants_dict:
        #For each restaurant, we check the 'address_components1 info
        for i in range(len(restaurant['address_components'])):
            #We identify the position in the list of the level type "locality"
            level_type = restaurant['address_components'][i]['types'][0]
            if level_type == 'locality':
                #Once the level type locality is found, we check if the restaurant is located in Barcelona
                if restaurant['address_components'][i]['long_name']=='Barcelona':
                    barcelona_restaurants.append(restaurant) 
    return barcelona_restaurants

def restaurants_geo_points(restaurants: list[dict]) -> list[geopy.point.Point]:
    """This function create a list of geo points (latitudes and longitudes) from a list of restaurant dictionaries.
    The same index in the two lists corresponds to the same restaurant

    Args:
        restaurants (list[dict]): list of restaurant dictionaries

    Returns:
        list[geopy.point.Point]: List of geo points (latitudes and longitudes) of each restaurant
    """    
    
    geo_points = []
    for restaurant in restaurants:
        geo_points.append(geopy.point.Point(restaurant['geometry']['location']['lat'], restaurant['geometry']['location']['lng']))
    
    return geo_points

def get_restaurants_inside_cercle(center: geopy.point.Point,
                                  radius: float, 
                                  restaurant_points: list[geopy.point.Point],
                                  restaurants: list[dict]) -> list[dict]:
    """This function returns the restaurants that are inside a cercle.

    Args:
        center (geopy.point.Point): Center of the cercle as a geo point (latitude and longitude)
        radius (float): Radius of the cercle in kilometers
        restaurants_points (list[geopy.point.Point]): List of restaurant geo points (latitudes and longitudes)
        restaurants (list[dict]): List of restaurant dictionaries

    Returns:
        list[dict]: list of restaurant dictionaries (that are inside the cercle)
    """
    selected_points = np.array([geopy.distance.geodesic(center,geo_p).kilometers < radius for geo_p in restaurant_points])
    return np.array(restaurants)[selected_points].tolist()

def get_restaurants_selection_inside_cercle(center: geopy.point.Point,
                                            radius: float, 
                                            restaurant_points: np.ndarray[geopy.point.Point]) -> np.ndarray[bool]:
    
    """This function returns the selection (numpy array of boolean values, True if the restaurant is selected and False if it is not) 
    of the restaurants that are inside a cercle

    Args:
        center (geopy.point.Point): Center of the cercle as a geo point (latitude and longitude)
        radius (float): Radius of the cercle in kilometers
        restaurants_points (np.ndarray[geopy.point.Point]): numpy array of restaurant geo points (latitudes and longitudes)

    Returns:
        np.ndarray[bool]: The selection (numpy array of boolean values, True if the restaurant is selected and False if it is not)
    """    

    return np.vectorize(lambda x: geopy.distance.geodesic(center,x).kilometers < radius)(restaurant_points)

def get_selections_from_pkl_files(folder: str) -> tuple[list[np.ndarray[bool]], list[geopy.point.Point]]:

    """This function extract the selections (boolean numpy arrays) stored in the .pkl files that are inside a folder.

    Args:
        folder (str): Name of the folder.

    Returns:
        tuple[list[np.ndarray[bool]], list[geopy.point.Point]]: 
                List of selections (each selection is a boolean numpy array) and
                list of geo points (latitudes and longitudes). 
                Each selection is around one of these points. The indexing coincides
    """  

    # Get all files in the folder
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    
    # Get restaurant dictionaries from files
    list_of_selections = []
    list_of_geo_points = []
    for f in files:
        lat_and_lon = os.path.splitext(f)[0].split('-')
        list_of_geo_points.append(geopy.point.Point(lat_and_lon))
        f_path = os.path.join(folder,f)
        with open(f_path, 'rb') as file:
            selection = pickle.load(file)
            list_of_selections.append(selection)
    
    return list_of_selections, list_of_geo_points

def grid_group_by(restaurants: np.ndarray[dict], selections: list[np.ndarray[bool]], get_function: callable, group_by_function: callable) -> list:
    """This function group by points in a grid. The list of all restaurants and the selections (boolean lists) for each point is given by the user. 
    The function to extract the quantity of interest from the restaurant dictionary is also given by the user. 
    The function to apply after the groupby (mean, count, etc.) is also given by the user.

    Args:
        restaurants (np.ndarray[dict]): Numpy array of restaurant dictionaries
        selections (list[np.ndarray[bool]]): List of selections (boolean numpy arrays)
        get_function (callable): Function to extract the quantity of interest from the restaurant dictionary.
        group_by_function (callable): The function to apply after the groupby (mean, count, etc.)

    Returns:
        list: Result of the groupby
    """    
    vectorized_get_function = np.vectorize(get_function)
    results = []
    for selection in selections:
        print(group_by_function(vectorized_get_function(restaurants[selection])))
        results.append(group_by_function(vectorized_get_function(restaurants[selection])))
    #vectorized_groupby_function = np.vectorize(lambda selection: group_by_function(vectorized_get_function(restaurants[selection])))
    #return vectorized_groupby_function(selections)
    return results

    

