from youtube.storage_service import api_sources, data_stages, data_sources


def test_storage_service_init(
    storage_service,
    fixed_clock,
    fixed_uuid_provider,
    tmp_path,
    channel_id,
    channel_folder_name,
):
    # Arrange
    # fixture

    # Act
    # StorageService.__init__()

    # Assert
    assert storage_service.channel_id == channel_id
    assert storage_service.channel_folder_name == channel_folder_name
    assert storage_service.clock() == fixed_clock
    assert storage_service.uuid_provider() == fixed_uuid_provider
    assert storage_service.base_data_path == tmp_path


def test_get_now_timestamp(storage_service, fixed_clock, format="%Y-%m-%d %s"):
    # Arrange
    # fixture

    # Act
    now = storage_service.clock().strftime(format)
    t_now = fixed_clock.strftime(format)

    assert now == t_now


def test_create_run_log(
    storage_service,
    fixed_uuid_provider,
    channel_id,
    channel_folder_name,
    fixed_clock,
):
    # Arrange
    # fixture

    # Act
    workflow_log = storage_service.create_run_log()

    # Assert
    assert workflow_log.id == str(fixed_uuid_provider)
    assert workflow_log.channel_id == channel_id
    assert workflow_log.channel_folder_name == channel_folder_name
    assert workflow_log.run_date == fixed_clock.strftime("%Y-%m-%d")
    assert workflow_log.run_timestamp == fixed_clock.strftime("%Y-%m-%d_%H-%M-%S_%z")


def test_create_target_file_path(
    storage_service,
    tmp_path,
    channel_folder_name="lirik_plays",
    api_source: api_sources = "youtube_api",
    data_stage: data_stages = "raw",
    data_source: data_sources = "channel",
    json_gz_file_name="2026-01-23.json.gz",
):
    # Arrange
    # fixture

    # Act
    file_path = storage_service._create_target_file_path(
        api_source=api_source, data_stage=data_stage, data_source=data_source
    )

    m_file_path = (
        tmp_path
        / channel_folder_name
        / api_source
        / data_stage
        / data_source
        / json_gz_file_name
    )

    # Assert
    assert file_path == m_file_path


def test_save_json_to_gz(
    storage_service,
    api_source: api_sources = "youtube_api",
    data_stage: data_stages = "raw",
    data_source: data_sources = "channel",
):
    # Arrange
    workflow_log = storage_service.create_run_log()

    # Act
    file_path = storage_service.save_json_to_gz(workflow_log, data_source=data_source)
    m_file_path = storage_service._create_target_file_path(
        api_source=api_source, data_stage=data_stage, data_source=data_source
    )

    # Assert
    assert file_path.exists()
    assert file_path == m_file_path
