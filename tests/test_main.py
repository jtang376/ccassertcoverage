from ccassertcoverage import main
from unittest.mock import patch, mock_open
import yaml

test_name = 'testName'
path = f'some/path/with/{test_name}'
target_file = 'someFile'
expected_file = 'expectedFile'
files = ['assertions.yaml', 'config.yaml', expected_file]
variable_name = 'variable'
config = {'default_context': {}}
config['default_context'][variable_name] = 'value'
assertion = f'filematches {target_file} {expected_file}'
assertions = {'assertions': []}
assertions['assertions'].append(assertion)
tests = [
    {
        'testPath': path,
        'testName': test_name,
        'variables': [variable_name],
        'rules': [assertion.split()],
        'expectedFiles': [expected_file]
    }
]
template = {
    'files': {
        'templatizedfile': [
            'variable'
        ],
        'subdirectory/anothertemplatizedfile': [
            'variable', 'variabletoo'
        ]
    },
    'variables': {
        'variable': [
            {
                'file': 'templatizedfile',
                'path': '../template/{{ cookiecutter.project_name }}'
            },
            {
                'file': 'anothertemplatizedfile',
                'path': '../template/{{ cookiecutter.project_name }}/subdirectory'
            }
        ],
        'variabletoo': [
            {
                'file': 'anothertemplatizedfile',
                'path': '../template/{{ cookiecutter.project_name }}/subdirectory'
            }
        ]
    }
}


def test_get_test_name_from_path_should_return_the_last_split_of_path():
    actual = main.get_test_name_from_path(path)

    assert actual == test_name


@patch('yaml.load')
@patch('builtins.open', new_callable=mock_open, read_data=yaml.dump(config))
def test_get_variables_should_return_a_list_of_variables_from_config_given_a_test_directory(mock_file, mock_load):
    mock_load.return_value = config

    actual = main.get_variables(path)

    assert actual == [variable_name]


@patch('yaml.load')
@patch('builtins.open', new_callable=mock_open, read_data=yaml.dump(assertions))
def test_get_rules_should_return_a_list_of_rules_assertions_given_a_test_directory(mock_file, mock_load):
    mock_load.return_value = assertions

    actual = main.get_rules(path)

    assert actual == [assertion.split()]


def test_get_expected_files_should_not_contain_assertions_or_config():
    actual = main.get_expected_files(files)

    assert actual == [expected_file]


@patch('yaml.load')
@patch('os.walk')
@patch('builtins.open', new_callable=mock_open, read_data=yaml.dump(config))
def test_get_tests_should_return_a_list_of_tests_given_a_path(mock_file, mock_tree, mock_load):
    mock_tree.return_value = [(path, [], files)]
    mock_load.side_effect = [config, assertions]

    actual = main.get_tests('../template')

    assert actual == tests


def test_get_target_files_returns_a_list_of_files_given_a_list_of_tests():
    actual = main.get_target_files(tests)

    assert actual == [target_file]


def test_get_template_should_return_a_map_of_templatized_files_to_list_of_variable_names():
    actual = main.get_template('../template')

    assert actual == template
