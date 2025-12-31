from googleapiclient.discovery import Resource
from youtube_client import YouTubeClient


class YouTubeAPI:
    """Handles YouTube API definitions."""

    def __init__(self, youtube_client: YouTubeClient):
        self.youtube_client = youtube_client

    @property
    def resource(self) -> Resource:
        return self.youtube_client.resource

    def get_channel_info(
        self,
        channel_id: str,
        query_parts="snippet,contentDetails,statistics,topicDetails,status",
    ) -> dict:
        return self.resource.channels().list(part=query_parts, id=channel_id).execute()

    def extract_channel_uploads_playlist_id(self, channel_info: dict) -> str:
        return channel_info["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def get_channel_playlist_items(
        self,
        playlist_id: str,
        query_parts="snippet,contentDetails,status",
        max_results=50,
        next_page_token: str = None,
    ) -> dict:
        return (
            self.resource.playlistItems()
            .list(
                playlistId=playlist_id,
                part=query_parts,
                maxResults=max_results,
                pageToken=next_page_token,
            )
            .execute()
        )
