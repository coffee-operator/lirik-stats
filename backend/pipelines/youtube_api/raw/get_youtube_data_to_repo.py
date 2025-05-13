import utils
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(
    channel_id: str, 
    channel_folder_name: str, 
    key_file_path: str
):
    api_config = utils.declare_youtube_api_config(key_file_path)
    credentials = utils.create_service_account_credentials(api_config)
    youtube_resource = utils.create_youtube_api_resource(api_config, credentials)

    # get channel data
    response_channel = utils.get_channel_info(youtube_resource, channel_id)

    # identify uploads playlist, get metadata for all videos uploaded to channel
    uploads_playlist_id = utils.parse_channel_uploads_playlist_id(response_channel)
    # all_video_metadata = utils.paginate_all_channel_uploads(youtube_resource, uploads_playlist_id)

    # write raw channel & video data as json to code repo
    # channel
    file_path = f"../../../datasets/{channel_folder_name}/youtube_api/raw/channel/{datetime.now().strftime('%Y-%m-%d')}.json.gz"
    utils.write_object_to_json_gzip_file(response_channel, file_path)

    # # video
    # file_path = f"../../../datasets/{channel_folder_name}/youtube_api/raw/video/{datetime.now().strftime("%Y-%m-%d")}.json.gz"
    # utils.write_object_to_json_gzip_file(all_video_metadata, file_path)


if __name__ == "__main__":
    """Pull channel & video data from target YouTube Channel and store to indicated folder in repo"""
    # set defaults for main(), change with CLI args
    cli_args = utils.attach_cli_args_to_main(
        channel_id_default="UCebh6Np0l-DT9LXHrXbmopg",
        channel_folder_name_default="lirik_plays",
        key_file_path_default="key_youtube-stats-459404-eefde03eff46.json",
    )
    main(
        channel_id=cli_args.channel_id,
        channel_folder_name=cli_args.channel_folder_name,
        key_file_path=cli_args.key_file_path,
    )
