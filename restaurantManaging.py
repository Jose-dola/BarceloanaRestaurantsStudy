import geopy.point
import geopy.distance
import numpy as np

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
        radius (float): radius of the cercle in kilometers
        restaurants_points (list[geopy.point.Point]): list of restaurant geo points (latitudes and longitudes)
        restaurants (list[dict]): list of restaurant dictionaries

    Returns:
        list[dict]: list of restaurant dictionaries (that are inside the cercle)
    """
    selected_points = np.array([geopy.distance.geodesic(center,geo_p).kilometers < radius for geo_p in restaurant_points])
    return np.array(restaurants)[selected_points].tolist()
