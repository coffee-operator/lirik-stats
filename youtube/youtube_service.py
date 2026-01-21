from typing import Iterator
from youtube.models import ChannelInfo, PlaylistItem, PlaylistItems
from youtube.youtube_api import YouTubeAPI
import logging

logger = logging.getLogger(__name__)


class YouTubeService:
    def __init__(self, youtube_api: YouTubeAPI):
        self.youtube_api = youtube_api

    def get_channel_info(self, channel_id: str) -> ChannelInfo:
        return self.youtube_api.get_channel_info(channel_id=channel_id)

    def extract_channel_uploads_playlist_id(self, channel_info: ChannelInfo) -> str:
        return self.youtube_api.extract_channel_uploads_playlist_id(channel_info)

    def fetch_next_playlist_items(
        self, playlist_id: str, next_page_token: str | None = None
    ) -> tuple[list[PlaylistItem], str] | None:
        playlist_item_response = self.youtube_api.get_channel_playlist_items(
            playlist_id=playlist_id, next_page_token=next_page_token
        )

        return playlist_item_response.items, playlist_item_response.nextPageToken

    def yield_all_playlist_items(
        self, playlist_id: str
    ) -> Iterator[list[PlaylistItem]]:
        i = 0
        next_page_token = None

        while True:
            i += 1
            logger.info(f"Calling batch {i} of playlist items")
            playlist_items, next_page_token = self.fetch_next_playlist_items(
                playlist_id=playlist_id, next_page_token=next_page_token
            )

            yield from playlist_items

            if not next_page_token:
                break

    def paginate_all_playlist_items(self, playlist_id: str) -> PlaylistItems:
        all_items = list(self.yield_all_playlist_items(playlist_id=playlist_id))

        return PlaylistItems(root=all_items)
