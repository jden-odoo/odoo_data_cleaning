from flask import Flask, current_app, request, redirect, url_for
from xmlrpc import client
import re
import json
#export FLASK_APP=server
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"]) #type="json" TODO
def clean_data():
    if request.method == "GET":
        return current_app.send_static_file('index.html')
    else:
        pattern = re.compile(r"^(\w+)(,\s*\w+)*$") 
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

    
    data = {
        "importable_fields": importable_fields,
        "columns": ["col1", "col2", "col3"] #TODO: unhardcode
    }

    data = json.dumps(data)
    return redirect(url_for('validate_columns', data = data))
    #TODO: ask leo for help with calling script

@app.route("/validate", methods=["GET"])
def validate_columns():
    return current_app.send_static_file('validate.html')