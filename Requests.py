import json
import requests
import pandas as pd

#Select the radius of search
rad = 0.1

#The funcion ???? returns a grid of geopy points
grid = funcion()

#TCreating a list to save the places IDs
list_of_id = []

#API key
API_key

#Performing request and keeping data for any location in the grid
for point in grid:

    #Specifying latitude and longitude
    lat = str(point[0])
    lon = str(point[1])

    #API request
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat}%2C{lon}&radius={rad}&type=restaurant&key={API_key}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    #Getting the requested data as a dictionary
    dict = response.json()

    #Saving the ID of the places obtained from the requested data
    places = dict['results'] #This is a list of dictionaries, each of them containing info on a specific place
    for place in places:
        list_of_id.append(place["place_id"])

#Eliminating duplicate IDs
IDs = list(set(list_of_id))

#Creating a dictionary where we will save the desired information for the several places
dict_places = {
    'Name':[],
    'Postal Code':[]
}

#Requesting complete info for each of the places found
for id in IDs:
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={id}&key={API_key}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    #Getting the requested data as a dictionary
    dict = response.json()

    #Adding information in the dictionary
    dict_places['Name'].append(dict['Name'])
    dict_places['Postal Code'].append(dict['Postal Code'])

#Creating the dara frame
df = pd.DataFrame(dict_places)