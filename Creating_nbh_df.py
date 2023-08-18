import gmapsdatalib as gmd
import restaurantManaging as rman
import geopy.point
import pickle

#Getting the list of restaurants (as dictionaries) from a file
restaurants_dict = gmd.pkl_files_to_list_of_dicts('ids_full_info')

#Getting only restaurants in Barcelona
barcelona_restaurants = rman.get_restaurants_in_barcelona(restaurants_dict)

#Selecting categories of interest for the data frame
categories_of_interest = [
    'name',
    'formatted_address',
    'rating',
    'delivery',
    'dine_in',
    'reservable',
    'serves_beer',
    'serves_brunch',
    'serves_dinner',
    'serves_lunch',
    'serves_vegetarian_food',
    'serves_wine',
    'takeout',
    'user_ratings_total',
    'vicinity',
    'wheelchair_accessible_entrance',
]

dict_to_df = {}
for category in categories_of_interest:
    dict_to_df[category] = rman.get_simple_category(barcelona_restaurants, category)

#Adding geographic data
lat = []
lng = []

for restaurant in barcelona_restaurants:
    latitude = restaurant['geometry']['location']['lat']
    longitude = restaurant['geometry']['location']['lng']

    lat.append(latitude)
    lng.append(longitude)

dict_to_df['Latitude'] = lat
dict_to_df['Longitude'] = lng

#Adding postal codes
dict_to_df['Postal Code'] = rman.get_postal_code_in_barcelona(barcelona_restaurants)

#Creating DataFrame
df = pd.DataFrame(dict_to_df)

#Dropping rows with a non-valid postal code
df = df.dropna(subset=['Postal Code'])

#Getting neighbourhood and district data
df = rman.get_nbh_distr_from_pc(df)

#Creating a CSV file
df.to_csv('nbhoods.csv', index=False)