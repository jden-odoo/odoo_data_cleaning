# INPUT: python3 main.py dirty_data columns
#
# SAMPLE INPUT: python3 main.py ../../../data/full.csv d,e,f


import pandas as pd
import csv_parsing as cs
import geoapify_lookup as api
import formatting as fm
import assemble as asse

import sys


def main(dirty_data, address_columns):
    df = cs.read_data(dirty_data)
    all_addresses = fm.get_all_addresses(address_columns, df)
    addresses_responses = api.get_address_info(all_addresses)
    addresses_dict = asse.create_address_dict(all_addresses, addresses_responses)
    addresses_list = fm.get_address_list(addresses_dict)
    new_df = pd.DataFrame(addresses_list, columns=["Original Address", "Formatted Address", "Street1", "Street2", "City", "State", "Country", "Postal Code"]).set_index("Original Address")
    cs.create_csv(new_df, dirty_data)


dirty_data = sys.argv[1]
address_columns = sys.argv[2].split(",")
main(dirty_data, address_columns)