import pandas as pd

def f_size(ratio):
    if float(ratio) == 0: return float(ratio)
    else: return (float(ratio) - 0.4)*100

# Open the file in read mode
file = open("ratio_serve_beer.csv", "r")

# Read all lines of the file
lines = file.readlines()

# Close the file
file.close()

# Making the data frame
headers_line = lines[0]
headers_line = headers_line.replace("\n","")
headers = headers_line.split(',')
headers.append("size")
lat = []
lon = []
ratio = []
size = []
for line in lines[1:]:
    l = line.replace("\n","")
    l_list = l.split(",")
    lat.append(l_list[0])
    lon.append(l_list[1])
    ratio.append(l_list[2])
    size.append(f_size(l_list[2]))

df = pd.DataFrame(columns=headers)
df[headers[0]] = lat
df[headers[1]] = lon
df[headers[2]] = ratio
df[headers[3]] = size

# Making the csv
df.to_csv("beer_with_size_column.csv")
