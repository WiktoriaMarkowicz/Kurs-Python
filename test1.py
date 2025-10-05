import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from zadanie1 import parse_drugbank, display_drug_data

@pytest.fixture
def empty_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    mock_root.findall.return_value = []  # Pusta oczekiwana wartość, czyli brak lekow
    return mock_tree

@pytest.fixture
def populated_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    drug_mock = MagicMock()
    drug_mock.find.return_value.text = 'DB0000'
    drug_mock.findtext.side_effect = lambda x, namespaces=None: {
        'db:name': 'Paracetamol',
        'db:description': 'Lek pzeciwbólowy i przeciwzapalny',
        'db:state': 'Tabletka',
        'db:indication': 'Ból głowy, bzuca itp.',
        'db:mechanism-of-action': 'Zwalcza stany zapalne'
    }.get(x, 'Brak danych')
    drug_mock.get.return_value = 'small molecule'

    mock_root.findall.return_value = [drug_mock]
    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_drugbank_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_drugbank('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert df.empty

@patch('xml.etree.ElementTree.parse')
def test_parse_drugbank_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_drugbank('fake_file.xml')
    assert len(df) == 1  # Jeden lek
    assert df.loc[0, 'DrugBank ID'] == 'DB0000'
    assert df.loc[0, 'Nazwa'] == 'Paracetamol'
    assert df.loc[0, 'Typ'] == 'small molecule'
    assert df.loc[0, 'Opis'] == 'Lek pzeciwbólowy i przeciwzapalny'
    assert df.loc[0, 'Postać'] == 'Tabletka'
    assert df.loc[0, 'Wskazania'] == 'Ból głowy, bzuca itp.'
    assert df.loc[0, 'Mechanizm działania'] == 'Zwalcza stany zapalne'



def test_display_drug_data():
    df = pd.DataFrame([{
        'DrugBank ID': 'DB9999',
        'Nazwa': 'Paracetamol',
        'Typ': 'small molecule',
        'Opis': 'Lek pzeciwbólowy i przeciwapalny',
        'Postać': 'Tabletka',
        'Wskazania': 'Ból głowy, bzuca itp.',
        'Mechanizm działania': 'Brak informacji',
        'Pokarmy, z którymi wchodzi w interakcję': 'Brak informacji'
    }])
    try:
        display_drug_data(df)
    except Exception as e:
        pytest.fail(f"display_drug_data() rzuciło wyjątek: {e}")
