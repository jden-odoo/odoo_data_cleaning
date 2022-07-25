#!/bin/bash

python /home/leo/odoo/dev/odoo_data_cleaning/scripts/type1/dirty_to_attribute_values.py $1 $2 $3 $4
python /home/leo/odoo/dev/odoo_data_cleaning/scripts/type1/dirty_to_clean.py $1 $2 $3 $4
##python combine.py
