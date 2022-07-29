# Makes an api call for each address in a list using Geoapify API


import json
import requests
import re

import urllib.request
import config


# returns address info as a dictionary
def get_address_info(addresses):
    temp = []
    for address in addresses:
        if address.replace(" ","") != "":
            updated_address = re.sub('[^a-zA-z0-9- \n\.]', '', address)
            updated_address = updated_address.replace("\n", " ")
            url = ("https://api.geoapify.com/v1/geocode/search?"\
            "text=" + updated_address + "&format=json&"\
            "apiKey=" + config.geoapify_api_key).replace(' ', '%20').replace('\n', '%')
            response = json.load(urllib.request.urlopen(url))
            temp.append(response)
        else:
            temp.append("")
    return temp