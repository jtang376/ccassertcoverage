import os

import yaml


# from ccassertcoverage import test


def getTestNameFromPath(path: str):
    return path.split('/')[-1]


def getVariables(path):
    configFile = path + '/config.yaml'
    with open(configFile, 'r') as yamlConfigFile:
        configData = yaml.load(yamlConfigFile, Loader=yaml.FullLoader)
    return list(configData['default_context'].keys())


def getRules(path):
    assertionFile = path + '/assertions.yaml'
    rules = []
    with open(assertionFile, 'r') as yamlAssertionFile:
        assertionData = yaml.load(yamlAssertionFile, Loader=yaml.FullLoader)
        for ruleString in assertionData["assertions"]:
            rules.append(ruleString.split())
    return rules


def getExpectedFiles(files):
    expectedFiles = files.copy()
    expectedFiles.remove('assertions.yaml')
    expectedFiles.remove('config.yaml')
    return expectedFiles

tests = []
current_tree = os.walk(os.getcwd() + '/tests')

for row in current_tree:
    if 'assertions.yaml' in row[2] and 'config.yaml' in row[2]:
        test = {'testPath': row[0],
                'testName': getTestNameFromPath(row[0]),
                'variables': getVariables(row[0]),
                'rules': getRules(row[0]),
                'expectedFiles': getExpectedFiles(row[2])}
        print(test)
