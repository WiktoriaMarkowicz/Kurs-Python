import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from zadanie4 import parse_pathways

@pytest.fixture
def empty_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    mock_root.findall.return_value = []
    return mock_tree

@pytest.fixture
def populated_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root

    drug_mock = MagicMock()
    drug_mock.find.return_value.text = 'DB00005'
    pathway_mock = MagicMock()
    pathway_mock.findtext.side_effect = lambda x, namespaces=None: {
        'db:name': 'Szlak',
        'db:smpdb-id': 'SMP00001'
    }.get(x, 'Brak danych')

    drug_mock.findall.return_value = [pathway_mock]
    mock_root.findall.return_value = [drug_mock]
    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_pathways_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_pathways('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert df.empty  # DataFrame powinien być pusty

@patch('xml.etree.ElementTree.parse')
def test_parse_pathways_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_pathways('fake_file.xml')
    assert len(df) == 1
    assert df.loc[0, 'DrugBank ID'] == 'DB00005'
    assert df.loc[0, 'Nazwa szlaku'] == 'Szlak'
    assert df.loc[0, 'ID szlaku'] == 'SMP00001'

@patch('xml.etree.ElementTree.parse')
def test_unique_pathways_count(mock_parse, populated_xml_mock, capsys):
    mock_parse.return_value = populated_xml_mock

    parse_pathways('fake_file.xml')
    captured = capsys.readouterr()
    assert 'Całkowita liczba unikalnych szlaków: 1' in captured.out
