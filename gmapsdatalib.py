import geopy.point
import geopy.distance
import json
import requests
import pandas as pd
import pickle

class RequestError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"RequestError: {self.message}"

def request_check(response: requests.models.Response):
    status = response.json()['status']
    if status != 'OK' and status != 'ZERO_RESULTS':
        raise RequestError("Google API returned the following status: "+status) 

def gridMaker(center: geopy.point.Point, \
              top_left: geopy.point.Point, \
              bottom_right: geopy.point.Point, \
              x_step: float, \
              y_step: float) -> list[tuple[float,float]]:    
    
    """Returns a grid of points where center, top_left, and bottom_right are three of the four vertexes 
    of the parallelogram. step_x and step_y are the distance between the points in the grid.
    
    Args:
        center (Point): A vertex of the grid/parallelogram
        top_left (Point): A vertex of the grid/parallelogram
        bottom_right (Point): A vertex of the grid/parallelogram
        x_step (float): Distance between points in the x axis of the grid/parallelogram (in meters). 
                        The x axis is the one defined by the center and the bottom_right points
        y_step (float): Distance between points in the y axis of the grid/parallelogram (in meters). 
                        The y axis is the one defined by the center and the top_left points

    Returns:
        list[tuple[float,float]]: The grid. List of tuples. Each tuple are the latitude and
                                  the longitude of a point in the grid
    """    
    # Steps in kilometers
    x_step = x_step / 1000
    y_step = y_step / 1000

    # Compute vector_x and vector_y coordinates
    vector_x_lat = bottom_right.latitude - center.latitude
    vector_x_lon = bottom_right.longitude - center.longitude
    vector_y_lat = top_left.latitude - center.latitude
    vector_y_lon = top_left.longitude - center.longitude

    # Compute the number of points in the grid according to the steps
    vx_norm = geopy.distance.geodesic(center, bottom_right).kilometers
    vy_norm = geopy.distance.geodesic(center, top_left).kilometers
    num_points_x = vx_norm/x_step
    num_points_y = vy_norm/y_step
    
    # Compute the grid of points
    grid = [] 
    npx = int(num_points_x)
    npy = int(num_points_y)
    for i in range(npx+1):
        for j in range(npy+1):
            latitude = center.latitude + \
                       (i/npx)*vector_x_lat + \
                       (j/npy)*vector_y_lat
            longitude = center.longitude + \
                       (i/npx)*vector_x_lon + \
                       (j/npy)*vector_y_lon
            grid.append((latitude, longitude))
            
    return grid

def get_ids_from_grid(grid: list[tuple[float,float]], \
                      place_type: str, \
                      API_key: str, \
                      payload: dict = {}, \
                      headers: dict = {}) -> list[str]:

    """Given a grid with coordinates (tuples of floats with latitude and longitude data) this function performs
    an API request to Google Maps in order to obtain the 20 closer points of interest (specified by the
    place_type argument) to each of the locations of the grid. It returns a list with the places id's used
    by Google Maps.
    
    Args:
        grid (list of float tuples): List with coordinates (latitude, longitude)
        place_type (str): Type of places of interest (for instance 'restaurant' or 'hospital')
        API_key (str): API key used to perform Nearby Search API requests.
        payload (dict): Payload used to perform Nearby Search API requests. It is an empty dictionary by default.
        headers (dict): Headers used to perform Nearby Search API requests. It is an empty dictionary by default.

    Returns:
        list[str]: List of place ids as a string.
    """  

    #Creating the list to save the places IDs
    list_of_id = []

    #Performing request and keeping data for any location in the grid
    for point in grid:

        #Specifying latitude and longitude
        lat = str(point[0])
        lon = str(point[1])

        #API request
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&type={place_type}&rankby=distance&key={API_key}'
        response = requests.request("GET", url, headers=headers, data=payload)
        request_check(response)

        #Getting the requested data as a dictionary
        dict = response.json()

        #Saving the ID of the places obtained from the requested data
        places = dict['results'] #This is a list of dictionaries, each of them containing info on a specific place
        for place in places:
            list_of_id.append(place["place_id"])
    
    return list(set(list_of_id))

