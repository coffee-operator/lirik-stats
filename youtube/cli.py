import argparse
from youtube import config
from youtube.models import MainCliArgs


def parse_args() -> MainCliArgs:
    parser = argparse.ArgumentParser(
        description="Pipeline to reterieve Youtube API data"
    )
    parser.add_argument(
        "--key_file_path",
        type=str,
        default=str(config.DEFAULT_KEY_FILE_PATH),
        help="File path to the service account API credential that authorizes calls to the YouTube API",
    )
    parser.add_argument(
        "--channel_id",
        type=str,
        default=config.DEFAULT_CHANNEL_ID,
        help="Unique identifier for the target YouTube account",
    )
    parser.add_argument(
        "--channel_folder_name",
        type=str,
        default=config.DEFAULT_CHANNEL_FOLDER_NAME,
        help="Snakecase, human-readable name of the target YouTube account",
    )

    return parser.parse_args()
