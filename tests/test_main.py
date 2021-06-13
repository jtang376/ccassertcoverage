from ccassertcoverage import main
from unittest.mock import patch, mock_open
import yaml

test_name = 'testName'
path = f'some/path/with/{test_name}'
variable_name = 'variable'
config = {'default_context': {}}
config['default_context'][variable_name] = 'value'
assertion = 'filematches someFile expectedFile'
assertions = {'assertions': []}
assertions['assertions'].append(assertion)


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
    files = ['assertions.yaml', 'config.yaml', 'expectedFile']

    actual = main.get_expected_files(files)

    assert actual == ['expectedFile']


# def test_get_tests_should_return_a_list_of_tests_given_path():
