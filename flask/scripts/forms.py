# -*- coding: utf-8 -*-

from wtforms import Form, StringField, validators, IntegerField

# form posted in home page
class InformationForm(Form):
    branch = IntegerField('branch', validators=[validators.Optional()])
    modelType = IntegerField('modelType', validators=[validators.Optional()])
    width = IntegerField('width', validators=[validators.DataRequired()])
    height = IntegerField('height', validators=[validators.DataRequired()])
    batch = IntegerField('batch', validators=[validators.DataRequired()])
    epochs = IntegerField('epochs', validators=[validators.DataRequired()])
    halfPrecision = IntegerField('halfPrecision', validators=[validators.Optional()])
    message = StringField('message', validators=[validators.Optional()])
    resultName = StringField('resultName', validators=[validators.DataRequired()])
    extraArgs = StringField('extraArgs', validators=[validators.Optional()])

# form posted in settings page
class PathForm(Form):
    pythonPath = StringField('pythonPath', validators=[validators.DataRequired()])
    projectPath = StringField('projectPath', validators=[validators.DataRequired()])
    trainPath = StringField('trainPath', validators=[validators.DataRequired()])
    exportPath = StringField('exportPath', validators=[validators.DataRequired()])
    convertPath = StringField('convertPath', validators=[validators.DataRequired()])
    dataPath = StringField('dataPath', validators=[validators.DataRequired()])
    configPath = StringField('configPath', validators=[validators.DataRequired()])
    resultPath = StringField('resultPath', validators=[validators.DataRequired()])
    preprocessPath = StringField('preprocessPath', validators=[validators.Optional()])