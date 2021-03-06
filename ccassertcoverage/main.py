import json
import os
import re

import yaml


def get_test_name_from_path(path: str):
    return path.split('/')[-1]


def get_variables(path):
    configfile = path + '/config.yaml'
    with open(configfile, 'r') as yamlConfigFile:
        configdata = yaml.load(yamlConfigFile, Loader=yaml.FullLoader)
    return list(configdata['default_context'].keys())


def get_rules(path):
    assertionfile = path + '/assertions.yaml'
    rules = []
    with open(assertionfile, 'r') as yamlAssertionFile:
        assertiondata = yaml.load(yamlAssertionFile, Loader=yaml.FullLoader)
        for ruleString in assertiondata["assertions"]:
            rules.append(ruleString.split())
    return rules


def get_expected_files(files):
    expectedFiles = files.copy()
    expectedFiles.remove('assertions.yaml')
    expectedFiles.remove('config.yaml')
    return expectedFiles


def get_tests(path):
    tests = []
    current_tree = os.walk(path + '/tests')
    for row in current_tree:
        if 'assertions.yaml' in row[2] and 'config.yaml' in row[2]:
            test = {'testPath': row[0],
                    'testName': get_test_name_from_path(row[0]),
                    'variables': get_variables(row[0]),
                    'rules': get_rules(row[0]),
                    'expectedFiles': get_expected_files(row[2])}
            tests.append(test)
    return tests


def get_project_name(test):
    if 'project_name' in test['variables']:
        configfile = test['testPath'] + '/config.yaml'
        with open(configfile, 'r') as yamlConfigFile:
            configdata = yaml.load(yamlConfigFile, Loader=yaml.FullLoader)
            return configdata['default_context']['project_name']
    else:
        path = test['testPath'].rsplit('/', 2)[0]
        configfile = path + '/defaultConfig.yaml'
        with open(configfile, 'r') as yamlConfigFile:
            configdata = yaml.load(yamlConfigFile, Loader=yaml.FullLoader)
            if 'project_name' in configdata['default_context'].keys():
                return configdata['default_context']['project_name']
            else:
                configfile = path + '/cookiecutter.json'
                with open(configfile, 'r') as cookiecutterJson:
                    configdata = json.load(cookiecutterJson)
                    return configdata['project_name']


def get_target_files(tests):
    files = []
    for test in tests:
        for rule in test['rules']:
            print(rule)
            if 'filematches' in rule:
                files.extend(filter(lambda element: element != 'filematches' and element not in test['expectedFiles'], rule))
    return files


def get_template(path):
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
                    key = (row[0].replace(templatepath, '') + '/' + filename).replace('/', '', 1)
                    if key not in templatedata['files'].keys():
                        templatedata['files'][key] = []
                    templatedata['files'][key].append(variable)
    return templatedata


# curr_dir = os.getcwd()
curr_dir = '../template'

# get list of files referenced in tests
tests = get_tests(curr_dir)
print(f'Tests -> {tests}')
target_files = get_target_files(tests)
print(f'Target Files -> {target_files}')

# get templatized files
template = get_template(curr_dir)
print(f'Template -> {template}')
templatized_files = template['files'].keys()
print(f'Templatized Files -> {templatized_files}')

# percentage of files with variables that are verified by a test
# filename -> list of tests
# list files with variables not verified by a test

# percentage of variables exercised by test
# list of variables not exercised by test
