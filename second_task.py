import first_task
import pytest
from collections import OrderedDict
list_of_files_to_check = []

@pytest.fixture
def expected(pdf_path):
    expected_data = first_task.extract_info_from_pdf('test_task.pdf')
    return expected_data


@pytest.mark.parametrize("input", list_of_files_to_check)
def test_fields(input, expected):
    input_data = first_task.extract_info_from_pdf(input)
    assert input_data.keys() == expected.keys()


@pytest.mark.parametrize("input", list_of_files_to_check)
def test_fields_order(input, expected):
    input_data = first_task.extract_info_from_pdf(input)
    ordered_data = OrderedDict(sorted(input_data.items()))
    ordered_expected = OrderedDict(sorted(expected.items()))
    assert list(ordered_data.keys()) == list(ordered_expected.keys())


def test_first_barcode(input):
    data = first_task.extract_info_from_pdf(input)
    pn_value = data['PN']
    pn_barcode = data['barcode_1']['data'].decode("utf-8")
    assert pn_value == pn_barcode


def test_second_barcode(input):
    data = first_task.extract_info_from_pdf(input)
    qty_value = data['Qty']
    qty_barcode = data['barcode_0']['data'].decode("utf-8")
    assert qty_value == qty_barcode
