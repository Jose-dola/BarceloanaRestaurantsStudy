
import gmapsdatalib as gmd

"""
This script requests the information of all restaurants as dictionaries using the google maps API. 
The google maps id of each restaurant that wants to be requested is stored in files (list_of_ids.txt, list_of_ids2.txt). 
Each restaurant dictionary is stored in a different .pkl file inside a folder ("ids_full_info).
"""

files = ["list_of_ids.txt","list_of_ids2.txt"]
ids = gmd.get_unique_ids_from_files(files)
API_key = "YOUR_API_KEY"
error_ids = gmd.data_from_ids_to_files(ids, "ids_full_info", API_key)