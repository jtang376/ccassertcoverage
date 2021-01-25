import os
import re

import yaml


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


def getTests(path):
    tests = []
    current_tree = os.walk(path + '/tests')

    for row in current_tree:
        if 'assertions.yaml' in row[2] and 'config.yaml' in row[2]:
            test = {'testPath': row[0],
                    'testName': getTestNameFromPath(row[0]),
                    'variables': getVariables(row[0]),
                    'rules': getRules(row[0]),
                    'expectedFiles': getExpectedFiles(row[2])}
            tests.append(test)
    return tests


def getTemplate(path):
    templatedata = {'files': {}, 'variables': {}}
    templatepath = path + '/{{ cookiecutter.project_name }}'
    current_tree = os.walk(templatepath)

    for row in current_tree:
        for filename in row[2]:
            fullpath = row[0] + '/' + filename
            file = open(fullpath, 'r')
            lines = file.readlines()
            for line in lines:
                if 'cookiecutter.' in line:
                    match = re.search('cookiecutter\.[A-Za-z_]*\ ', line)
                    variable = match.group(0).split('.')[-1].strip()
                    if variable not in templatedata['variables'].keys():
                        templatedata['variables'][variable] = []
                    templatedata['variables'][variable].append({'file': filename, 'path': row[0]})
                    if fullpath not in templatedata['files'].keys():
                        templatedata['files'][fullpath] = []
                    templatedata['files'][fullpath].append(variable)
    return templatedata


curr_dir = os.getcwd()
tests = getTests(curr_dir)
template = getTemplate(curr_dir)
print(template)


