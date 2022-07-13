# -*- coding: utf-8 -*-

import py_cyberonnx as cyonnx
import os

# parse information and args from posted form
def parseForm(form, database):
    version = cyonnx.CyberONNX_VERSION()
    
    # parse the metadata and message
    dataID, paraID, preID = database.getVersionID()
    version.dataVersion = dataID
    version.parameterVersion = paraID
    version.preprocessVersion = preID

    metadata = cyonnx.CyberONNX_METADATA()
    metadata.version = version
    metadata.branch = cyonnx.CyberONNX_BRANCH(form.branch.data)
    metadata.modelType = cyonnx.CyberONNX_MODEL_TYPE(form.modelType.data)
    metadata.width = form.width.data
    metadata.height = form.height.data
    metadata.half = form.halfPrecision.data
    
    message = form.message.data

    # parse the args for commands
    args = dict()
    args["batch"] = form.batch.data
    args["epochs"] = form.epochs.data
    args["resultName"] = form.resultName.data
    args["width"] = form.width.data
    args["height"] = form.height.data
    args["dataPath"] = database.paths['dataPath']
    args["parameterPath"] = database.paths['configPath']
    # args["preprocessPath"] = database.paths['preprocessPath']
    args["extra"] = form.extraArgs.data
    args["half"] = form.halfPrecision.data
    return metadata, args, message

# get train command
def getCommandTrain(paths, args):
    train = os.path.join(paths.projectPath, paths.trainPath)

    # fill all the blanks with '#' in order to pass the command as a parameter
    cmd1 = paths.pythonPath + '#' + train
    cmd2 = "--batch#" + str(args["batch"]) + "#--epochs#" + str(args["epochs"])
    cmd3 = "--img#" + str(args["width"])
    cmd4 = "--data#" + args['dataPath'] + "#--cfg#" + args['parameterPath'] + "#--name#" + args["resultName"]
    command = cmd1 + '#' + cmd2 + '#' + cmd3 + '#' + cmd4
    
    if(len(args["extra"]) > 0):
        args["extra"] = args["extra"].replace(' ', '#')
        command = command + '#' + args["extra"]

    return command

# get export command
def getCommandExport(paths, args):
    export = os.path.join(paths.projectPath, paths.exportPath)
    result = os.path.join(paths.resultPath, args["resultName"])

    # fill all the blanks with '#' in order to pass the command as a parameter
    best = os.path.join(result, "best.pt")
    img_size = str(args["height"]) + '#' + str(args["width"])
    cmd1 = paths.pythonPath + '#' + export
    
    cmd2 = "--weights#" + best
    cmd3 = "--batch#1#--dynamic#--include#onnx"
    cmd4 = "--img#" + img_size
    command = cmd1 + '#' + cmd2 + '#' + cmd3 + '#' + cmd4
    if(args["half"] == 1):
        command += "#--half"

    return command

# get convert command
def getCommandConvert(paths, args):
    convert = os.path.join(paths.projectPath, paths.convertPath)
    model = os.path.join(paths.resultPath, "best.onnx")

    # fill all the blanks with '#' in order to pass the command as a parameter
    infoFileName = args["resultName"] + '_info.yml'
    infoFolder = os.path.join(paths.resultPath, 'info')
    info = os.path.join(infoFolder, infoFileName)

    cmd1 = paths.pythonPath + '#' + convert
    cmd2 = "--model#" + model + "#--info#" + info
    command = cmd1 + '#' + cmd2

    return command

# generate information file 
def generateInfoFile(paths, args, metadata, message = None):
    infoFolder = os.path.join(paths.resultPath, 'info')

    if not (os.path.exists(infoFolder)):
        os.mkdir(infoFolder)

    infoFileName = args["resultName"] + '_info.yml'
    info = os.path.join(infoFolder, infoFileName)
    cyonnx.generateYML(info, metadata, message)

# check whether the result name is valid
def validateResultName(paths, args):
    result = os.path.join(paths.resultPath, args["resultName"])
    if (os.path.exists(result) and "--exist-ok" not in args["extra"]):
        return False
    return True