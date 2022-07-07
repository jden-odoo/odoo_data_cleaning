import pandas as pd


display_type = "Radio"
create_variant = "Instantly"
visibility = "Visible"
company_name = "ABA company"


# Gets dirty data from dirty data csv
def get_dirty_data():
    return pd.read_csv('../../data.csv', thousands=',')


# Returns list of column names ordered by dirty data csv
def list_names(dirty_data):
    return dirty_data.columns


# Get input names (case insensisitive)
# Future implementation will be drop down XML
def get_names():
    column_letters = ['b', 'c', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    res = []
    for col in column_letters:
        col = col.lower()
        res.append(ord(col))
    return res


# Get corresponding names for letter columns
def get_corresponding_names(names_list, dirty_data):
    names = []
    all_names = dirty_data.columns
    for i in range(len(all_names.tolist())):
        if (i + 97) in names_list:
            names.append(all_names[i])
    return names


# Create ids for name_list
def get_ids(name_list):
    ids_list = []
    for cell in name_list:
        if cell in ids_list and cell != " ":
            ids_list.append(" ")
        else:
            ids_list.append(company_name.lower()[:2] + "-" + cell.lower())
    return ids_list


# Get value_id/name from dirty data
def get_value_id_name(column_name, dirty_data):
    value_id_names = []
    for value in dirty_data[column_name].tolist():
        if value not in value_id_names:
            value_id_names.append(value)
    return value_id_names


# Creates a csv for the output
def create_csv(df):
    df.to_excel(excel_writer = './data/attr-val-test.xlsx')


# Create the data to be added to the new dataframe for the output csv
# Creates value_id/id
# Appends values into the data and returns a dataframe with data
def create():
    dirty_data = get_dirty_data()
    #print(dirty_data.iloc[:, 5][4073])
    names_list = get_names()
    names_list_words = get_corresponding_names(names_list, dirty_data)
    ids_list = get_ids(names_list_words)
    data = []
    count = 0
    for name in names_list_words:
        value_id_names = get_value_id_name(name, dirty_data)
        id_num = 1
        prev = ""
        for value in value_id_names:
            if not isinstance(value, str):
                continue
            value_id_id = name.lower() + "_" + str(id_num)
            id_num = id_num + 1
            if prev == name:
                data.append(["","","","","",value,value_id_id])
            else:
                data.append([name, ids_list[count], display_type, create_variant, visibility, "\"" + value + "\"", value_id_id.lower()])
            prev = name
        count = count + 1
    df = pd.DataFrame(data, columns=["name", "id", "display_type", "create_variant", "visibility", "value_id/name", "value_id/id"]).set_index('name')
    #print(df.iloc[:, 4][1538])
    return df


# Creates csv for dataframe
def parse():
    df = create()
    create_csv(df)


parse()