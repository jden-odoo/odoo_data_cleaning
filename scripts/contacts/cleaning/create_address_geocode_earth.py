# Gets Address1, Address2, City, State, Country, Zip 
# Uses Geocode Earth API for Address1, City, State, Country, Zip
# Uses Postgrid API for Address2


import state_code_cleaning as sc


# housenumber + street -> none
def get_address_1(response):
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
    

# locality -> county_a -> none
def get_city(response):
    properties = response["features"][0]["properties"]
    if "locality" in properties:
        return properties["locality"]
    if "county_a" in properties:
        return properties["county_a"]
    return ""


# region_a -> region -> none
def get_state(response, country, data):
    properties = response["features"][0]["properties"]
    if "region" in properties:
        temp = sc.match(properties["region"], country, data)
        if temp != "":
            return temp
    if "region_a" in properties:
        return properties["region_a"]
    return ""


# country_a -> country -> none
def get_country(response):
    properties = response["features"][0]["properties"]
    if "country" in properties:
        return properties["country"]
    if "country_a" in properties:
        return properties["country_a"]
    return ""


# postalcode -> none
def get_post(response):
    properties = response["features"][0]["properties"]
    if "postalcode" in properties:
        return properties["postalcode"]
    return ""