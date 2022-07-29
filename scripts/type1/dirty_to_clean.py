#############################################################################################
#Usage: python3 dirty_to_clean.py dirtydata.csv parentcolumns children collumns (space separated)
# Input (Space separated): 1: [dirtydata].csv, replace dirtydata with actual file name
#       2: letter of parent columns 
#         for instance, in the example file DEV | 01 Client Dirty Data, input would be d,b,c,e,f,g,h,i,j,k,l,m,n (not case-sensitive)
#       3: letter of children columns
#Commandline input example: python3 dirty_to_clean.py dirtydata.csv d,b,c,e,f,g,h,i,j,k,l,m,n a,o

#Output: outputdata.csv                                                                                       



import csv
import sys
import pandas as pd
#TODO: CHANGE FILE PATHS FOR INPUT/OUTPUT

 
#############################################################################################
#Reads from a hard coded excel file path and returns a dictionary that stores the value/id pairs

def create_attr_val_dict():


    #Testing
    attr_val_df = pd.read_excel('../data/attr-val.xlsx')

    attr_val_dict = {}
    currDict = {}
    currCategory = None

    for row in range(0, len(attr_val_df)): 
        if not pd.isna(attr_val_df['name'][row]):  
            if currCategory:
                attr_val_dict[currCategory] = currDict
            currCategory = str(attr_val_df['name'][row]).replace(' ','_').lower() #Replace space with underscore for consistency
            currDict = {}

        currDict[str(attr_val_df['value_ids/name'][row]).replace(' ','_').lower()] = str(attr_val_df['value_ids/id'][row])

    if currCategory:
        attr_val_dict[currCategory] = currDict

    return attr_val_dict
#############################################################################################
#input: headers from the input file, data of the rest of the rows, and the parents and children column numbers
#output: a dictionary of the following format:
# Dictionary:{ItemName: [parentVal1, parentVal2,...]

def create_item_dict(inHeader,inRows,parents,children):
    parent_cols = []
    children_cols = []
    # converting columns in letter to index of array
    for letter in parents:
        
        parent_cols.append(ord(letter.lower())-97)
    for letter in children:
        
        children_cols.append(ord(letter.lower())-97)
    attributes = []
    for col in children_cols:
        attributes.append(inHeader[col])
    item_set = []
    for item in inRows:
        data = []
        for i in parent_cols:
            data.append(item[i])
            
        #looping through the attributes, add attribute and value to dictionary
        
        attr_pairs = []
        #cleaning all the input strings, and replacing spaces with underscores, converting to lowercase for all letters
        for i in range(0,len(attributes)):
            attr_pairs.append((str(attributes[i]).replace(' ','_').lower(),str(item[children_cols[i]]).replace(' ','_').lower() ))
        data.append(attr_pairs)
        item_set.append(data)
    return item_set


#input: item_set: dictionary consisting of item name as key and parent col values as value
#       outHeader: the selected header from the original input file that should go into the output
#       id_dict: dictionary consists of the attribute name as key and the id as value
#output: writing to outputdata.csv for a clean output
def output_clean_data(item_set,outHeader,id_dict):
    f = open('../data/outputdata.csv','w')
    writer = csv.writer(f)
    writer.writerow(outHeader)
    count = 0
    for item in item_set:
        row = []
        parents = item[0:-1]
        parent_len = len(parents)
        attributes = item[-1]
        attr_len = len(attributes)
        attr_start = 0
        for val in parents:
            row.append(val)
        
        if len(attributes) > 0:
            
            attr0,val0 = attributes[attr_start]
            
            while val0 == '' and attr_start < attr_len:
                attr_start+=1
                attr0,val0 = attributes[attr_start]

            if val0 != '':
                row.append("attribute_"+str(attr0).replace(' ','_').lower())
                row.append(id_dict[attr0][val0])
        
        writer.writerow(row)
        count+=1
        
        
        for i in range(attr_start+1,len(attributes)):
            attr,val = attributes[i]
            #skipping empty value rows
            if val == '':
                continue
            temprow = []
            for j in range(parent_len):
                temprow.append('')
            temprow.append("attribute_"+str(attr).replace(' ','_').lower())
            temprow.append(id_dict[attr][val])
            writer.writerow(temprow)
            count+=1
    f.close()
        
        

        
        
        
#Input: 1: '[dirtydata].csv', replace dirtydata with actual file name
#       2: letter of parent columns in a comma separated list
#         for instance, in the example file DEV | 01 Client Dirty Data, input would be ['d','b','c','e','f','g','h','i','j','k','l','m','n'] (not case-sensitive)
#       3: letter of children columns in a comma separated list

#Output: outputdata.csv
def main(dirtydata,parents,children):
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
    item_set = create_item_dict(inHeader,inRows,parents,children)
    id_dict = create_attr_val_dict()
    output_clean_data(item_set,outheader,id_dict)


# main(sys.argv[1],sys.argv[2].split(','),sys.argv[3].split(','))   
