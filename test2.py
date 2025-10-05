import pytest
from unittest.mock import patch, MagicMock
from zadanie2 import parse_synonyms, print_synonyms, plot_synonym_graph

@pytest.fixture
def empty_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    mock_root.findall.return_value = []  # Brak leków
    return mock_tree

@pytest.fixture
def populated_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root

    drug_mock = MagicMock()
    drug_mock.find.return_value.text = 'DB00005'
    drug_mock.findall.return_value = [
        MagicMock(text='Synonim1'),
        MagicMock(text='Synonim2')
    ]

    mock_root.findall.return_value = [drug_mock]
    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_synonyms_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    synonym_data = parse_synonyms('fake_file.xml')
    assert isinstance(synonym_data, dict)
    assert len(synonym_data) == 0

@patch('xml.etree.ElementTree.parse')
def test_parse_synonyms_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    synonym_data = parse_synonyms('fake_file.xml')
    assert 'DB00005' in synonym_data
    assert synonym_data['DB00005'] == ['Synonim1', 'Synonim2']

def test_display_synonyms():
    synonym_data = {'DB00005': ['Synonim1', 'Synonim2']}
    try:
        print_synonyms(synonym_data)
    except Exception as e:
        pytest.fail(f"display_synonyms() rzuciło wyjątek: {e}")

@patch('matplotlib.pyplot.show')
def test_plot_synonym_graph(mock_show):
    synonym_data = {'DB00005': ['Synonim1', 'Synonim2']}
    try:
        plot_synonym_graph(synonym_data, 'DB00005')
        mock_show.assert_called_once()
    except Exception as e:
        pytest.fail(f"plot_synonym_graph() rzuciło wyjątek: {e}")
