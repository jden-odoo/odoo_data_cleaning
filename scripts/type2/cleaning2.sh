#!/bin/bash
#   USE ARGUMENTS IN THE FOLLOWING ORDER: ./cleaning.sh filename parentlist producttemplateid attribute value 
# EXAMPLE: ./cleaning2.sh ../../data/dirty2.csv a,c,d,l,m,n,q a i j
echo "working shell"
python dirty_to_attribute_values_2.py $1 $2 $3 $4 $5
python dirty_to_clean_2.py $1 $2 $3 $4 $5
##python combine.py