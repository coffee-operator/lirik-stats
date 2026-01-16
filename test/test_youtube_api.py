from unittest.mock import MagicMock
from youtube.models import ChannelInfo, PlaylistItem
from youtube.youtube_api import YouTubeAPI


def test_youtube_api_init(api_service_name: str = "fake_value"):
    # Arrange
    m_youtube_client = MagicMock()
    m_youtube_client.resource.api_service_name.return_value = api_service_name
    youtube_api = YouTubeAPI(youtube_client=m_youtube_client)

    # Act
    # YouTubeAPI__init__()

    # Assert
    youtube_api.resource == api_service_name


def test_youtube_api_get_channel_info(channel_id: str = "123123"):
    # Arrange
    m_youtube_client = MagicMock()
    m_channel_info = {
        "kind": "k",
        "etag": "e",
        "pageInfo": {},
        "items": [{"id": channel_id}],
    }
    m_youtube_client.resource.channels.return_value.list.return_value.execute.return_value = m_channel_info
    youtube_api = YouTubeAPI(youtube_client=m_youtube_client)

    # Act
    channel_info = youtube_api.get_channel_info(channel_id=channel_id)

    # Assert
    assert isinstance(channel_info, ChannelInfo)
    assert channel_info.items[0]["id"] == channel_id


def test_extract_channel_uploads_playlist_id(playlist_id: str = "123123"):
    # Arrange
    youtube_api = YouTubeAPI(youtube_client=MagicMock())
    channel_info = ChannelInfo(
        **{
            "kind": "k",
            "etag": "e",
            "pageInfo": {},
            "items": [
                {"contentDetails": {"relatedPlaylists": {"uploads": playlist_id}}}
            ],
        }
    )

    # Act
    m_playlist_id = youtube_api.extract_channel_uploads_playlist_id(channel_info)

    # Assert
    assert m_playlist_id == playlist_id


def test_youtube_api_get_channel_playlist_items(playlist_id: str = "abcabc"):
    # Arrange
    m_youtube_client = MagicMock()
    m_youtube_client.resource.playlistItems.return_value.list.return_value.execute.return_value = {
        "kind": "k",
        "etag": "e",
        "nextPageToken": "",
        "items": [
            PlaylistItem(
                kind="a",
                etag="b",
                id=playlist_id,
                snippet={},
                contentDetails={},
                status={},
            )
        ],
        "pageInfo": {},
    }
    youtube_api = YouTubeAPI(youtube_client=m_youtube_client)

    # Act
    playlist_items_response = youtube_api.get_channel_playlist_items(
        playlist_id=playlist_id
    )

    # Assert
    assert playlist_items_response.items[0].id == playlist_id
