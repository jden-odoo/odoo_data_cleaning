# odoo_data_cleaning

## Assumptions
1. item column is in column A


## Usage

Sample :./cleaning.sh file parentlist childrenlist 
./cleaning.sh ../../data/dirtydata.csv a,d,l,m,n b,c,e,f,g,h,i,j,k
./cleaning2.sh ../../data/dirty2.csv a,c,d,l,m,n,q a i j
running type1 file : ./cleaning.sh filename parentlist childrenlist 

running type2 file: ./cleaning.sh filename parentlist productid attribute value 
