from unittest.mock import patch
from youtube.cli import parse_cli_args
from youtube.models import MainCliArgs
from youtube import config
from main import main, run


def test_run(
    factory_youtube_service,
    mock_youtube_api,
    factory_channel_info,
    factory_playlist_items_response,
    storage_service,
    playlist_id: str = "123123123",
):
    # Arrange
    ## cli args
    args = MainCliArgs(
        key_file_path=config.DEFAULT_KEY_FILE_PATH,
        channel_id=config.DEFAULT_CHANNEL_ID,
        channel_folder_name=config.DEFAULT_CHANNEL_FOLDER_NAME,
    )

    ## YouTubeService
    youtube_service = factory_youtube_service(youtube_api=mock_youtube_api)

    ### Mock YouTubeService internal calls
    mock_youtube_api.get_channel_info.return_value = factory_channel_info(
        channel_id=args.channel_id, playlist_id=playlist_id
    )

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

    ## StorageService
    # fixture

    # Act
    run(args=args, youtube_service=youtube_service, storage_service=storage_service)

    m_channel_file_path = storage_service._create_target_file_path(
        api_source="youtube_api", data_stage="raw", data_source="channel"
    )
    m_video_file_path = storage_service._create_target_file_path(
        api_source="youtube_api", data_stage="raw", data_source="video"
    )
    m_workflow_file_path = storage_service._create_target_file_path(
        api_source="youtube_api", data_stage="raw", data_source="workflow"
    )

    # Assert
    assert m_channel_file_path.exists()
    assert m_video_file_path.exists()
    assert m_workflow_file_path.exists()


@patch("main.YouTubeClient")
@patch("main.YouTubeAPI")
@patch("main.YouTubeService")
@patch("main.StorageService")
@patch("main.run")
def test_main_setup(
    p_run,
    p_storage_service,
    p_youtube_service,
    p_youtube_api,
    p_youtube_client,
    key_file_path: str = str(config.DEFAULT_KEY_FILE_PATH),
    channel_id: str = "123123",
    channel_folder_name: str = "lirik_wins",
):
    # Strategy is to test the wiring between my Objects, not the business logic handled by run(),
    # since that's addressed above

    # Arrange
    cli_args = [
        "--key_file_path",
        key_file_path,
        "--channel_id",
        channel_id,
        "--channel_folder_name",
        channel_folder_name,
    ]

    # Act
    main(cli_args=cli_args)
    ## main internal call
    args = parse_cli_args(cli_args=cli_args)

    # Assert
    assert args.key_file_path == key_file_path
    assert args.channel_id == channel_id
    assert args.channel_folder_name == channel_folder_name

    p_youtube_client.assert_called_once_with(
        key_file_path=key_file_path,
        scopes=config.SCOPES,
        api_service_name=config.API_SERVICE_NAME,
        api_version=config.API_VERSION,
        cache_discovery=config.CACHE_DISCOVERY,
    )
    p_youtube_api.assert_called_once_with(p_youtube_client.return_value)
    p_youtube_service.assert_called_once_with(p_youtube_api.return_value)
    p_storage_service.assert_called_once_with(
        channel_id=channel_id, channel_folder_name=channel_folder_name
    )

    p_run.assert_called_once_with(
        args=args,
        youtube_service=p_youtube_service.return_value,
        storage_service=p_storage_service.return_value,
    )
