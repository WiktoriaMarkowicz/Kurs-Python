import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from zadanie3 import parse_products, display_products_for_id

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
    product_mock = MagicMock()
    product_mock.findtext.side_effect = lambda x, namespaces=None: {
        'db:name': 'Paracetamol',
        'db:labeller': 'Bayer',
        'db:ndc-product-code': '12345-6789',
        'db:dosage-form': 'Tabletka',
        'db:route': 'Doustna',
        'db:strength': '500mg',
        'db:country': 'USA',
        'db:source': 'Agencja'
    }.get(x, 'Brak danych')

    drug_mock.findall.return_value = [product_mock]
    mock_root.findall.return_value = [drug_mock]
    return mock_tree

@patch('xml.etree.ElementTree.parse')
@patch('pandas.DataFrame.to_csv')
def test_parse_products_empty(mock_to_csv, mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_products('fake_file.xml', 'output.csv')
    assert isinstance(df, pd.DataFrame)
    assert df.empty  # Sprawdzamy, czy DataFrame jest pusty
    mock_to_csv.assert_called_once()  # Sprawdzamy czy dane zapisano do CSV

@patch('xml.etree.ElementTree.parse')
@patch('pandas.DataFrame.to_csv')
def test_parse_products_with_data(mock_to_csv, mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_products('fake_file.xml', 'output.csv')
    assert len(df) == 1
    assert df.loc[0, 'DrugBank ID'] == 'DB00005'
    assert df.loc[0, 'Nazwa produktu'] == 'Paracetamol'
    assert df.loc[0, 'Producent'] == 'Bayer'
    assert df.loc[0, 'Kod NDC'] == '12345-6789'
    assert df.loc[0, 'Postać'] == 'Tabletka'
    assert df.loc[0, 'Sposób aplikacji'] == 'Doustna'
    assert df.loc[0, 'Dawka'] == '500mg'
    assert df.loc[0, 'Kraj'] == 'USA'
    assert df.loc[0, 'Agencja'] == 'Agencja'

    mock_to_csv.assert_called_once()

def test_display_products_for_id(capsys):
    df = pd.DataFrame([{
        'DrugBank ID': 'DB00005',
        'Nazwa produktu': 'Paracetamol',
        'Producent': 'Bayer'
    }])
    display_products_for_id(df, 'DB00005')
    captured = capsys.readouterr() # Przechwytywanie wyniku print()
    assert 'Tabela produktów dla DB00005' in captured.out
    assert 'Paracetamol' in captured.out
    assert 'Bayer' in captured.out
