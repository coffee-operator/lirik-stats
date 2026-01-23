from datetime import datetime, timezone
from pathlib import Path
import uuid

from pytest import fixture
from youtube.storage_service import (
    StorageService,
    api_sources,
    data_stages,
    data_sources,
)


@fixture
def m_channel_id() -> str:
    return "123abc"


@fixture
def m_channel_folder_name() -> str:
    return "alpha"


@fixture
def m_clock() -> datetime:
    return datetime(2026, 1, 23, 12, 0, 0, tzinfo=timezone.utc)


@fixture
def m_uuid_provider() -> uuid:
    return uuid.UUID("d8d2e059-bbb9-47c8-9907-c2b0bbdeaf1d")


@fixture
def m_base_data_path(tmp_path) -> Path:
    return tmp_path


@fixture
def m_json_gz_file_name(m_clock, format="%Y-%m-%d") -> str:
    return f"{m_clock.strftime(format)}.json.gz"

@fixture
def m_storage_service(
    m_channel_id,
    m_channel_folder_name,
    m_clock,
    m_uuid_provider,
    m_base_data_path,
) -> StorageService:
    return StorageService(
        channel_id=m_channel_id,
        channel_folder_name=m_channel_folder_name,
        clock=lambda: m_clock,
        uuid_provider=lambda: m_uuid_provider,
        base_data_path=m_base_data_path,
    )


def test_storage_service_init(
    m_storage_service,
    m_clock,
    m_uuid_provider,
    m_base_data_path,
    m_channel_id,
    m_channel_folder_name,
):
    # Arrange
    # fixture

    # Act
    # StorageService.__init__()

    # Assert
    assert m_storage_service.channel_id == m_channel_id
    assert m_storage_service.channel_folder_name == m_channel_folder_name
    assert m_storage_service.clock() == m_clock
    assert m_storage_service.uuid_provider() == m_uuid_provider
    assert m_storage_service.base_data_path == m_base_data_path


def test_get_now_timestamp(m_storage_service, m_clock, format="%Y-%m-%d %s"):
    # Arrange
    # fixture

    # Act
    now = m_storage_service.clock().strftime(format)
    m_now = m_clock.strftime(format)

    assert now == m_now


def test_create_run_log(
    m_storage_service, m_uuid_provider, m_channel_id, m_channel_folder_name, m_clock
):
    # Arrange
    # fixture

    # Act
    workflow_log = m_storage_service.create_run_log()

    # Assert
    assert workflow_log.id == str(m_uuid_provider)
    assert workflow_log.channel_id == m_channel_id
    assert workflow_log.channel_folder_name == m_channel_folder_name
    assert workflow_log.run_date == m_clock.strftime("%Y-%m-%d")
    assert workflow_log.run_timestamp == m_clock.strftime("%Y-%m-%d_%H-%M-%S_%z")


def test_create_target_file_path(
    m_storage_service,
    m_base_data_path,
    m_channel_folder_name,
    m_json_gz_file_name,
    api_source: api_sources = "youtube_api",
    data_stage: data_stages = "raw",
    data_source: data_sources = "sync",
):
    # Arrange
    # fixture

    # Act
    file_path = m_storage_service._create_target_file_path(
        api_source=api_source,
        data_stage=data_stage,
        data_source=data_source
    )

    m_file_path = (
        m_base_data_path
        / m_channel_folder_name
        / api_source
        / data_stage
        / data_source
        / m_json_gz_file_name
    )

    # Assert
    assert file_path == m_file_path
