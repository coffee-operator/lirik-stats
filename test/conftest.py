from pathlib import Path
from pytest import fixture
from unittest.mock import MagicMock
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from youtube.models import ChannelInfo, PlaylistItemsResponse
from youtube.youtube_api import YouTubeAPI
from youtube.youtube_service import YouTubeService


FAKE_SCOPES = ["www.youtubeapis.read.com"]
FAKE_API_SERVICE_NAME = "youtube"
FAKE_API_VERSION = "v3"


@fixture
def fake_key_file_path(tmp_path: Path, path: str = "key.json") -> Path:
    return tmp_path / path


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
def m_youtube_client():
    return MagicMock()


@fixture
def m_youtube_api():
    return MagicMock()


@fixture
def f_youtube_service():
    def _create(youtube_api: MagicMock | YouTubeAPI) -> YouTubeService:
        return YouTubeService(youtube_api=youtube_api)

    return _create


@fixture
def f_channel_info():
    def _create(channel_id: str = "12345", playlist_id: str = "abc") -> ChannelInfo:
        return ChannelInfo(
            **{
                "kind": "k",
                "etag": "e",
                "pageInfo": {"channelId": channel_id},
                "items": [
                    {"contentDetails": {"relatedPlaylists": {"uploads": playlist_id}}}
                ],
            }
        )

    return _create


@fixture
def f_playlist_items_response():
    def _create(
        next_page_token: str = "42", playlist_id: str = "alpha"
    ) -> PlaylistItemsResponse:
        return PlaylistItemsResponse(
            **{
                "kind": "k",
                "etag": "e",
                "nextPageToken": next_page_token,
                "items": [
                    {
                        "kind": "a",
                        "etag": "b",
                        "id": "c",
                        "snippet": {},
                        "contentDetails": {
                            "relatedPlaylists": {"uploads": playlist_id}
                        },
                        "status": {},
                    }
                ],
                "pageInfo": {},
            }
        )

    return _create