def ids_to_file_from_grid(grid: list[tuple[float,float]], \
                      place_type: str, \
                      file_name: str, \
                      API_key: str, \
                      payload: dict = {}, \
                      headers: dict = {}) -> list[str]:

    """Given a grid with coordinates (tuples of floats with latitude and longitude data) this function performs
    an API request to Google Maps in order to obtain the 20 closer points of interest (specified by the
    place_type argument) to each of the locations of the grid. It saves this ids in a file.
    
    Args:
        grid (list of float tuples): List with coordinates (latitude, longitude)
        place_type (str): Type of places of interest (for instance 'restaurant' or 'hospital')
        file_name (str): Path of the file were the ids will be stored.
        API_key (str): API key used to perform Nearby Search API requests.
        payload (dict): Payload used to perform Nearby Search API requests. It is an empty dictionary by default.
        headers (dict): Headers used to perform Nearby Search API requests. It is an empty dictionary by default.
    """  

    # Open the file in write mode and truncate it
    with open(file_name, 'w') as file:
        file.truncate()

    #Performing request and keeping data for any location in the grid
    for i, point in enumerate(grid):

        #Specifying latitude and longitude
        lat = str(point[0])
        lon = str(point[1])

        #API request
        url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&type={place_type}&rankby=distance&key={API_key}'
        response = requests.request("GET", url, headers=headers, data=payload)
        request_check(response)

        #Getting the requested data as a dictionary
        dict = response.json()

        #Saving the ID of the places obtained from the requested data
        places = dict['results'] #This is a list of dictionaries, each of them containing info on a specific place
        with open(file_name, 'a') as file:
            for place in places:
                # Save id in the file
                file.write(str(i)+" "+place["place_id"]+"\n")

def get_unique_ids_from_files(files: list[str]) -> list[str]:

    """This function extracts the google maps API ids from files generated by the ids_to_file_from_grid() function. 
    It extracts all ids from the files, removes duplicates, and returns all the unique ids in a list.

    Args:
        files (list[str]): list of file paths

    Returns:
        list[str]: list of unique ids
    """   

    ids = []
    for file_name in files:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                split_line = line.split()
                ids.append(split_line[1])
    return list(set(ids))

def get_data_from_ids(ids: list[str], \
                      API_key: str, \
                      payload: dict = {}, \
                      headers: dict = {}) -> list[str]:

    """This function makes a list of dictionaries from a list of google maps place ids. 
    Each place id is a unique reference of a google maps place. For each place id, 
    a google maps API request is made to get all information about this place. 
    This information is given by google as a json dictionary. The function returns a list of dictionaries. 
    Each dictionary is the information of each place.
    
    Args:
        ids (list of strings): List of the requested google maps places ids.
        API_key (str): API key used to perform Nearby Search API requests.
        payload (dict): Payload used to perform Nearby Search API requests. It is an empty dictionary by default.
        headers (dict): Headers used to perform Nearby Search API requests. It is an empty dictionary by default.

    Returns:
        list[str]: List of dictionaries. Each dictionary is the information of each place.
    """  

    #Initializing the list of dictionries (each place data is a dictionary)
    list_of_dict = []

    #Requesting complete info for each place id
    for id in ids:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id}&key={API_key}"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        request_check(response)

        #Getting the requested data as a dictionary
        dict = response.json()['result']

        #Adding information in the list of dictionaries
        list_of_dict.append(dict)

    return list_of_dict

def data_from_ids_to_files(ids: list[str], \
                           folder: str, \
                           API_key: str, \
                           payload: dict = {}, \
                           headers: dict = {}) -> list[str]:

    """This function makes a list of dictionaries from a list of google maps place ids. 
    Each place id is a unique reference of a google maps place. For each place id, 
    a google maps API request is made to get all information about this place. 
    This information is given by google as a json dictionary. The function stores each
    dictionary in a file. The files are saved in a folder specified by the user. The function
    returns a list of the ids that had problems during the google API request.
    
    Args:
        ids (list of strings): List of the requested google maps places ids.
        folder (str): Path to the folder where the files will be saved (with no final slash)
        API_key (str): API key used to perform Nearby Search API requests.
        payload (dict): Payload used to perform Nearby Search API requests. It is an empty dictionary by default.
        headers (dict): Headers used to perform Nearby Search API requests. It is an empty dictionary by default.

    Returns:
        list[str]: List of the ids that had problems during the google API request. 
    """  

    #ids that raised an error in the google API request
    error_ids = []

    #Requesting complete info for each of place id
    for id in ids:
        url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id}&key={API_key}"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        try:
            request_check(response)
        except:
            error_ids.append(id)
            continue

        #Getting the requested data as a dictionary
        dict = response.json()['result']

        #Saving the dictionary in a file
        with open(folder+'/'+id+'.pkl', 'wb') as file:
            pickle.dump(dict, file)
    return error_ids