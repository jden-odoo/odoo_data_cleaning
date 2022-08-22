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

Standalone
./cleaning.sh ../../data/dirtydata.csv a,d,l,m,n b,c,e,f,g,h,i,j,k
./cleaning2.sh ../../data/dirty2.csv a,c,d,l,m,n,q a i j
running type1 file : ./cleaning.sh filename parentlist childrenlist 
running type2 file: ./cleaning.sh filename parentlist productid attribute value 
This will generate the files called attr-val.xlsx and output.csv in the ../data directory.
These can then imported into odoo.

External Page
To use the external page front end, simply cd into the external page folder, use the command 'export FLASK_APP=server', and then 'flask run'.
This supports both file types.

Odoo Module
If this repo is installed as a module, it will overwrite the existing Odoo import tool. 
To use it, upload the dirty data and match the parent columns with their fields and the child columns with the option "child column" in the ui. Fill in the information in the bottom left required for importing into a database. 
This importing method only supports type 1 csv files.

Type 1 file example
Item,Manufacturer,Collection,Name,Color,Vendor_SKU,Designer,Fabric_Type,Fiber_Contents,Fabric_Width,Putup_Format, Sales Price , Cost ,Product Category
BD-17632-B01-15,Santee Print Works,Tone on Tone,Tone on Tone - White - 15-yard bolt,White,Card 8 - 17632-W/W,,Cotton,100% Cotton,"45"" wide",D/R, $ 49.20 , $ 27.75 ,Units
BD-17632-B01-13.25,Santee Print Works,Tone on Tone,Tone on Tone - White - 13.25-yard bolt,White,Card 8 - 17632-W/W,,Cotton,100% Cotton,"45"" wide",D/R, $ 43.46 , $ 24.51 ,Units
BD-17632-B01-13.125,Santee Print Works,Tone on Tone,Tone on Tone - White - 13.125-yard bolt,White,Card 8 - 17632-W/W,,Cotton,100% Cotton,"45"" wide",D/R, $ 43.05 , $ 24.28 ,Units
BD-17632-B01-12.625,Santee Print Works,Tone on Tone,Tone on Tone - White - 12.625-yard bolt,White,Card 8 - 17632-W/W,,Cotton,100% Cotton,"45"" wide",D/R, $ 41.41 , $ 23.36 ,Units
BD-17632-B01-12.25,Santee Print Works,Tone on Tone,Tone on Tone - White - 12.25-yard bolt,White,Card 8 - 17632-W/W,,Cotton,100% Cotton,"45"" wide",D/R, $ 40.18 , $ 22.66 ,Units
BD-17632-B01-11.875,Santee Print Works,Tone on Tone,Tone on Tone - White - 11.875-yard bolt,White,


Type 2 file
Product ID,Variant ID,Product Name,Product Type,Product Description,Supplier,Brand,Tags,Attributes,Values,Barcode,Sellable,Purchasable,Taxable,Buy Price,Retail Price,Type
28025381,47279983,CBDfx - CBD Oil Vape Additive,CBD,"This CBD oil vape additive contains up to 500mg of 100% organically grown cannabidiol. Our CBD is CO2 extracted from the highest quality, organically grown and EU sourced hemp. This proprietary blend of VG/PG mixture can be vaped, or taken orally as a CBD tincture. Our liquid carries the leafy, tea-like flavor profile of the natural hemp plant and pairs nicely with dessert and fruit-flavored e-liquids. CBDfx’s vape oil additive mixes easily with your favorite e-juice with the included dropper. With our vape additive, you get the convenience of using your favorite vape gear while gaining the ability to dose CBD. CBDfx’s vape additive is cGMP certified and made in the USA. CBD is also rich in Omega-3 fatty acids.",CBDfx,CBDfx,"CBD,CBDfx,Tincture",CBD Level,120MG,2.1E+11,TRUE,TRUE,7%,7.51,35.99,Storable Product
28025381,47279984,CBDfx - CBD Oil Vape Additive,CBD,"This CBD oil vape additive contains up to 500mg of 100% organically grown cannabidiol. Our CBD is CO2 extracted from the highest quality, organically grown and EU sourced hemp. This proprietary blend of VG/PG mixture can be vaped, or taken orally as a CBD tincture. Our liquid carries the leafy, tea-like flavor profile of the natural hemp plant and pairs nicely with dessert and fruit-flavored e-liquids. CBDfx’s vape oil additive mixes easily with your favorite e-juice with the included dropper. With our vape additive, you get the convenience of using your favorite vape gear while gaining the ability to dose CBD. CBDfx’s vape additive is cGMP certified and made in the USA. CBD is also rich in Omega-3 fatty acids.",CBDfx,CBDfx,"CBD,CBDfx,Tincture",CBD Level,300MG,2.1E+11,TRUE,TRUE,7%,24.18,44.99,Storable Product
28025381,47279985,CBDfx - CBD Oil Vape Additive,CBD,"This CBD oil vape additive contains up to 500mg of 100% organically grown cannabidiol. Our CBD is CO2 extracted from the highest quality, organically grown and EU sourced hemp. This proprietary blend of VG/PG mixture can be vaped, or taken orally as a CBD tincture. Our liquid carries the leafy, tea-like flavor profile of the natural hemp plant and pairs nicely with dessert and fruit-flavored e-liquids. CBDfx’s vape oil additive mixes easily with your favorite e-juice with the included dropper. With our vape additive, you get the convenience of using your favorite vape gear while gaining the ability to dose CBD. CBDfx’s vape additive is cGMP certified and made in the USA. CBD is also rich in Omega-3 fatty acids.",CBDfx,CBDfx,"CBD,CBDfx,Tincture",CBD Level,500MG,2.1E+11,TRUE,TRUE,7%,30.23,54.99,Storable Product


