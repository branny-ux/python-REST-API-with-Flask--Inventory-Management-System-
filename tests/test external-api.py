
from unittest.mock import Mock, patch

import requests
import pytest

from external_api import (
    extract_fields,
    fetch_by_barcode,
    fetch_by_name,
)


def test_extract_fields():
    product = {
        "product_name": "Orange Juice",
        "categories": "Beverages",
        "brands": "Fresh",
        "code": "123",
    }
    result = extract_fields(product)
    assert result["product_name"] == "Orange Juice"
    assert result["category"] == "Beverages"
    assert result["barcode"] == "123"


@patch("external_api.requests.get")
def test_fetch_barcode_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Juice",
            "categories": "Drinks",
            "brands": "Fresh",
            "code": "123",
        },
    }
    mock_get.return_value = mock_response

    result = fetch_by_barcode("123")

    assert result["product_name"] == "Juice"
    mock_get.assert_called_once()


@patch("external_api.requests.get")
def test_fetch_barcode_not_found(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "status": 0,
        "product": {},
    }
    mock_get.return_value = mock_response

    assert fetch_by_barcode("000") is None


@patch("external_api.requests.get")
def test_fetch_name_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "products": [
            {
                "product_name": "Milk",
                "categories": "Dairy",
                "brands": "Fresh",
                "code": "456",
            }
        ]
    }
    mock_get.return_value = mock_response

    result = fetch_by_name("Milk")

    assert len(result) == 1
    assert result[0]["product_name"] == "Milk"


@patch("external_api.requests.get")
def test_fetch_name_empty(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"products": []}
    mock_get.return_value = mock_response

    assert fetch_by_name("Unknown product") == []


@patch("external_api.requests.get")
def test_fetch_barcode_http_error(mock_get):
    mock_get.side_effect = requests.RequestException("Network error")

    with pytest.raises(requests.RequestException):
        fetch_by_barcode("123")