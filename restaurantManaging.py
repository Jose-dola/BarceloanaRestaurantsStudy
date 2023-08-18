import geopy.point
import geopy.distance
import geopy.geocoders
import numpy as np
import os
import pickle
import math
import pandas as pd

# Global variables
neighbourhoods = {
    '08001' : 'El Raval',
    '08002' : 'Barri Gotic',
    '08003' : 'Barceloneta',
    '08004' : 'Poble Sec',
    '08005' : 'Poblenou',
    '08006' : 'El Farro',
    '08007' : 'Antiga Esquerra Eixample',
    '08008' : 'Antiga Esquerra Eixample',
    '08009' : 'Dreta Eixample',
    '08010' : 'Dreta Eixample',
    '08011' : 'Esquerra Eixample',
    '08012' : 'Vila de Gracia',
    '08013' : 'El Fort Pienc',
    '08014' : 'La Bordeta - Les Corts',
    '08015' : 'Nova Esquerra Exiample - Sant Antoni',
    '08016' : 'Porta-La Prosperitat',
    '08017' : 'Vallvidrera',
    '08018' : 'El Clot',
    '08019' : 'El Besos - Sant Marti',
    '08020' : 'La Verneda - Sant Marti de Provençals',
    '08021' : 'Les Corts - Sarria',
    '08022' : 'Sarria - La Bonanova',
    '08023' : 'El Coll',
    '08024' : 'Gracia - Can Baro',
    '08025' : "Camps d'en Grassot i Gracia Nova",
    '08026' : "Camp de l'arpa",
    '08027' : "El Congres - Navas",
    '08028' : "Les Corts",
    '08029' : "Sarria",
    '08030' : "San Andres Palomar",
    '08031' : "Horta",
    '08032' : "La Font d'en Fargues",
    '08033' : "Trinitat - Torre Baro",
    '08034' : "Pedralbes",
    '08035' : "Sant Genis dels Agudells",
    '08036' : "Esquerra Eixample",
    '08037' : "Dreta Eixample",
    '08038' : "Montjuic",
    '08039' : "Port de Barcelona",
    '08040' : "Zona Franca",
    '08041' : "El Guinardo",
    '08042' : "Canyelles - Roquetes"
}
districts = {
    'El Raval' : 'Ciutat Vella',
    'Barri Gotic' : 'Ciutat Vella',
    'Barceloneta' : 'Ciutat Vella',
    'Poble Sec' : 'Sants - Montjuic',
    'Poblenou' : 'Sant Marti',
    'El Farro' : 'Sarria - Sant Gervasi',
    'Antiga Esquerra Eixample' : 'Eixample',
    'Dreta Eixample' : 'Eixample',
    'Esquerra Eixample' : 'Eixample',
    'Vila de Gracia' : 'Gracia',
    'El Fort Pienc' : 'Eixample',
    'La Bordeta - Les Corts' : 'Sants - Montjuic',
    'Nova Esquerra Exiample - Sant Antoni' : 'Eixample',
    'Porta-La Prosperitat' : 'Nou Barris',
    'Vallvidrera' : 'Sarria - Sant Gervasi',
    'El Clot' : 'Sant Marti',
    'El Besos - Sant Marti' : 'Sant Marti',
    'La Verneda - Sant Marti de Provençals' : 'Sant Marti',
    'Les Corts - Sarria' : 'Les Corts',
    'Sarria - La Bonanova' : 'Les Corts',
    'El Coll' : 'Gracia',
    'Gracia - Can Baro' : 'Gracia',
    "Camps d'en Grassot i Gracia Nova" : 'Gracia',
    "Camp de l'arpa" : 'Sant Marti',
    "El Congres - Navas" : 'Sant Andreu',
    "Les Corts" : 'Les Corts',
    "Sarria" : 'Sarria - Sant Gervasi',
    "San Andres Palomar" : 'Sant Andreu',
    "Horta" : 'Horta - Guinardo',
    "La Font d'en Fargues" : 'Horta - Guinardo',
    "Trinitat - Torre Baro" : 'Nou Barris',
    "Pedralbes" : 'Les Corts',
    "Sant Genis dels Agudells" : 'Horta - Guinardo',
    "Montjuic" : 'Sants - Montjuic',
    "Port de Barcelona" : 'Sants - Montjuic',
    "Zona Franca" : "Sants - Montjuic",
    "El Guinardo" : 'Horta - Guinardo',
    "Canyelles - Roquetes" : 'Nou Barris'
}

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

def grid_group_by(restaurants: list[dict], selections: list[np.ndarray[bool]], get_function: callable, group_by_function: callable) -> list:
 
    """This function group by points in a grid. The list of all restaurants and the selections (boolean lists) for each point is given by the user. 
    The function to extract the quantity of interest from the restaurant dictionary is also given by the user. 
    The function to apply after the groupby (mean, count, etc.) is also given by the user.

    Args:
        restaurants (list[dict]): List of restaurant dictionaries
        selections (list[np.ndarray[bool]]): List of selections (boolean numpy arrays)
        get_function (callable): Function to extract the quantity of interest from the restaurant dictionary.
        group_by_function (callable): The function to apply after the groupby (mean, count, etc.)

    Returns:
        list: Result of the groupby
    """    

    # Creating numpy array from restaurants list
    restaurants_array = np.array(restaurants)
    # Function to apply get_function to all elements in a numpy array
    vectorized_get_function = np.vectorize(get_function)
    # Applying the gruopby and storing the results in the results list
    results = []
    for selection in selections:
        restaurants_selection = restaurants_array[selection]
        n = len(restaurants_selection)
        if n > 0: group_results = vectorized_get_function(restaurants_selection)
        else: group_results = np.array([])
        results.append(group_by_function(group_results))

    return results

