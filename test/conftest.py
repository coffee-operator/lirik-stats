from datetime import datetime, timezone
from pathlib import Path
from typing import Callable
import uuid
from pytest import fixture
from unittest.mock import MagicMock
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from youtube.models import ChannelInfo, PlaylistItemsResponse
from youtube.youtube_api import YouTubeAPI
from youtube.youtube_client import YouTubeClient
from youtube.youtube_service import YouTubeService
from youtube.storage_service import StorageService


# YouTubeClient/API/Service


FAKE_SCOPES = ["www.youtubeapis.read.com"]
FAKE_API_SERVICE_NAME = "youtube"
FAKE_API_VERSION = "v3"


@fixture
def fake_key_file_path(tmp_path: Path, path: str = "key.json") -> Path:
    return tmp_path / path


@fixture
def mock_credentials(fake_key_file_path: Path) -> Credentials:
    mock_credentials: Credentials = MagicMock()
    mock_credentials.from_service_account_file.return_value = MagicMock(
        **{"filename": fake_key_file_path, "scopes": FAKE_SCOPES}
    )
    return mock_credentials


@fixture
def mock_discovery(mock_credentials: Credentials) -> discovery:
    mock_discovery = MagicMock()
    mock_discovery.build.return_value = MagicMock(
        **{
            "api_service_name": FAKE_API_SERVICE_NAME,
            "api_version": FAKE_API_VERSION,
            "credentials": mock_credentials.from_service_account_file.return_value,
        }
    )
    return mock_discovery


@fixture
def mock_youtube_client() -> YouTubeClient:
    return MagicMock()


@fixture
def mock_youtube_api() -> YouTubeAPI:
    return MagicMock()


@fixture
def factory_youtube_service() -> Callable[[MagicMock | YouTubeAPI], YouTubeService]:
    def _create(youtube_api: MagicMock | YouTubeAPI) -> YouTubeService:
        return YouTubeService(youtube_api=youtube_api)

    return _create


@fixture
def factory_channel_info() -> Callable[[str, str], ChannelInfo]:
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
def factory_playlist_items_response() -> Callable[[str, str], PlaylistItemsResponse]:
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


# STORAGE SERVICE


@fixture
def channel_id() -> str:
    return "UCebh6Np0l-DT9LXHrXbmopg"


@fixture
def channel_folder_name() -> str:
    return "lirik_plays"


@fixture
def fixed_clock() -> datetime:
    return datetime(2026, 1, 23, 12, 0, 0, tzinfo=timezone.utc)


@fixture
def fixed_uuid_provider() -> uuid:
    return uuid.UUID("d8d2e059-bbb9-47c8-9907-c2b0bbdeaf1d")


@fixture
def storage_service(
    channel_id,
    channel_folder_name,
    fixed_clock,
    fixed_uuid_provider,
    tmp_path,
) -> StorageService:
    return StorageService(
        channel_id=channel_id,
        channel_folder_name=channel_folder_name,
        clock=lambda: fixed_clock,
        uuid_provider=lambda: fixed_uuid_provider,
        base_data_path=tmp_path,
    )
