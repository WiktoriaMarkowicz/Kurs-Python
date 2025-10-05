import pytest
from unittest.mock import patch, MagicMock
from zadanie7 import parse_drug_targets
import pandas as pd

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

    target_mock = MagicMock()
    target_mock.findtext.return_value = 'DB00001'

    polypeptide_mock = MagicMock()
    polypeptide_mock.get.side_effect = ['P12345', 'Swiss-Prot']
    polypeptide_mock.findtext.side_effect = [
        'Polipeptyd', 'GENE1', 'Cytoplazma', '11'
    ]

    external_identifier_mock = MagicMock()
    external_identifier_mock.findtext.side_effect = ['GenAtlas', 'GENE1']
    target_mock.findall.return_value = [external_identifier_mock]

    target_mock.find.return_value = polypeptide_mock
    mock_root.findall.return_value = [target_mock]

    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_drug_targets_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_drug_targets('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert df.empty  # Brak targetów

@patch('xml.etree.ElementTree.parse')
def test_parse_drug_targets_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_drug_targets('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert not df.empty  # Powinny być dane
    assert len(df) == 1
    assert df.iloc[0]['DrugBank ID'] == 'DB00001'
    assert df.iloc[0]['Zewnetrzna baza'] == 'Swiss-Prot'
    assert df.iloc[0]['ID zewnetrznej bazy'] == 'P12345'
    assert df.iloc[0]['Nazwa polipeptydu'] == 'Polipeptyd'
    assert df.iloc[0]['Nazwa genu kodujacego'] == 'GENE1'
    assert df.iloc[0]['GenAtlas ID'] == 'GENE1'
    assert df.iloc[0]['Umiejscowienie w komorce'] == 'Cytoplazma'
