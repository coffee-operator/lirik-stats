from unittest.mock import MagicMock
from youtube.models import ChannelInfo, PlaylistItems
from youtube.youtube_api import YouTubeAPI


def test_youtube_service_init(mock_youtube_api, factory_youtube_service):
    # Arrange
    youtube_service = factory_youtube_service(youtube_api=mock_youtube_api)

    # Act
    # YouTubeService.__init_()

    # Assert
    assert youtube_service.youtube_api == mock_youtube_api


def test_get_channel_info(
    mock_youtube_api,
    factory_youtube_service,
    factory_channel_info,
    channel_id: str = "abcabc",
):
    # Arrange
    youtube_service = factory_youtube_service(youtube_api=mock_youtube_api)
    mock_youtube_api.get_channel_info.return_value = factory_channel_info(
        channel_id=channel_id
    )

    # Act
    channel_info = youtube_service.get_channel_info(channel_id=channel_id)

    # Assert
    assert isinstance(channel_info, ChannelInfo)
    assert channel_info.pageInfo["channelId"] == channel_id


def test_extract_channel_uploads_playlist_id(
    factory_youtube_service, factory_channel_info, playlist_id: str = "123123"
):
    # Arrange
    youtube_api = YouTubeAPI(youtube_client=MagicMock())
    youtube_service = factory_youtube_service(youtube_api=youtube_api)
    channel_info = factory_channel_info(playlist_id=playlist_id)

    # Act
    m_playlist_id = youtube_service.extract_channel_uploads_playlist_id(
        channel_info=channel_info
    )

    # Assert
    assert m_playlist_id == playlist_id


def test_fetch_next_playlist_items(
    mock_youtube_api,
    factory_youtube_service,
    factory_playlist_items_response,
    playlist_id: str = "432432",
    next_page_token: str = "hij",
):
    # Arrange
    youtube_service = factory_youtube_service(youtube_api=mock_youtube_api)
    m_playlist_item_response = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token=next_page_token
    )
    mock_youtube_api.get_channel_playlist_items.return_value = m_playlist_item_response

    # Act
    playlist_items, m_next_page_token = youtube_service.fetch_next_playlist_items(
        playlist_id=playlist_id, next_page_token=next_page_token
    )

    # Assert
    assert m_next_page_token == next_page_token
    assert m_playlist_item_response.items == playlist_items


def test_yield_all_playlist_items(
    mock_youtube_api,
    factory_youtube_service,
    factory_playlist_items_response,
    playlist_id: str = "123",
):
    # Arrange
    youtube_service = factory_youtube_service(youtube_api=mock_youtube_api)
    page_1 = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token="1"
    )
    page_2 = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token="2"
    )
    page_3 = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token=None
    )
    mock_youtube_api.get_channel_playlist_items.side_effect = [page_1, page_2, page_3]

    # Act
    m_all_items = list(
        youtube_service.yield_all_playlist_items(playlist_id=playlist_id)
    )

    # Assert
    assert mock_youtube_api.get_channel_playlist_items.call_count == 3
    assert m_all_items == (page_1.items + page_2.items + page_3.items)


def test_paginate_all_playlist_items(
    mock_youtube_api,
    factory_youtube_service,
    factory_playlist_items_response,
    playlist_id: str = "456",
):
    # Arrange
    youtube_service = factory_youtube_service(youtube_api=mock_youtube_api)
    page_1 = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token="1"
    )
    page_2 = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token="2"
    )
    page_3 = factory_playlist_items_response(
        playlist_id=playlist_id, next_page_token=None
    )
    mock_youtube_api.get_channel_playlist_items.side_effect = [page_1, page_2, page_3]

    # Act
    m_all_playlist_items = youtube_service.paginate_all_playlist_items(
        playlist_id=playlist_id
    )

    # Assert
    assert mock_youtube_api.get_channel_playlist_items.call_count == 3
    assert m_all_playlist_items == PlaylistItems(
        page_1.items + page_2.items + page_3.items
    )
