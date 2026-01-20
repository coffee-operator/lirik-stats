import gzip
import json
from typing import Callable, Literal
from datetime import datetime, timezone
import uuid
import logging
from pydantic import BaseModel
from youtube import config
from youtube.models import WorkflowLog


logger = logging.getLogger(__name__)

type data_sources = Literal["channel", "video", "workflow"]


class StorageService:
    def __init__(
        self,
        channel_id: str,
        channel_folder_name: str,
        clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
        uuid_provider: Callable[[], uuid.UUID] = lambda: uuid.uuid4,
    ):
        self.channel_id = channel_id
        self.channel_folder_name = channel_folder_name
        self.clock = clock
        self.uuid_provider = uuid_provider
        self.storage_base_path = (
            config.BASE_DATA_PATH / channel_folder_name / "youtube_api" / "raw"
        )

    def _get_now_timestamp(self, format: str = "%Y-%m-%d"):
        return self.clock().strftime(format)

    def create_run_log(self) -> WorkflowLog:
        return WorkflowLog(
            id=str(self.uuid_provider()),
            channel_id=self.channel_id,
            channel_folder_name=self.channel_folder_name,
            run_date=self._get_now_timestamp("%Y-%m-%d"),
            run_timestamp=self._get_now_timestamp("%Y-%m-%d_%H-%M-%S_%z"),
        )

    def save_json_to_gz(self, data: BaseModel, data_source: data_sources):
        file_path = (
            self.storage_base_path
            / data_source
            / f"{self._get_now_timestamp()}.json.gz"
        )
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with gzip.open(file_path, "wt", encoding="utf-8") as f:
            json.dump(data.model_dump(), f, indent=4)
        logger.info(f"Object {data.__class__} written to {file_path}")
