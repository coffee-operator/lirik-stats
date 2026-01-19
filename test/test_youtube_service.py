from unittest.mock import MagicMock
from youtube.models import ChannelInfo, PlaylistItems
from youtube.youtube_api import YouTubeAPI


def test_youtube_service_init(m_youtube_api, f_youtube_service):
    # Arrange
    youtube_service = f_youtube_service(youtube_api=m_youtube_api)

    # Act
    # YouTubeService.__init_()

    # Assert
    assert youtube_service.youtube_api == m_youtube_api


def test_get_channel_info(
    m_youtube_api, f_youtube_service, f_channel_info, channel_id: str = "abcabc"
):
    # Arrange
    youtube_service = f_youtube_service(youtube_api=m_youtube_api)
    m_youtube_api.get_channel_info.return_value = f_channel_info(channel_id=channel_id)

    # Act
    channel_info = youtube_service.get_channel_info(channel_id=channel_id)

    # Assert
    assert isinstance(channel_info, ChannelInfo)
    assert channel_info.pageInfo["channelId"] == channel_id


def test_extract_channel_uploads_playlist_id(
    f_youtube_service, f_channel_info, playlist_id: str = "123123"
):
    # Arrange
    youtube_api = YouTubeAPI(youtube_client=MagicMock())
    youtube_service = f_youtube_service(youtube_api=youtube_api)
    channel_info = f_channel_info(playlist_id=playlist_id)

    # Act
    m_playlist_id = youtube_service.extract_channel_uploads_playlist_id(
        channel_info=channel_info
    )

    # Assert
    assert m_playlist_id == playlist_id


def test_extend_playlist_items(
    m_youtube_api,
    f_youtube_service,
    f_playlist_items_response,
    playlist_id: str = "123123",
    next_page_token: str = "def",
):
    # Arrange
    youtube_service = f_youtube_service(youtube_api=m_youtube_api)

    m_all_playlist_items = PlaylistItems([])
    m_playlist_items_response = f_playlist_items_response(
        playlist_id=playlist_id, next_page_token=next_page_token
    )
    m_youtube_api.get_channel_playlist_items.return_value = m_playlist_items_response

    # Act
    m_next_page_token = youtube_service.extend_playlist_items(
        all_playlist_items=m_all_playlist_items,
        playlist_id=playlist_id,
        next_page_token=None,
    )

    # Assert
    assert m_next_page_token == next_page_token
    assert m_all_playlist_items == PlaylistItems(m_playlist_items_response.items)


def test_paginate_all_playlist_items(
    m_youtube_api,
    f_youtube_service,
    f_playlist_items_response,
    playlist_id: str = "234234",
    next_page_token: str = "ghi",
):
    # Arrange
    youtube_service = f_youtube_service(youtube_api=m_youtube_api)

    page_1 = f_playlist_items_response(
        playlist_id=playlist_id, next_page_token=next_page_token
    )

    page_2 = f_playlist_items_response(playlist_id=playlist_id, next_page_token=None)

    m_youtube_api.get_channel_playlist_items.side_effect = [page_1, page_2]

    # Act
    m_all_playlist_items = youtube_service.paginate_all_playlist_items(
        playlist_id=playlist_id
    )

    # Assert
    assert m_youtube_api.get_channel_playlist_items.call_count == 2
    m_youtube_api.get_channel_playlist_items.assert_called_with(
        playlist_id=playlist_id, next_page_token=next_page_token
    )
    assert m_all_playlist_items == PlaylistItems(page_1.items + page_2.items)
