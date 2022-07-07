#############################################################################################
#Usage: python3 dirty_to_clean.py dirtydata.csv columns unit    
#Input (Space separated): 1: [dirtydata].csv, replace dirtydata with actual file name
#       2: letter of columns inputed in the following order: 
#         Name,Manufacturer,Collection,Color,Vendor_SKU,Designer,Fabric_Type,Fiber_Contents,Fabric Width,Putup_Format, Sales Price, Cost, Product Categry
#         for instance, in the example file DEV | 01 Client Dirty Data, input would be d,b,c,e,f,g,h,i,j,k,l,m,n (not case-sensitive)
#       3: unit needed, for instance: yard
#Commandline input example: python3 dirty_to_clean.py dirtydata.csv d,b,c,e,f,g,h,i,j,k,l,m,n yard


#Output: outputdata.csv                                                                                       



import csv
import sys

#TODO: CHANGE FILE PATHS FOR INPUT/OUTPUT


#############################################################################################
#input: data of inrows, and a comma separated list of the column letter of the fields in the following order :
#        [Name,Manufacturer,Collection,Color,Vendor_SKU,Designer,Fabric_Type,Fiber_Contents,Fabric Width,Putup_Format, Sales Price, Cost, Product Categry]
# for instance, in the example file DEV | 01 Client Dirty Data, input would be ['d','b','c','e','f','g','h','i','j','k','l','m','n'] (not case-sensitive)

#output: a dictionary of the following format:
# Dictionary:{Item: [Name,[(Manufacturer,value),
#                         (Collection,value),
#                         (Color,value),
#                         (Vendor_SKU,value),
#                         (Designer,value),
#                         (Fabric_Type,value),
#                         (Fiber_Contents,value),
#                         (Fabric Width,value),
#                         (Putup_Format,value)],
#                      [Sales Price, Cost, Product,Category]]}

def create_item_dict(inRows,columns):
    cols = []
    # converting columns in letter to index of array
    for letter in columns:
        
        cols.append(ord(letter.lower())-97)
    attributes = ['Manufacturer','Collection','Color','Vendor_SKU','Designer','Fabric_Type','Fiber_Contents','Fabric_Width','Putup_Format']
    item_dictionary = {}
    for item in inRows:
        data = []
        key = item[0]
        #looping through the attributes, add attribute and value to dictionary
        
        data.append(item[cols[0]])
        attr_pairs = []
        for i in range(0,len(attributes)):
            attr_pairs.append((attributes[i],item[cols[i+1]]))
        data.append(attr_pairs)
        extra_data = []
        for i in range(len(attributes)+1,len(cols)):
            extra_data.append(item[cols[i]])
        data.append(extra_data)
        item_dictionary[key] = data
    return item_dictionary


def output_clean_data(item_dict,outHeader,unit):
    f = open('../data/outputdata.csv','w')
    writer = csv.writer(f)
    writer.writerow(outHeader)
    for key in item_dict.keys():
        row = []
        item = item_dict[key]
        name = item[0]
        attributes = item[1]
        extra = item[2]
        row.append(key)
        row.append(name)
        (manu,val) = attributes[0]
        row.append(manu)
        row.append(val)
        for num in extra:
            row.append(num)
        row[-1] = unit
        writer.writerow(row)
        for i in range(1,len(attributes)):
            (manu,val) = attributes[i]
            temprow = ['','']
            temprow.append(manu)
            temprow.append(val)
            writer.writerow(temprow)
    f.close()

        
        
        
#Input: 1: '[dirtydata].csv', replace dirtydata with actual file name
#       2: letter of columns inputed in the following order: 
#         [Name,Manufacturer,Collection,Color,Vendor_SKU,Designer,Fabric_Type,Fiber_Contents,Fabric Width,Putup_Format, Sales Price, Cost, Product Categry]
#         for instance, in the example file DEV | 01 Client Dirty Data, input would be ['d','b','c','e','f','g','h','i','j','k','l','m','n'] (not case-sensitive)
#       3: unit needed, for instance: 'yard'


#Output: outputdata.csv
def main(dirtydata,columns,unit):
    csvname = dirtydata
    file = open(csvname)
    csvreader=csv.reader(file)
    inHeader = []
    inRows = []

    inHeader = next(csvreader)
    for row in csvreader:
        inRows.append(row)
    # print(inHeader)
    outHeader = ['Item', 'Name', 'Attribute', 'Value', 'Sales_Price', 'Cost', 'Product_Category']
    file.close()
    item_dict = create_item_dict(inRows,columns)
    output_clean_data(item_dict,outHeader,unit)

# main('dirtydata.csv',['d','b','c','e','f','g','h','i','j','k','l','m','n'],'yard')
arr = sys.argv[2].split(',')
main(sys.argv[1],arr,sys.argv[3])