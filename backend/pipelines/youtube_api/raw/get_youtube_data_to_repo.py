import utils
from datetime import datetime
from typing import ClassVar
import argparse


def main(
    channel_id: str = "UCebh6Np0l-DT9LXHrXbmopg",
    channel_folder_name: str = "lirk_plays"
):
    api_config = utils.declare_youtube_api_config()
    credentials = utils.create_service_account_credentials(api_config)
    youtube_resource = utils.create_youtube_api_resource(api_config, credentials)

    # identify channel
    response_channel = utils.get_channel_info(youtube_resource, channel_id)

    # identify uploads playlist, pull all videos
    uploads_playlist_id = utils.parse_channel_uploads_playlist_id(response_channel)
    all_video_metadata = utils.paginate_all_channel_uploads(youtube_resource, uploads_playlist_id)

    # write raw channel & video data as json to code repo
    # channel
    file_path = f"../../../datasets/{channel_folder_name}/youtube_api/raw/channel/{datetime.now().strftime("%Y-%m-%d")}.json.gz"
    utils.write_object_to_json_gzip_file(response_channel, file_path)

    # video
    file_path = f"../../../datasets/{channel_folder_name}/youtube_api/raw/video/{datetime.now().strftime("%Y-%m-%d")}.json.gz"
    utils.write_object_to_json_gzip_file(all_video_metadata, file_path)


if __name__ == "__main__":
    # pull channel & video data from target YouTube Channel and store to indicated folder in repo
    cli_args = utils.attach_cli_args_to_main()
    main(
        channel_id=cli_args["channel_id"],
        channel_folder_name=cli_args["channel_folder_name"]
    )