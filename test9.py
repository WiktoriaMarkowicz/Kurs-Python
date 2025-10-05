import pytest
from unittest.mock import patch, MagicMock
from zadanie9 import parse_group, plot_pie_charts

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
    group_mock_approved = MagicMock(text='approved')
    group_mock_withdrawn = MagicMock(text='withdrawn')
    group_mock_experimental = MagicMock(text='experimental')
    drug_mock.findall.return_value = [group_mock_approved, group_mock_experimental]

    drug_withdrawn_mock = MagicMock()
    drug_withdrawn_mock.findall.return_value = [group_mock_approved, group_mock_withdrawn]

    mock_root.findall.return_value = [drug_mock, drug_withdrawn_mock]
    return mock_tree

@patch('xml.etree.ElementTree.parse')
def test_parse_group_empty(mock_parse, empty_xml_mock):
    mock_parse.return_value = empty_xml_mock

    group_counts = parse_group('fake_file.xml')
    assert isinstance(group_counts, dict)
    assert len(group_counts) == 0  # Brak grup

@patch('xml.etree.ElementTree.parse')
def test_parse_group_with_data(mock_parse, populated_xml_mock):
    mock_parse.return_value = populated_xml_mock

    group_counts = parse_group('fake_file.xml')
    assert isinstance(group_counts, dict)
    assert group_counts['approved'] == 2  # Jeden lek approved, drugi approved i withdrawn
    assert group_counts['experimental'] == 1
    assert group_counts['withdrawn'] == 1  # Jeden withdrawn

@patch('matplotlib.pyplot.show')
def test_plot_pie_charts(mock_show):
    group_counts = {'approved': 2, 'experimental': 1, 'withdrawn': 1}
    try:
        plot_pie_charts(group_counts)
        mock_show.assert_called_once()
    except Exception as e:
        pytest.fail(f"plot_pie_charts() rzuciło wyjątek: {e}")
