from pathlib import Path
import config
import logging
from youtube_client import YouTubeClient
from youtube_api import YouTubeAPI
from youtube_service import YouTubeService


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def parse_args() -> dict:
    return {
        "channel_id": "UCebh6Np0l-DT9LXHrXbmopg",
        "channel_folder_name": "lirik_plays",
        "key_file_path": config.DEFAULT_KEY_FILE_PATH,
    }


def main():
    args = parse_args()

    # setup
    youtube_client = YouTubeClient(
        key_file_path=args["key_file_path"],
        scopes=config.SCOPES,
        api_service_name=config.API_SERVICE_NAME,
        api_version=config.API_VERSION,
        cache_discovery=config.CACHE_DISCOVERY,
    )

    youtube_api = YouTubeAPI(youtube_client)
    youtube_service = YouTubeService(youtube_api)

    # pull data
    channel_info = youtube_service.channel_info(channel_id=args["channel_id"])
    channel_uploads_playlist_id = youtube_service.channel_uploads_playlist_id(
        channel_info=channel_info
    )
    all_playlist_items = youtube_service.paginate_all_playlist_items(
        playlist_id=channel_uploads_playlist_id
    )

    # save
    

if __name__ == "__main__":
    main()
