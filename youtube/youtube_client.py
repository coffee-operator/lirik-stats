from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
from googleapiclient.discovery import Resource


class YouTubeClient:
    """Credentials and setup to call YouTube APIs."""

    def __init__(
        self,
        key_file_path: Path,
        scopes: list[str],
        api_service_name: str,
        api_version: str,
        cache_discovery=False,
        credentials: Credentials = Credentials,
        discovery: discovery = discovery,
    ):
        self.credentials: Credentials = credentials.from_service_account_file(
            filename=key_file_path, scopes=scopes
        )

        self.resource: Resource = discovery.build(
            serviceName=api_service_name,
            version=api_version,
            credentials=self.credentials,
            cache_discovery=cache_discovery,
        )
