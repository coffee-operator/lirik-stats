from youtube.youtube_client import YouTubeClient
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from unittest.mock import MagicMock
from pathlib import Path
from pytest import fixture, mark


@fixture
def fake_key_file_path(tmp_path: Path, path: str = "key.json") -> Path:
    return tmp_path / path


FAKE_SCOPES = ["www.youtubeapis.read.com"]
FAKE_API_SERVICE_NAME = "youtube"
FAKE_API_VERSION = "v3"


@fixture
def m_credentials(fake_key_file_path: Path) -> Credentials:
    m_credentials: Credentials = MagicMock()
    m_credentials.from_service_account_file.return_value = MagicMock(
        **{"filename": fake_key_file_path, "scopes": FAKE_SCOPES}
    )
    return m_credentials


@fixture
def m_discovery(m_credentials: Credentials) -> discovery:
    m_discovery = MagicMock()
    m_discovery.build.return_value = MagicMock(
        **{
            "api_service_name": FAKE_API_SERVICE_NAME,
            "api_version": FAKE_API_VERSION,
            "credentials": m_credentials.from_service_account_file.return_value,
        }
    )
    return m_discovery


@fixture
def youtube_client(
    fake_key_file_path: Path, m_credentials: Credentials, m_discovery: discovery
) -> YouTubeClient:
    return YouTubeClient(
        key_file_path=fake_key_file_path,
        scopes=FAKE_SCOPES,
        api_service_name=FAKE_API_SERVICE_NAME,
        api_version=FAKE_API_VERSION,
        credentials=m_credentials,
        discovery=m_discovery,
    )


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
