from unittest.mock import patch
from objective.objective import Client
from objective.objective import _preprocess_fields


def test_preprocess_fields_for_segment_delimiter():
    input_fields = {"segment_delimiter": {"test": "test"}}

    assert input_fields == _preprocess_fields(input_fields)


def test_create_indexes_with_highlights():
    with patch.object(Client, "request", return_value={"id": "test"}) as mock_method:
        client = Client("test_api_key")
        client.indexes.create_index(
            index_type={"name": "text", "highlights": {"text": True}},
            fields={"searchable": []},
        )
        mock_method.assert_called_once_with(
            "POST",
            "indexes",
            data={
                "configuration": {
                    "index_type": {"name": "text", "highlights": {"text": True}},
                    "fields": {"searchable": {"allow": []}},
                }
            },
        )


def test_create_indexes_without_highlights():
    with patch.object(Client, "request", return_value={"id": "test"}) as mock_method:
        client = Client("test_api_key")
        client.indexes.create_index(
            index_type={"name": "text"}, fields={"searchable": []}
        )
        mock_method.assert_called_with(
            "POST",
            "indexes",
            data={
                "configuration": {
                    "index_type": {"name": "text"},
                    "fields": {"searchable": {"allow": []}},
                }
            },
        )

        client.indexes.create_index(index_type="text", fields={"searchable": []})
        mock_method.assert_called_with(
            "POST",
            "indexes",
            data={
                "configuration": {
                    "index_type": {"name": "text"},
                    "fields": {"searchable": {"allow": []}},
                }
            },
        )


def test_delete_index():
    with patch.object(Client, "request", return_value={"id": "test"}) as mock_method:
        client = Client("test_api_key")
        client.indexes.delete_index(id="test")
        mock_method.assert_called_once_with(
            "DELETE",
            "indexes/test",
        )
