from youtube.youtube_client import YouTubeClient
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from pathlib import Path
from conftest import FAKE_SCOPES, FAKE_API_SERVICE_NAME, FAKE_API_VERSION


def test_youtube_client_init(
    fake_key_file_path: Path, m_credentials: Credentials, m_discovery: discovery
):
    # Arrange
    youtube_client = YouTubeClient(
        key_file_path=fake_key_file_path,
        scopes=FAKE_SCOPES,
        api_service_name=FAKE_API_SERVICE_NAME,
        api_version=FAKE_API_VERSION,
        credentials=m_credentials,
        discovery=m_discovery,
    )

    # Act
    # YouTubeClient.__init__()

    # Assert
    m_credentials.from_service_account_file.assert_called_once()
    m_discovery.build.assert_called_once()

    assert youtube_client.credentials.scopes == FAKE_SCOPES
    assert youtube_client.resource.api_service_name == FAKE_API_SERVICE_NAME
    assert youtube_client.credentials == youtube_client.resource.credentials
