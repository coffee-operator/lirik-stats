from youtube.models import ChannelInfo
from youtube.youtube_api import YouTubeAPI


def test_youtube_api_init(mock_youtube_client, api_service_name: str = "fake_value"):
    # Arrange
    mock_youtube_client.resource.api_service_name.return_value = api_service_name
    youtube_api = YouTubeAPI(youtube_client=mock_youtube_client)

    # Act
    # YouTubeAPI__init__()

    # Assert
    assert youtube_api.youtube_client == mock_youtube_client
    assert youtube_api.resource == mock_youtube_client.resource


def test_youtube_api_get_channel_info(
    mock_youtube_client, factory_channel_info, channel_id: str = "123123"
):
    # Arrange
    mock_youtube_client.resource.channels.return_value.list.return_value.execute.return_value = factory_channel_info(
        channel_id=channel_id
    ).model_dump()
    youtube_api = YouTubeAPI(youtube_client=mock_youtube_client)

    # Act
    channel_info = youtube_api.get_channel_info(channel_id=channel_id)

    # Assert
    assert isinstance(channel_info, ChannelInfo)
    assert channel_info.pageInfo["channelId"] == channel_id


def test_extract_channel_uploads_playlist_id(
    mock_youtube_client, factory_channel_info, playlist_id: str = "123123"
):
    # Arrange
    youtube_api = YouTubeAPI(youtube_client=mock_youtube_client)

    # Act
    m_playlist_id = youtube_api.extract_channel_uploads_playlist_id(
        factory_channel_info(playlist_id=playlist_id)
    )

    # Assert
    assert m_playlist_id == playlist_id


def test_youtube_api_get_channel_playlist_items(
    mock_youtube_client, factory_playlist_items_response, playlist_id: str = "abcabc"
):
    # Arrange
    mock_youtube_client.resource.playlistItems.return_value.list.return_value.execute.return_value = (
        factory_playlist_items_response(playlist_id=playlist_id)
    ).model_dump()
    youtube_api = YouTubeAPI(youtube_client=mock_youtube_client)

    # Act
    playlist_items_response = youtube_api.get_channel_playlist_items(
        playlist_id=playlist_id
    )

    # Assert
    assert (
        playlist_items_response.items[0].contentDetails["relatedPlaylists"]["uploads"]
        == playlist_id
    )
