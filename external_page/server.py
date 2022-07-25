from flask import Flask, current_app, request, redirect, url_for, flash
from xmlrpc import client
import re
import json
import io
import os
import pandas as pd
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'xlsx','csv', 'xls'}
#export FLASK_APP=server
app = Flask(__name__)
app.secret_key='much super such wow'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = '../data'


@app.route("/", methods=["GET", "POST"]) #type="json" TODO
def clean_data():
    if request.method == "GET":
        return current_app.send_static_file('index.html')
    else:
        pattern = re.compile(r"^(\w+)(,\s*\w+)*$") #regex to check if input is comma seperated list
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

        #Validate the user input for api access credentials
        common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, user, password, {})
        models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        model_fields = models.execute_kw(db, uid, password, model, 'fields_get', [])
        importable_fields = []
        for field in model_fields.keys():
            if not model_fields[field]['readonly']:
                importable_fields.append(field)


        
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #CALL SCRIPT HERE
            
            
            output_df = pd.read_csv('../data/outputdata.csv')
            data = {
                "importable_fields": importable_fields, #KEYS MUST BE DOUBLE QUOTE
                "columns": list(output_df.columns)
            }
            data = json.dumps(data)
            return redirect(url_for('validate_columns', data = data))
        
        #TODO: ask leo for help with calling script

@app.route("/validate", methods=["GET", "POST"])
def validate_columns():
    if request.method == "GET":
        return current_app.send_static_file('validate.html')



        

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
        