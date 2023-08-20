import restaurantManaging as rman
import pandas as pd
import numpy as np

# Getting geo points from stored .pkl files
geo_points = rman.get_selections_from_pkl_files("filtering_grid")[1]

# Generating a CSV file
headers = ["latitude","longitude","size"]
# Initializing pandas data frame
df = pd.DataFrame(columns=headers)
# Setting columns
df[headers[0]] = [p.latitude for p in geo_points]
df[headers[1]] = [p.longitude for p in geo_points]
df[headers[2]] = [1 for p in geo_points]
file_name = "parallelogram_grid.csv"
# Creating csv from the pandas dataframe
df.to_csv(file_name,index=False)