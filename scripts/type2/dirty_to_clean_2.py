import csv
import sys
import pandas as pd


#############################################################################################

# create_attr_val_dict() will return dictionary of the following format:
# {
#     'color_of_car_body', {
#         'attribute_external_id': 'car_body_color',
#         'values': {
#             'white': 'car_body_white',
#             'green': 'car_body_green'
#         }
#     }
#     'color_of_car_trim', {
#         'attribute_external_id': 'car_trim_color'
#         'values': {
#             'white': 'car_trim_white',
#             'green': 'car_trim_green'
#         }
#     }
# }

def create_attr_val_dict():

    attr_val_df = pd.read_excel('../data/attr-val.xlsx')

    attr_val_dict = {}
    curr_attribute = None

    for row in range(0, len(attr_val_df)):
        if not pd.isna(attr_val_df['name'][row]):            
            curr_attribute = str(attr_val_df['name'][row]).replace(' ','_').lower()
            attr_val_dict[curr_attribute] = {}
            attr_val_dict[curr_attribute]['attribute_external_id'] = attr_val_df['id'][row]
            attr_val_dict[curr_attribute]['values'] = {}

        curr_val_name = str(attr_val_df['value_ids/name'][row]).replace(' ', '_').lower()
        curr_val_external_id = str(attr_val_df['value_ids/id'][row])
        
        attr_val_dict[curr_attribute]['values'][curr_val_name] = curr_val_external_id

    return attr_val_dict

#create the id_dictionary to keep track of the attribute and value ids
def create(inRows, id, attributes, values):
    # {Product ID: {Attributes: [Value1, Value2]}}
    id = ord(id.lower())-97
    attributes = ord(attributes.lower())-97
    values = ord(values.lower())-97
    id_dict = {}
    for row in inRows:
        productID = row[id]
        attr = row[attributes]
        val = row[values]
        if not attr or not val:
            continue
        if productID in id_dict:
            if attr in id_dict[productID]:
                
                id_dict[productID][attr].append(val)
            else:
                id_dict[productID][attr] = [val]
        else:
            temp = {}
            temp[attr] = [val]
            id_dict[productID] = temp
    return id_dict
#############################################################################################
# input: the headers of the input, the rest of the csv data in inRows, parent column letters as passed in arguments, and product_id column letter
# output: dictionary that contains the product id as key and the list of parent column values as value
# dict = {productID:[parent1,parent2,....,
        #             
        #         ]

def create_item_dict(inHeader,inRows,parents,product_id):
    parent_cols = []
    product_id_col = ord(product_id.lower())-97

    # converting columns in letter to index of array
    for letter in parents:
        parent_cols.append(ord(letter.lower())-97)

    item_dict = {}
    for item in inRows:
        data = []
        key = item[product_id_col]
        if key in item_dict:
            continue
        elif key not in item_dict:
            for i in parent_cols:
                data.append(item[i])
            item_dict[key] = data
            
        #looping through the attributes, add attribute and value to dictionary
        
       
    return item_dict


#id_dict: {Product ID: {Attributes : [Value1, Value2]}}
# writing clean data to the output, ensures that the attribute and value column are to the right most of the output file,
# if for some attribute, there are more than one values, ensures they are in a comma separated string 
def output_clean_data(item_dict,outHeader,id_dict,val_to_id):
    f = open('../data/outputdata.csv','w')
    writer = csv.writer(f)
    writer.writerow(outHeader)
    for key in item_dict.keys():
        item = item_dict[key]
        if key in id_dict:
            attributes = id_dict[key]
        else:
            row = item.copy()
            writer.writerow(row)
            continue
        length = len(item)
        row = item.copy()

        for attr in attributes.keys():
            vals = attributes[attr]
            for i in range(len(vals)):
                
                val = val_to_id[str(attr).replace(' ','_').lower()]['values'][str(vals[i]).replace(" ", "_").lower()]
                vals[i] = val
            temp = ','.join(vals)
            row.append( "attribute_" + str(attr).replace(" ", "_").replace(".", "_").lower())
            row.append(temp)
            attributes.pop(attr)
            break
            
        writer.writerow(row)
        for attr in attributes.keys():
            row = []
            vals = attributes[attr]
            for i in range(len(vals)):
                
                val = val_to_id[str(attr).replace(' ','_').lower()]['values'][str(vals[i]).replace(" ", "_").lower()]
                vals[i] = val
            temp = ','.join(vals)
            for i in range(length):
                row.append('')
            row.append("attribute_" + str(attr).replace(" ", "_").replace(".", "_").lower())
            row.append(temp)
            writer.writerow(row)

 
    f.close()
        
        
        

        
        
        
#Input: 1: '[dirtydata].csv', replace dirtydata with actual file name
#       2: parentlist (list of parent column letters)
#       3: productid (column letter of product id)
#       4: attribute (column letter of attribute)
#       5: value    (column letter of value)

#Output: outputdata.csv
def main(dirtydata,parents,product_id,attributes,values):
    csvname = dirtydata
    file = open(csvname)
    csvreader=csv.reader(file)
    inHeader = []
    inHeader = next(csvreader)
    inRows = []
    parent_cols = []
    outheader = []
    # converting columns in letter to index of array
    for letter in parents:
        parent_cols.append(ord(letter.lower())-97)
 
    for row in csvreader:
        inRows.append(row)
    for i in parent_cols:
        outheader.append(inHeader[i]) 
    outheader.append('Attribute')
    outheader.append('Value')
    file.close()
    item_set = create_item_dict(inHeader,inRows,parents,product_id)
    id_dict = create(inRows, product_id, attributes, values)
    val_to_id = create_attr_val_dict()

    output_clean_data(item_set,outheader,id_dict,val_to_id)
# main(sys.argv[1],sys.argv[2].split(','), sys.argv[3],sys.argv[4],sys.argv[5])

