from youtube import config
from youtube.cli import parse_cli_args


def test_parse_cli_args(
    key_file_path: str = str(config.DEFAULT_KEY_FILE_PATH),
    channel_id: str = "123123",
    channel_folder_name: str = "lirik_wins",
):
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
    args = parse_cli_args(cli_args)

    # Assert
    assert args.key_file_path == key_file_path
    assert args.channel_id == channel_id
    assert args.channel_folder_name == channel_folder_name
