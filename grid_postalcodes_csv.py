import restaurantManaging as rman

# Getting geo points and selections according to this geo points from stored .pkl files
geo_points = rman.get_selections_from_pkl_files("filtering_grid")[1]
# Getting postal codes of each geo point
pcodes = []
for p in geo_points:
    try:
        pcode = rman.get_postalcode_from_geopoint(p)
    except:
        pcode = 'nan'
    pcodes.append(pcode)

# Saving results in a CSV file
headers = ["latitude","longitude","postal_code"]
file_name = "grid_postalcodes.csv"
rman.geopoints_values_to_csv(geo_points,pcodes,headers=headers,file_name=file_name)