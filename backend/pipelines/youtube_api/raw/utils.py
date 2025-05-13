import os
import googleapiclient.discovery
from google.oauth2 import service_account
from dotenv import load_dotenv
import json
from typing import List, Union
import gzip
import argparse
import logging

load_dotenv()
logger = logging.getLogger(__name__)


def declare_youtube_api_config(key_file_path: str = None) -> dict:
    return {
        "scopes": ["https://www.googleapis.com/auth/youtube.readonly"],
        "api_service_name": "youtube",
        "api_version": "v3",
        "key_file_path": key_file_path,
    }


def create_service_account_credentials(api_config: dict) -> service_account.Credentials:
    return service_account.Credentials.from_service_account_file(
        filename=api_config["key_file_path"], scopes=api_config["scopes"]
    )


def create_youtube_api_resource(
    api_config: dict, 
    credentials: service_account.Credentials
) -> googleapiclient.discovery.Resource:
    return googleapiclient.discovery.build(
        serviceName=api_config["api_service_name"],
        version=api_config["api_version"],
        credentials=credentials,
        cache_discovery=False,
    )


def get_channel_info(
    youtube_resource: googleapiclient.discovery.Resource, 
    id: str
) -> dict:
    request = youtube_resource.channels().list(
        part="snippet,contentDetails,statistics,topicDetails,status", id=id
    )
    return request.execute()


def parse_channel_uploads_playlist_id(response_channel: dict) -> str:
    return response_channel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def paginate_all_channel_uploads(
    youtube_resource: googleapiclient.discovery.Resource, 
    uploads_playlist_id: str
) -> List[dict]:
    def get_uploads_playlist_items(next_page_token: str = None):
        request = youtube_resource.playlistItems().list(
            part="snippet,contentDetails,status",
            maxResults=50,
            playlistId=uploads_playlist_id,
            pageToken=next_page_token,
        )
        response_playlist_items = request.execute()

        return response_playlist_items

    video_metadata = []
    response_playlist_items = get_uploads_playlist_items()
    video_metadata.extend(response_playlist_items["items"])

    while response_playlist_items.get("nextPageToken"):
        response_playlist_items = get_uploads_playlist_items(
            response_playlist_items.get("nextPageToken")
        )
        video_metadata.extend(response_playlist_items["items"])

    return video_metadata


def create_file_path_if_doesnt_exist(file_path: str) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def write_object_to_json_gzip_file(
    object: Union[dict, List[dict]], 
    file_path: str
) -> None:
    create_file_path_if_doesnt_exist(file_path)
    with gzip.open(file_path, "wt", encoding="utf-8") as f:
        json.dump(object, f, indent=4)
        logger.info(f"Object written to {file_path}")


class MainCliArgs(argparse.Namespace):
    channel_id: str
    channel_folder_name: str
    key_file_path: str


def attach_cli_args_to_main(
    channel_id_default: str,
    channel_folder_name_default: str,
    key_file_path_default: str,
) -> MainCliArgs:
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--channel_id",
        type=str,
        default=channel_id_default,
        help="YouTube channel unique ID as a string",
    )
    parser.add_argument(
        "--channel_folder_name",
        type=str,
        default=channel_folder_name_default,
        help="Folder name to hold YouTube API data as a string",
    )
    parser.add_argument(
        "--key_file_path",
        type=str,
        default=key_file_path_default,
        help="Key file path name as a string",
    )

    return parser.parse_args()
