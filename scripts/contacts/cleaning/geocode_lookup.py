# Makes one api call for a given address using Geocode Earth API


import re
import json
import urllib.request
import config


def get_address_info(address):
    """Creates an addresses from Geocode Earth responses.
    
    :param list addresses: An address
    :return: Json response of a Geocode Earth request
    :rtype: dict
    """

    if address.replace(" ","") != "":
        updated_address = re.sub('[^a-zA-z0-9 \n\.]', '', address)
        updated_address = updated_address.replace("\n", " ")
        url = ("https://api.geocode.earth/v1/search?" \
        "api_key="+config.geocode_api_key+"&"\
        "text=" + updated_address).replace(' ', '+').replace('\n', '+')
        response = json.load(urllib.request.urlopen(url))
        return response
    return address