def geopoints_values_to_csv(geo_points: list[geopy.point.Point], 
                            values: list, 
                            headers: list[str] = ["latitude","longitude","value"], 
                            file_name: str = ["geo_table.csv"]):
    """This function creates a CSV file with 3 columns. The first and de second columns are the latitudes and longitudes 
    according to a given list of geo points (latitudes and longitudes). The third column is the corresponding value for each 
    latitude and longitude.

    Args:
        geo_points (list[geopy.point.Point]): List of geo points (latitudes and longitudes).
        values (list): Values associated to each geo point (latitude and longitude).
        headers (list[str]): Headers for the CSV file. Defaults to ["latitude","longitude","value"]. 
        file_name (str): Name of the CSV file. Defaults to ["geo_table.csv"].
    """    

    # Initializing pandas data frame
    df = pd.DataFrame(columns=headers)
    # Setting columns
    df[headers[0]] = [p.latitude for p in geo_points]
    df[headers[1]] = [p.longitude for p in geo_points]
    df[headers[2]] = values
    # Creating csv from the pandas dataframe
    df.to_csv(file_name,index=False)

def get_postal_code_in_barcelona(restaurants_dict: list[dict]) -> list[str]:
    """Given a list of restaurants (as dictionaries) this function returns the postal code,
       if available, or a NaN entry, if the postal code is not available.

    Args:
        restaurants_dict (list[dict]): list of restaurants (as dictionaries)

    Returns:
        list[str]: List of postal codes (as strings).
    """
    #List to return
    postal_codes = []

    for restaurant in restaurants_dict:
        #To keep control if the postal code is available
        found = False
        #For each restaurant, we check the 'address_components' info
        for i in range(len(restaurant['address_components'])):
            #We identify the position in the list of the level type "postal_code"
            level_type = restaurant['address_components'][i]['types'][0]
            if level_type == 'postal_code':
                #Once the level type postal_code is found, we include it in the list
                postal_codes.append(restaurant['address_components'][i]['long_name'])
                found = True
                break
        if not found:
            postal_codes.append(math.nan)
    return postal_codes

def get_simple_category(restaurants_dict: list[dict],
                        category: str) -> list[str]:
    """This funcion gets two arguments.
       The first one is a list of restaurants (as dictionaries).
       The second one is a "simple category", being this a key in a restaurant's dictionary whose value
       is a single variable (that is, neither a list or a dictionary). "Simple category" are:
       
       'adr_address', 'business_status', 'dine_in', 'formatted_address', 'formatted_phone_number', 'icon',
       'icon_background_color', 'icon_mask_base_uri', 'international_phone_number', 'name', 'place_id',
       'rating', 'reference', 'reservable', 'serves_beer', 'serves_breakfast', 'serves_brunch', 'serves_dinner',
       'serves_lunch', 'serves_vegetarian_food', 'serves_wine', 'takeout', 'url', 'user_ratings_total', 'utc_offset',
       'vicinity', 'website' and 'wheelchair_accessible_entrance'


       The function creates then a list with the info of the specified category, if available, or a NaN entry,
       if the the info is not available.

    Args:
        restaurants_dict (list[dict]): list of restaurants (as dictionaries).
        category (str): name of the category of interest. 
    Returns:
        list[str]: list of the category info for each restaurant.
    """
    #List to return
    category_info = []
    
    for restaurant in restaurants_dict:
        try:
            category_info.append(restaurant[category])
        except:
            category_info.append(math.nan)
    
    return category_info

def get_nbh_distr_from_pc(df:pd.DataFrame) -> pd.DataFrame:
    """This function should be provided with a DataFrame of restaurants with a 'Postal Code' column
       as an argument. Then, based on the postal code, it will create two additional columns to the
       provided DataFrame,  one for the neighbourhood and one for the district.

       If the 'Postal Code' column in the DataFrame has a non-valid entry, then it returns both
       neighbourhood and district as a NaN values.

    Args:
        df (DataFrame): DataFrame of restaurants with a 'Postal Code' column.

    Returns:
        DataFrame: Original data frame with two additional columns: "Neighbourhood" and "District"
    """   

    global neighbourhoods
    global districts

    nbh_list = []
    dis_ist = []

    for postal_code in df['Postal Code']:
        try:
            nbh = neighbourhoods[postal_code]
        except:
            nbh_list.append(math.nan)
            dis_ist.append(math.nan)
        else:
            nbh_list.append(nbh)
            dis = districts[nbh]
            dis_ist.append(dis)
    
    df['Neighbourhood'] = nbh_list
    df['District'] = dis_ist

    return df
    
def get_barcelona_postalcodes() -> list[str]:
    """This function returns a list of all postal codes in Barcelona

    Returns:
        list[str]: All postal codes in Barcelona
    """    
    global neighbourhoods
    return list(neighbourhoods.keys())

def get_postalcode_from_geopoint(geo_point: geopy.point.Point) -> str:

    # Create a geocoder instance
    geolocator = geopy.geocoders.Nominatim(user_agent="my_geocoder")
    
    # Define the latitude and longitude coordinates
    latitude = geo_point.latitude
    longitude = geo_point.longitude
    
    # Geocode the coordinates
    location = geolocator.reverse((latitude, longitude))
    
    # Extract the postal code from the location address
    postal_code = location.raw['address']['postcode']
    
    return postal_code