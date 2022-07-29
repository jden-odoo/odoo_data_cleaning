# Formats certain columns of a dataframe into one list of addresses
# Converts a dictionary address to a 2D list


import pandas as pd


# gets all addresses from dirty data based on given letter indexes
def get_all_addresses(index, df):
    rows = len(df)
    data = []
    for i in range(rows):
        data.append("")
    for i in index:
        actual = get_value(i.lower())
        for r in range(rows):
            p2 = df.iloc[r,actual]
            if not (isinstance(p2, str)):
                p2 = ""
            data[r] = str(data[r]) + str(p2) + " "
    new_df = pd.DataFrame(data, columns=["Addresses"])
    return new_df.iloc[:,0]


# returns address dictionary as a 2d list
def get_address_list(addresses):
    data = []
    for address in addresses:
        data.append([address["original"], address["address"], address["address_1"], address["address_2"], address["city"], address["state"], address["country"], address["postcode"]])
    data.pop(0)
    return data


# converts value of csv column to an index
# ex. A -> 0, AA -> 27
def get_value(value):
    total = 0
    count = 0
    value = value.lower()
    while len(value) != 0:
        total += (ord(value[len(value)-1])-96) * pow(26,count)
        value = value[0:len(value)-1]
        count = count + 1
    return total-1