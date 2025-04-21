import pytest
from unittest.mock import patch, MagicMock
from app import gcs_utils

@patch("app.gcs_utils.storage.Client")
def test_upload_to_gcs(mock_storage_client):
    # Arrange
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_blob.public_url = "https://fake-url.com/image.jpg"
    mock_bucket.blob.return_value = mock_blob
    mock_storage_client.return_value.bucket.return_value = mock_bucket

    # Act
    file_bytes = b"fake image data"
    filename = "test.jpg"
    url = gcs_utils.upload_to_gcs(file_bytes, filename)

    # Assert
    assert url == "https://fake-url.com/image.jpg"
    mock_blob.upload_from_string.assert_called_once_with(file_bytes, content_type='image/jpeg')
    mock_blob.make_public.assert_called_once()
