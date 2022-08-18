# Gets Address1, Address2, City, State, Country, Zip 
# Uses Geoapify API for Address1, City, State, Country, Zip
# Uses Postgrid API for Address2


import requests
import config
import state_code_cleaning as sc


def get_address1(response):
    """Gets address 1.
    
    :param dict response: Json response of an API output
    :return: Address 1
    :rtype: str
    """

    if response["results"]:
        results = response["results"][0]
        if "housenumber" in results or "street" in results:
            temp = ""
            house = False
            if "housenumber" in results:
                temp = temp + results["housenumber"]
                house = True
            if "street" in results:
                if house:
                    temp = temp + " "
                temp = temp + results["street"]
            return temp
    if response["query"]:
        if "parsed" not in response["query"]:
            return ""
        query = response["query"]["parsed"]
        if "housenumber" in query or "street" in query:
            temp = ""
            if "housenumber" in query:
                temp = temp + query["housenumber"]
            if "street" in query:
                temp = temp + query["street"]
            return temp
        if "house" in query:
            return query["house"]
    return ""


def get_address2(response):
    """Gets address 2.
    
    :param dict response: Json response of an API output
    :return: Address 2
    :rtype: str
    """

    url = "https://api.postgrid.com/v1/addver/parses"

    payload='address=' + response["query"]["text"]
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-api-key': config.postgrid_api_key,
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    result = response.json()
    if "unit" in result["data"]:
        return result["data"]["unit"] 
    if "level" in result["data"]:
        return result["data"]["level"] 
    if "poBox" in result["data"]:
        return result["data"]["poBox"]
    return ""


def get_city(response):
    """Gets city.
    
    :param dict response: Json response of an API output
    :return: City
    :rtype: str
    """

    if response["results"]:
        if "city" in response["results"][0]:
            return response["results"][0]["city"]
    if response["query"]:
        if "parsed" not in response["query"]:
            return ""
        if "city" in response["query"]["parsed"]:
            return response["query"]["parsed"]["city"]
    return ""


def get_state(response, country, data):
    """Gets state.
    
    :param dict response: Json response of an API output
    :return: State
    :rtype: str
    """

    if response["results"]:
        results = response["results"][0]
        if "state" in results:
            temp = sc.match(results["state"], country, data)
            if temp != "":
                return temp
        if "state" + "_code" in results:
            return results["state" + "_code"]
        
    if response["query"]:
        if "parsed" not in response["query"]:
            return ""
        query = response["query"]["parsed"]
        if "state" in query:
            temp = sc.match(results["state"], country, data)
            if temp != "":
                return temp
    return ""


def get_country(response):
    """Gets country.
    
    :param dict response: Json response of an API output
    :return: Country
    :rtype: str
    """

    if response["results"]:
        results = response["results"][0]
        if "country" in results:
            return results["country"]
        if "country" + "_code" in results:
            return results["country" + "_code"]
        
    if response["query"]:
        if "parsed" not in response["query"]:
            return ""
        query = response["query"]["parsed"]
        if "country" in query:
            return query["value"]
    return ""


def get_postcode(response):
    """Gets postcode.
    
    :param dict response: Json response of an API output
    :return: Post code
    :rtype: str
    """

    if response["results"]:
        if "postcode" in response["results"][0]:
            return response["results"][0]["postcode"]
    if response["query"]:
        if "parsed" in response["query"]:
            if "postcode" in response["query"]["parsed"]:
                return response["query"]["parsed"]["postcode"]
    return ""