from flask import Flask, current_app, request, redirect, url_for, flash, session, render_template
from xmlrpc import client
import re
import json
import io
import os
import pandas as pd
from werkzeug.utils import secure_filename
from import_script import ExternalImport
import importlib.util
import sys


ALLOWED_EXTENSIONS = {'xlsx','csv', 'xls'}
#export FLASK_APP=server
app = Flask(__name__)
app.secret_key='much super such wow'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = '../data'


@app.route("/", methods=["GET", "POST"]) #type="json" TODO
def clean_data():
    """
    get route sends home page
    post route cleans the data that was uploaded and redirects to the validation page
    """
    if request.method == "GET":
        return render_template('index.html')
    else:
        pattern = re.compile(r"^(\w+)(,\s*\w+)*$") #regex to check if input is comma seperated list TODO: fix this regex, regex is incorrect
        parent_columns = request.form['parent_columns']
        children_columns = request.form['children_columns']
        if pattern.match(parent_columns) == None or pattern.match(children_columns) == None:
            print('Error: not properly matched')
            #TODO: add error raising

        url = request.form['url']
        db = request.form['db']
        password = request.form['api_key']
        user = request.form['username']
        model = request.form['model']
    

        #Storing for later
        session['url'] = url
        session['db'] = db
        session['password'] = password
        session['user'] = user
        session['model'] = model

        #Validate the user input for api access credentials
        common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, user, password, {})
        models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        
        if 'data_file' not in request.files:
            print('No file part')
            return redirect(url_for('clean_data'))
        file = request.files['data_file']
        if file.filename == '':
            print('No selected file')
            return redirect(url_for('clean_data'))
        if file and allowed_file(file.filename):
            print('file found')
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            fileType = request.form['type']
            if fileType == '1':
                parseArgs(file_path, parent_columns, children_columns,0,0,0,fileType)
            elif fileType == '2':  
                attribute = request.form['attribute']
                value = request.form['value']
                productid = request.form['productid']
                parseArgs(file_path, parent_columns, children_columns,productid,attribute,value,fileType)
            
            
            output_df = pd.read_csv('../data/outputdata.csv')
            matched = []
            columns = list(output_df.columns)
            columns.remove("Attribute")
            columns.remove("Value")

            model_fields = models.execute_kw(db, uid, password, model, 'fields_get', [])

            importable_fields = []  
            for field in model_fields.keys():
                if not model_fields[field]['readonly']:
                    importable_fields.append(field)

            for col in columns:
                col_match = "False"
                for field in importable_fields:          
                    if model_fields[field]['string'].lower().strip() == col.lower().strip():
                        print(col, ',', field)
                        col_match = field
                        break
                matched.append(col_match)

            data = {
                "importable_fields": importable_fields, #KEYS MUST BE DOUBLE QUOTE
                "columns": columns,
                "matched": matched
            }
            data = json.dumps(data)
            return redirect(url_for('validate_columns', data = data))


@app.route("/validate", methods=["GET", "POST"])
def validate_columns():
    """
    get route sends the validation page that allows user to match the columns with the model fields
    post route imports the data into the database
    """
    if request.method == "GET":
        return current_app.send_static_file("validate.html")
    else:
        print(request.form)
        fields = []
        columns = []
        for key in request.form.keys():
            columns.append(key.lower().strip())
            fields.append(request.form[key].lower().strip())
        importer = ExternalImport()
        importer.main(session['user'], session['password'], session['db'], session['url'], fields, columns, session['model'])

        #TODO: add return page

    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#running type1 file : ./cleaning.sh filename parentlist childrenlist 
# running type2 file: ./cleaning.sh filename parentlist productid attribute value 

def parseArgs(filename, parent_columns, children_columns,productid,attribute,value,fileType):
    print('parseargs called')
    parentlist = parent_columns.split(',')
    childrenlist = children_columns.split(',')
    if fileType == '1':
        #running dirty to attribute
        spec1 = importlib.util.spec_from_file_location("dirty_to_attribute_values", "../scripts/type1/dirty_to_attribute_values.py")
        foo1 = importlib.util.module_from_spec(spec1)
        spec1.loader.exec_module(foo1)
        print(filename)
        foo1.parse(childrenlist,filename)

        #running dirty to clean
        spec2 = importlib.util.spec_from_file_location("dirty_to_clean", "../scripts/type1/dirty_to_clean.py")
        foo2 = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(foo2)
        foo2.main(filename, parentlist,childrenlist)

    elif fileType == '2':
        spec1 = importlib.util.spec_from_file_location("dirty_to_attribute_values_2", "../scripts/type2/dirty_to_attribute_values_2.py")
        foo1 = importlib.util.module_from_spec(spec1)
        spec1.loader.exec_module(foo1)
        foo1.main(filename,attribute,value)

        #running dirty to clean
        spec2 = importlib.util.spec_from_file_location("dirty_to_clean_2", "../scripts/type2/dirty_to_clean_2.py")
        foo2 = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(foo2)
        foo2.main(filename,parentlist,productid,attribute,value)