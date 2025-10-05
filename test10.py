import pytest
from unittest.mock import patch, MagicMock
from zadanie10 import parse_drug_interactions_for_id
import pandas as pd

@pytest.fixture
def empty_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    mock_root.find.return_value = None  # Brak leku z danym ID
    return mock_tree

@pytest.fixture
def populated_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root

    drug_mock = MagicMock()

    interaction_mock = MagicMock()
    interaction_mock.findtext.side_effect = ["DB99999", "Drug", "Opis interakcji"]
    drug_mock.findall.return_value = [interaction_mock]

    mock_root.find.return_value = drug_mock
    return mock_tree


@patch('xml.etree.ElementTree.parse')
def test_parse_drug_interactions_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_drug_interactions_for_id('fake_file.xml', 'DB00001')
    assert isinstance(df, pd.DataFrame)
    assert df.empty

@patch('xml.etree.ElementTree.parse')
def test_parse_drug_interactions_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_drug_interactions_for_id('fake_file.xml', 'DB00001')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.iloc[0]['DrugBank ID'] == 'DB99999'
    assert df.iloc[0]['Nazwa'] == 'Drug'
    assert df.iloc[0]['Opis'] == 'Opis interakcji'
