import utils
from datetime import datetime
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main(
    channel_id: str, 
    channel_folder_name: str, 
    key_file_path: str
):
    # initilize api assets
    api_config = utils.declare_youtube_api_config(key_file_path)
    credentials = utils.create_service_account_credentials(api_config)
    youtube_resource = utils.create_youtube_api_resource(api_config, credentials)

    # get channel data
    response_channel = utils.get_channel_info(youtube_resource, channel_id)

    # identify uploads playlist, get metadata for all videos uploaded to channel
    uploads_playlist_id = utils.parse_channel_uploads_playlist_id(response_channel)
    all_video_metadata = utils.paginate_all_channel_uploads(youtube_resource, uploads_playlist_id)

    # log workflow run
    run_log = utils.create_workflow_run_log(channel_id, channel_folder_name)

    # write raw data to code repo as json.gz: channel, video, log
    utils.write_object_to_json_gzip_file(response_channel, utils.create_abs_file_path(channel_folder_name, "channel"))
    utils.write_object_to_json_gzip_file(all_video_metadata, utils.create_abs_file_path(channel_folder_name, "video"))
    utils.write_object_to_json_gzip_file(run_log, utils.create_abs_file_path(channel_folder_name, "workflow"))

if __name__ == "__main__":
    """Pull channel & video data from target YouTube Channel and store to indicated folder in repo"""
    # main() defaults to lirik_plays & local key, change with CLI args
    cli_args = utils.attach_cli_args_to_main()
    main(
        channel_id=cli_args.channel_id,
        channel_folder_name=cli_args.channel_folder_name,
        key_file_path=cli_args.key_file_path,
    )
