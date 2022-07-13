# -*- coding: utf-8 -*-

import subprocess
from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)  # Generic key for dev purposes only

databaseFile = 'database.yaml'
db = tabledef.DataBase(databaseFile)

# -------- Train ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form = forms.InformationForm(request.form)
        if form.validate():

            # check path settings first
            paths = tabledef.pathSettings(db.paths)
            path_status = paths.validatePaths()
            if(path_status != 'OK'):
                return json.dumps({'status': 'Wrong path setting: ' + path_status})

            # parse information and args
            metadata, args, message = helpers.parseForm(form, db)
            if not(helpers.validateResultName(paths, args)):
                return json.dumps({'status': 
                f'Result with name \"{args["resultName"]}\" already exists. \nAdd extra argument \"--exist-ok\" or rename your result.'})

            # generate information file and get commands
            helpers.generateInfoFile(paths, args, metadata, message)
            cmdTrain = helpers.getCommandTrain(paths, args)
            cmdExport = helpers.getCommandExport(paths, args)
            cmdConvert = helpers.getCommandConvert(paths, args)

            # run commands
            subprocess.Popen("cmd /c start {} -i .\\call.py --train {} --export {} --convert {} --cwd {}"\
                            .format(paths.pythonPath, cmdTrain, cmdExport, cmdConvert, paths.projectPath))
            return json.dumps({'status': 'Run successful'})
        return json.dumps({'status': 'Wrong model settings'})
    return render_template('home.html')

# -------- Runing ------------------------------------------------------------- #
@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

# -------- Setting ------------------------------------------------------------ #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        form = forms.PathForm(request.form)
        if form.validate():

            # save new settings
            db.updatePath(dict(request.form))
            return json.dumps({'status': 'Save successful'})
        return json.dumps({'status': 'Wrong settings: some required fields are missing!'})
    return render_template('settings.html', defaultPath=db.paths)

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.run(debug=False)
