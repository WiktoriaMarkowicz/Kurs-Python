import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from zadanie5 import parse_pathways_and_drugs, plot_graph

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

    pathway_mock = MagicMock()
    pathway_mock.findtext.side_effect = lambda x, namespaces=None: {
        'db:name': 'Szlak',
        'db:smpdb-id': 'SMP00001'
    }.get(x, 'Brak danych')

    drug_mock = MagicMock()
    drug_mock.findtext.side_effect = lambda x, namespaces=None: {
        'db:name': 'Lek',
        'db:drugbank-id': 'DB00005'
    }.get(x, 'Brak danych')

    pathway_mock.findall.return_value = [drug_mock]
    mock_root.findall.return_value = [pathway_mock]
    return mock_tree


@patch('xml.etree.ElementTree.parse')
def test_parse_pathways_and_drugs_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    df = parse_pathways_and_drugs('fake_file.xml')
    assert isinstance(df, pd.DataFrame)
    assert df.empty

@patch('xml.etree.ElementTree.parse')
def test_parse_pathways_and_drugs_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    df = parse_pathways_and_drugs('fake_file.xml')
    assert len(df) == 1
    assert df.loc[0, 'ID szlaku'] == 'SMP00001'
    assert df.loc[0, 'Nazwa szlaku'] == 'Szlak'
    assert df.loc[0, 'DrugBank ID'] == 'DB00005'
    assert df.loc[0, 'Nazwa leku'] == 'Lek'

@patch('matplotlib.pyplot.show')
def test_plot_graph(mock_show):
    interaction_df = pd.DataFrame([{
        'ID szlaku': 'SMP00001',
        'Nazwa szlaku': 'Szlak',
        'DrugBank ID': 'DB00005',
        'Nazwa leku': 'Lek'
    }])
    try:
        plot_graph(interaction_df)
        mock_show.assert_called_once()  # Sprawdzamy, czy wykres został pokazany
    except Exception as e:
        pytest.fail(f"plot_graph() rzuciło wyjątek: {e}")
