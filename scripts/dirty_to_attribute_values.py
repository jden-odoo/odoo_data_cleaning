import pandas as pd


display_type = "Radio"
create_variant = "Instantly"
visibility = "Visible"
company_name = "ABA company"


def get_dirty_data():
    return pd.read_csv('../../data.csv')


#in order of dirty data
def list_names(dirty_data):
    return dirty_data.columns


#input will be correct case from xml
def get_names():
    names = input("Enter all column names separated by space").split(" ")
    return names


def get_ids(name_list):
    ids_list = []
    for cell in name_list:
        if cell in ids_list and cell != " ":
            ids_list.append(" ")
        else:
            ids_list.append(company_name.lower()[:2] + "-" + cell.lower())
    return ids_list


def get_value_id_name(column_name, dirty_data):
    value_id_names = []
    for value in dirty_data[column_name].tolist():
        if value not in value_id_names:
            value_id_names.append(value)
    return value_id_names


def create_csv(df):
    df.to_csv('./data/attr-val.csv', sep='\t', encoding='utf-8')


def create():
    dirty_data = get_dirty_data()
    names_list = get_names()
    ids_list = get_ids(names_list)
    data = []
    count = 0
    for name in names_list:
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
                data.append([name, ids_list[count], display_type, create_variant, visibility, value, value_id_id.lower()])
            prev = name
        count = count + 1
    df = pd.DataFrame(data, columns=["name", "id", "display_type", "create_variant", "visibility", "value_id/name", "value_id/id"]).set_index('name')
    return df


def parse():
    df = create()
    create_csv(df)


parse()