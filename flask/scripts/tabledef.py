# -*- coding: utf-8 -*-
import os
import yaml

# paths 
class pathSettings:
    def __init__(self, paths):
        self.pythonPath = paths['pythonPath']
        self.projectPath = paths['projectPath'] # path of the yolo project
        self.trainPath = os.path.join(paths['projectPath'], paths['trainPath']) # path of the train file
        self.exportPath = os.path.join(paths['projectPath'], paths['exportPath']) # path of the export file
        self.convertPath = os.path.join(paths['projectPath'], paths['convertPath']) # path of the convert file
        self.dataPath = os.path.join(paths['projectPath'], paths['dataPath']) # path of the data folder file
        self.configPath = os.path.join(paths['projectPath'], paths['configPath']) # path of the config folder file
        self.resultPath = os.path.join(paths['projectPath'], paths['resultPath']) # path of the result folder file
        # self.preprocessPath = paths['preprocessPath']

    # check existence of paths
    def validatePaths(self):
        if not (os.path.exists(self.pythonPath)):
            return 'python path does not exist!'
        if not (os.path.exists(self.projectPath)):
            return 'project path does not exist!'
        if not (os.path.exists(self.trainPath)):
            return 'train code path does not exist!'
        if not (os.path.exists(self.exportPath)):
            return 'export code path does not exist!'
        if not (os.path.exists(self.convertPath)):
            return 'convert code path does not exist!'
        if not (os.path.exists(self.dataPath)):
            return 'data path does not exist!'
        if not (os.path.exists(self.configPath)):
            return 'config path does not exist!'
        if not (os.path.exists(self.resultPath)):
            return 'result path does not exist!'
        if (os.path.samefile(self.dataPath, self.projectPath)):
            return 'please set data path!'
        if (os.path.samefile(self.configPath, self.projectPath)):
            return 'please set config path!'
        return 'OK'

# store the path settings and the file version information
class DataBase:
    def __init__(self, databaseFile):
        self.file = databaseFile
        if not (os.path.exists(self.file)):
            f = open(self.file, 'w')
            paths = {
                'pythonPath': 'C:/Program Files/anaconda3/python.exe',
                'projectPath': '../YoloV5/',
                'trainPath': 'train.py',
                'exportPath': 'models/export.py',
                'convertPath': 'utils/convert.py',
                'resultPath': 'runs/train/',
                'dataPath': 'data/',
                'configPath': 'models/',
                'preprocessPath': ''
            }
            yaml.dump(paths,f)
            f.close()

        f = open(self.file, 'r')
        self.paths = yaml.load(f.read())
        self.existVersions = {
            'dataVersion': [],
            'parameterVersion': [],
            'preprocessVersion': []
        }
        f.close()

    # update paths and database file
    def updatePath(self, paths):
        f = open(self.file, 'w')
        self.paths = paths
        yaml.dump(self.paths, f)
        f.close()
    
    # transfer the file paths to file IDs with database
    def getVersionID(self):
        versions = {
            'dataVersion': self.paths['dataPath'],
            'parameterVersion': self.paths['configPath'],
            'preprocessVersion': self.paths['preprocessPath']
        }
        versionFile = os.path.join(self.paths['projectPath'], self.file)
        if (os.path.exists(versionFile)):
            f = open(versionFile, 'r')
            self.existVersions = yaml.load(f)
            f.close()
            
        dataID = -1
        paraID = -1
        preID = -1

        # get IDs
        for i in range(len(self.existVersions['dataVersion'])):
            if(self.existVersions['dataVersion'][i] == versions['dataVersion']):
                dataID = i
                break
        if(dataID == -1):
            self.existVersions['dataVersion'].append(versions['dataVersion'])
            dataID = len(self.existVersions['dataVersion']) - 1

        for j in range(len(self.existVersions['parameterVersion'])):
            if(self.existVersions['parameterVersion'][j] == versions['parameterVersion']):
                paraID = j
                break
        if(paraID == -1):
            self.existVersions['parameterVersion'].append(versions['parameterVersion'])
            paraID = len(self.existVersions['parameterVersion']) - 1

        if(len(versions['preprocessVersion']) > 0):
            for k in range(len(self.existVersions['preprocessVersion'])):
                if(self.existVersions['preprocessVersion'][k] == versions['preprocessVersion']):
                    preID = k
                    break
            if(preID == -1):
                self.existVersions['preprocessVersion'].append(versions['preprocessVersion'])
                preID = len(self.existVersions['preprocessVersion']) - 1 

        # save to database file
        f = open(versionFile, 'w')
        yaml.dump(self.existVersions, f)
        f.close()
        return dataID, paraID, preID