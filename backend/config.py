from pathlib import Path

# YouTube client credentials and resource values
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CACHE_DISCOVERY = False

# Folder paths
REPO_BASE_PATH = Path(__file__).resolve().parent
DEFAULT_KEY_FILE_PATH = REPO_BASE_PATH / "backend" / "key_youtube-stats.json"
BASE_DATA_PATH = REPO_BASE_PATH / "backend" / "datasets"
