import gzip
import json
from typing import Any, Literal
import config
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger(__name__)

type data_sources = Literal["channel", "video", "workflow"]

class StorageService:
    def __init__(self, channel_folder_name: str):
        self.channel_folder_name = channel_folder_name
        self.storage_base_path = config.BASE_DATA_PATH / channel_folder_name / "youtube_api" / "raw"

    def _get_timestamp(self, format: str = '%Y-%m-%d'):
        return datetime.now(timezone.utc).strftime(format)
    
    def save_json_to_gz(self, data: Any, data_source: data_sources):
        file_path = self.storage_base_path / data_source / f"{self._get_timestamp()}.json.gz"
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(object, f, indent=4)
        logger.info(f"Object written to {file_path}")

    
