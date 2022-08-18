# odoo_data_cleaning
## Task ID: 2870227
## Desription
The module consists of then follwing 3 main folders:
### Scripts
Scripts in this folder take in dirty csv files and generate two clean output data files: outputdata.csv and attr-val.csv
#### type1
Parses files where input's attributes are dispersed in many different columns, passed in as children list
#### type2
Parse files where input's attributes are listed in multiple different rows.

### Models
This folder includes an odoo module that overides the original odoo poduct.template import tool. Will be improved in the coming weeks to become a standalone import module

### external_page

This folder contains the custom temporary front end and backend that's able to complete the entire pipeline of cleaning and parsing. By simply uploading the dirty csv fe and matching the fields to the odoo internal importable fields, the backend automatically parses and imports the entire file
## Usage

./cleaning.sh ../../data/dirtydata.csv a,d,l,m,n b,c,e,f,g,h,i,j,k
./cleaning2.sh ../../data/dirty2.csv a,c,d,l,m,n,q a i j
running type1 file : ./cleaning.sh filename parentlist childrenlist 

running type2 file: ./cleaning.sh filename parentlist productid attribute value 

To use the external page front end, simply cd into the external page folder, use the command 'export FLASK_APP=server', and then 'flask run'.
