#!/bin/bash
python dirty_to_clean.py $1 $2 $3 $4
python dirty_to_attribute_values.py $1 $2 $3 $4
python combine.py
