from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from googleapiclient.discovery import Resource


class YouTubeClient:
    def __init__(
        self,
        key_file_path: Path,
        scopes: list[str],
        api_service_name: str,
        api_version: str,
        cache_discovery=False,
    ):
        self.credentials: Credentials = Credentials.from_service_account_file(
            filename=key_file_path, scopes=scopes
        )

        self.resource: Resource = discovery.build(
            serviceName=api_service_name,
            version=api_version,
            credentials=self.credentials,
            cache_discovery=cache_discovery,
        )

if __name__ == "__main__":
    KEY_FILE_PATH = Path("./pipelines/youtube_api/raw/key_youtube-stats.json")

    youtube_client = YouTubeClient(
        key_file_path=KEY_FILE_PATH,
        scopes=["https://www.googleapis.com/auth/youtube.readonly"],
        api_service_name="youtube",
        api_version="v3"
    )

    print(youtube_client)