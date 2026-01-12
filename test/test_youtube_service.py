from unittest.mock import MagicMock
from youtube.models import ChannelInfo
from youtube.youtube_api import YouTubeAPI
from youtube.youtube_service import YouTubeService


def test_youtube_service_init():
    # Arrange
    m_youtube_api = MagicMock()
    youtube_service = YouTubeService(youtube_api=m_youtube_api)

    # Act
    # YouTubeService.__init_()

    # Assert
    assert youtube_service.youtube_api == m_youtube_api


def test_get_channel_info(channel_id: str = "abcabc"):
    # Arrange
    m_youtube_api = MagicMock()
    m_channel_info = ChannelInfo(
        **{
            "kind": "k",
            "etag": "e",
            "pageInfo": {},
            "items": [{"id": channel_id}],
        }
    )
    m_youtube_api.get_channel_info.return_value = m_channel_info
    youtube_service = YouTubeService(youtube_api=m_youtube_api)

    # Act
    channel_info = youtube_service.get_channel_info(channel_id=channel_id)

    # Assert
    assert isinstance(channel_info, ChannelInfo)
    assert channel_info.items[0]["id"] == channel_id


# e