from youtube import config
from youtube.cli import parse_args
from youtube.models import MainCliArgs
from youtube.youtube_client import YouTubeClient
from youtube.youtube_api import YouTubeAPI
from youtube.youtube_service import YouTubeService
from youtube.storage_service import StorageService
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def run(
    args: MainCliArgs, youtube_service: YouTubeService, storage_service: StorageService
):
    """
    Handle run of application logic
    
    :param args: CLI arguments for running the program
    :type args: MainCliArgs
    :param youtube_service: Coordinates YouTube API calls
    :type youtube_service: YouTubeService
    :param storage_service: Handles file IO
    :type storage_service: StorageService
    """

    # pull data & log
    channel_info = youtube_service.get_channel_info(channel_id=args.channel_id)
    channel_uploads_playlist_id = youtube_service.extract_channel_uploads_playlist_id(
        channel_info=channel_info
    )
    all_playlist_items = youtube_service.paginate_all_playlist_items(
        playlist_id=channel_uploads_playlist_id
    )
    workflow_log = storage_service.create_run_log()

    # save
    storage_service.save_json_to_gz(data=channel_info, data_source="channel")
    storage_service.save_json_to_gz(data=all_playlist_items, data_source="video")
    storage_service.save_json_to_gz(data=workflow_log, data_source="workflow")


def main():
    # setup objects
    args = parse_args()
    youtube_client = YouTubeClient(
        key_file_path=args.key_file_path,
        scopes=config.SCOPES,
        api_service_name=config.API_SERVICE_NAME,
        api_version=config.API_VERSION,
        cache_discovery=config.CACHE_DISCOVERY,
    )

    youtube_api = YouTubeAPI(youtube_client)
    youtube_service = YouTubeService(youtube_api)
    storage_service = StorageService(
        channel_id=args.channel_id, channel_folder_name=args.channel_folder_name
    )

    run(args=args, youtube_service=youtube_service, storage_service=storage_service)


if __name__ == "__main__":
    main()
