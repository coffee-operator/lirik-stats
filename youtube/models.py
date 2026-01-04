import argparse
from typing import Optional
from pydantic import BaseModel, RootModel

class MainCliArgs(argparse.Namespace):
    key_file_path: str
    channel_id: str
    channel_folder_name: str


class ChannelInfo(BaseModel):
    kind: str
    etag: str
    pageInfo: dict
    items: list[dict]


class PlaylistItem(BaseModel):
    kind: str
    etag: str
    id: str
    snippet: dict
    contentDetails: dict
    status: dict


class PlaylistItems(RootModel):
    root: list[PlaylistItem]


class PlaylistItemsResponse(BaseModel):
    kind: str
    etag: str
    nextPageToken: Optional[str] = None
    items: list[PlaylistItem]
    pageInfo: dict


class WorkflowLog(BaseModel):
    id: str
    channel_id: str
    channel_folder_name: str
    run_date: str
    run_timestamp: str
