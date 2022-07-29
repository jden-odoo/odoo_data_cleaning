# Creates address and formats into dictionary


import geocode_lookup as geo
import create_address_geocode_earth as ca
import create_address_geoapify as cr
import state_code_cleaning as sc

import re


# creates each value in the dictionary
def create_address(original, address, address_1, address_2, city, state_code, country_code, postal_code):
    """Creates an address dictionary given all values.

    :param str original: Original address
    :param str address: Formatted address from APIs
    :param str address_1: Address 1
    :param str address_2: Address 2
    :param str state_code: State code based on Odoo data
    :param str country_code: Country code based on Odoo data
    :param str postal_code: Postal code
    :return: An address containing all the values
    :rtype: dict
    """

    return {
        "original": original,
        "address": address,
        "address_1": address_1,
        "address_2": address_2,
        "city": city,
        "state": state_code,
        "country": country_code,
        "postcode": postal_code,
    }


# creates the dictionary
def create_address_list(original, addresses):
    """Creates a list of all address dictionaries.

    :param list original: List of original addresses
    :param list addresses: List of all json responses from Geoapify API
    :return: List of all formmated addresses
    :rtype: list
    """

    dict = []
    data = sc.create_dict()
    country_data = sc.country_dict()
    for response, og in zip(addresses, original):
        matches = ["match_by_city_or_disrict", "match_by_country_or_state", "match_by_postcode"]
        if response == "" or "results" not in response:
            dict.append(create_dict_entry_geocode_earth(og, response, data, country_data))
        elif not response["results"]:
            dict.append(create_dict_entry_geocode_earth(og, response, data, country_data))
        elif response["results"][0]["rank"]["match_type"] in matches:
            dict.append(create_dict_entry_geocode_earth(og, response, data, country_data))
        else:   
            dict.append(create_dict_entry_geoapify(og, response, data, country_data))
    return dict


def create_dict_entry_geoapify(og, response, data, country_data):
    """Reads geoapify data and parses it.
    
    :param str og: original address
    :param dict response: json of geoapify output
    :param dict data: state codes
    :param dict country_data: country codes
    :return: An address containing all values using Geoapify
    :rtype: dict
    """
    
    address_1 = cr.get_address1(response)
    address_2 = cr.get_address2(response)
    # address_2 = "temp"
    city = cr.get_city(response)
    country_name = cr.get_country(response)
    state = cr.get_state(response, country_name, data)
    country = sc.match_country(country_name, country_data)
    postcode = cr.get_postcode(response)
    return create_address(og, response["query"]["text"].upper(), address_1.upper(), address_2.upper(), city.upper(), state.upper(), country.upper(), postcode)


def create_dict_entry_geocode_earth(og, response, data, country_data):
    """Reads Geocode Earth data and parses it.
    
    :param str og: original address
    :param dict response: json of geoapify output
    :param dict data: state codes
    :param dict country_data: country codes
    :return: An address containing all values using Geocode Earth or Geoapify
    :rtype: dict
    """

    if og == "":
        return create_address(og, "","","","","","","")
    updated_address = re.sub('[^a-zA-z0-9- \n\.]', '', og)
    updated_address = updated_address.replace("\n", " ")

    new_response = geo.get_address_info(updated_address)
    if isinstance(new_response, str):
        return create_address(og, "","","","","","","")
    if new_response["features"]:
        temp = ca.get_address_1(new_response)
        address_1 = temp if temp != "" else cr.get_address1(response)
        address_2 = cr.get_address2(response)
        # address_2 = "other temp"
        temp = ca.get_city(new_response)
        city = temp if temp != "" else cr.get_city(response)
        temp = ca.get_country(new_response)
        country_name = temp if temp != "" else cr.get_country(response)
        temp = ca.get_state(new_response, country_name, data)
        state = temp if temp != "" else cr.get_state(response, country_name, data)
        country = sc.match_country(country_name, country_data)
        temp = ca.get_post(new_response)
        postcode = temp if temp != "" else cr.get_postcode(response)
        return create_address(og, new_response["features"][0]["properties"]["label"].upper(), address_1.upper(), address_2.upper(), city.upper(), state.upper(), country.upper(), postcode.upper())
    else:
        if response == "":
            return create_address(og, "","","","","","","")
        else:
            return create_dict_entry_geoapify(og,response, data, country_data)    