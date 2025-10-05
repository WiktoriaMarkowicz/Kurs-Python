import pytest
from unittest.mock import patch, MagicMock
from zadanie6 import parse_drug_pathway_counts
import pandas as pd

@pytest.fixture
def empty_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    mock_root.findall.return_value = []  # Brak szlaków
    return mock_tree

@pytest.fixture
def populated_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root

    pathway_mock = MagicMock()
    pathway_mock.findtext.return_value = 'Pathway 1'

    drug_mock_1 = MagicMock()
    drug_mock_1.findtext.return_value = 'DB00001'
    drug_mock_2 = MagicMock()
    drug_mock_2.findtext.return_value = 'DB00002'
    pathway_mock.findall.return_value = [drug_mock_1, drug_mock_2]

    mock_root.findall.return_value = [pathway_mock]
    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_drug_pathway_counts_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_drug_pathway_counts('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert df.empty

@patch('xml.etree.ElementTree.parse')
def test_parse_drug_pathway_counts_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_drug_pathway_counts('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty  # Powinny być dane
    assert len(df) == 2
    assert df.iloc[0]['DrugBank ID'] == 'DB00001'
    assert df.iloc[0]['Liczba szlaków'] == 1
