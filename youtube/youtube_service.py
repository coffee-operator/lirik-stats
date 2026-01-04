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

    def extend_playlist_items(
        self,
        all_playlist_items: PlaylistItems,
        playlist_id: str,
        next_page_token: str = None,
    ) -> list[dict]:
        logger.info("Calling next batch of playlist items")
        playlist_item_response = self.youtube_api.get_channel_playlist_items(
            playlist_id=playlist_id, next_page_token=next_page_token
        )

        all_playlist_items.root.extend(playlist_item_response.items)

        return playlist_item_response.nextPageToken

    def paginate_all_playlist_items(self, playlist_id: str) -> list[PlaylistItem]:
        all_playlist_items = PlaylistItems([])
        next_page_token = self.extend_playlist_items(all_playlist_items, playlist_id)

        while next_page_token:
            next_page_token = self.extend_playlist_items(
                all_playlist_items, playlist_id, next_page_token
            )

        return all_playlist_items
