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
from youtube.storage_service import (
    api_sources,
    data_stages,
    data_sources,
    StorageService,
)


# YouTubeClient/API/Service


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
def m_youtube_client() -> YouTubeClient:
    return MagicMock()


@fixture
def m_youtube_api() -> YouTubeAPI:
    return MagicMock()


@fixture
def f_youtube_service() -> Callable[[MagicMock | YouTubeAPI], YouTubeService]:
    def _create(youtube_api: MagicMock | YouTubeAPI) -> YouTubeService:
        return YouTubeService(youtube_api=youtube_api)

    return _create


@fixture
def f_channel_info() -> Callable[[str, str], ChannelInfo]:
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
def f_playlist_items_response() -> Callable[[str, str], PlaylistItemsResponse]:
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
def m_channel_id() -> str:
    return "123abc"


@fixture
def m_channel_folder_name() -> str:
    return "alpha"


@fixture
def m_clock() -> datetime:
    return datetime(2026, 1, 23, 12, 0, 0, tzinfo=timezone.utc)


@fixture
def m_uuid_provider() -> uuid:
    return uuid.UUID("d8d2e059-bbb9-47c8-9907-c2b0bbdeaf1d")


@fixture
def m_base_data_path(tmp_path) -> Path:
    return tmp_path


@fixture
def m_api_source() -> api_sources:
    return "youtube_api"


@fixture
def m_data_stage() -> data_stages:
    return "raw"


@fixture
def m_data_source() -> data_sources:
    return "workflow"


@fixture
def m_json_gz_file_name(m_clock, format="%Y-%m-%d") -> str:
    return f"{m_clock.strftime(format)}.json.gz"


@fixture
def m_storage_service(
    m_channel_id,
    m_channel_folder_name,
    m_clock,
    m_uuid_provider,
    m_base_data_path,
) -> StorageService:
    return StorageService(
        channel_id=m_channel_id,
        channel_folder_name=m_channel_folder_name,
        clock=lambda: m_clock,
        uuid_provider=lambda: m_uuid_provider,
        base_data_path=m_base_data_path,
    )
