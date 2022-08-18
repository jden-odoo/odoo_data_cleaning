# Gets Address1, Address2, City, State, Country, Zip 
# Uses Geocode Earth API for Address1, City, State, Country, Zip


import state_code_cleaning as sc


def get_address_1(response):
    """Gets address 1.
    
    :param dict response: Json response of an API output
    :return: Address 1
    :rtype: str
    """

    text = ""
    properties = response["features"][0]["properties"]
    house = False
    if "housenumber" in properties:
        text = text + properties["housenumber"]
        house = True
    if "street" in properties:
        if house:
            text = text + " "
        text = text + properties["street"]
    return text
    

def get_city(response):
    """Gets city.
    
    :param dict response: Json response of an API output
    :return: City
    :rtype: str
    """

    properties = response["features"][0]["properties"]
    if "locality" in properties:
        return properties["locality"]
    if "county_a" in properties:
        return properties["county_a"]
    return ""


def get_state(response, country, data):
    """Gets state.
    
    :param dict response: Json response of an API output
    :return: State
    :rtype: str
    """

    properties = response["features"][0]["properties"]
    if "region" in properties:
        temp = sc.match(properties["region"], country, data)
        if temp != "":
            return temp
    if "region_a" in properties:
        return properties["region_a"]
    return ""


def get_country(response):
    """Gets country.
    
    :param dict response: Json response of an API output
    :return: Country
    :rtype: str
    """

    properties = response["features"][0]["properties"]
    if "country" in properties:
        return properties["country"]
    if "country_a" in properties:
        return properties["country_a"]
    return ""


def get_post(response):
    """Gets postcode.
    
    :param dict response: Json response of an API output
    :return: Post code
    :rtype: str
    """

    properties = response["features"][0]["properties"]
    if "postalcode" in properties:
        return properties["postalcode"]
    return ""