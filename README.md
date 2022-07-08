# odoo_data_cleaning

## Assumptions
1. item column is in column A


## Usage
Input (Space separated): 
    1: [dirtydata].csv, replace dirtydata with actual file name
    2: letter of columns inputed in the following order: 
        Name,Manufacturer,Collection,Color,Vendor_SKU,Designer,Fabric_Type,Fiber_Contents,Fabric Width,Putup_Format, Sales Price, Cost, Product Categry
        for instance, in the example file DEV | 01 Client Dirty Data, input would be d,b,c,e,f,g,h,i,j,k,l,m,n (not case-sensitive)
    3: company name
    4: unit needed, for instance: yard
Sample input: ./cleaning.sh dirtydata.csv d,b,c,e,f,g,h,i,j,k,l,m,n odoo yard
