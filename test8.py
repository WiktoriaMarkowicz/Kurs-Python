import pytest
from unittest.mock import patch, MagicMock
from zadanie8 import parse_target_locations, plot_pie_charts

@pytest.fixture
def empty_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root
    mock_root.findall.return_value = []  # Brak targetów
    return mock_tree

@pytest.fixture
def populated_xml_mock():
    mock_tree = MagicMock()
    mock_root = MagicMock()
    mock_tree.getroot.return_value = mock_root

    target_mock = MagicMock()
    polypeptide_mock = MagicMock()
    polypeptide_mock.findtext.return_value = 'Cytoplazma'
    target_mock.find.return_value = polypeptide_mock

    mock_root.findall.return_value = [target_mock, target_mock, target_mock]  # Trzy targety
    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_target_locations_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    location_counts = parse_target_locations('fake_file.xml')
    assert isinstance(location_counts, dict)
    assert len(location_counts) == 0  # Brak lokalizacji

@patch('xml.etree.ElementTree.parse')
def test_parse_target_locations_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    location_counts = parse_target_locations('fake_file.xml')
    assert isinstance(location_counts, dict)
    assert location_counts['Cytoplazma'] == 3

@patch('matplotlib.pyplot.show')
def test_plot_pie_charts(mock_show):
    location_counts = {'Cytoplazma': 3, 'Błona komórkowa': 1, 'Jądro komórkowe': 1}
    try:
        plot_pie_charts(location_counts)
        mock_show.assert_called_once()
    except Exception as e:
        pytest.fail(f"plot_pie_charts() rzuciło wyjątek: {e}")
