# AGENTS.md

This file contains guidelines and commands for agentic coding agents working in this repository.

## Build/Lint/Test Commands

### Linting and Formatting
```bash
# Run ruff linter (checks for style and error issues)
ruff check

# Run ruff with auto-fix
ruff check --fix

# Run ruff on specific file
ruff check path/to/file.py

# Run ruff in watch mode for continuous linting
ruff check --watch
```

### Testing
This project currently does not have formal test commands configured. When implementing tests, use standard Python testing patterns and update this section.

### Running the Application
```bash
# Run the main YouTube data pipeline
python backend/pipelines/youtube_api/raw/get_youtube_data_to_repo.py

# Run with custom arguments
python backend/pipelines/youtube_api/raw/get_youtube_data_to_repo.py --channel_id <ID> --channel_folder_name <NAME> --key_file_path <PATH>
```

## Code Style Guidelines

### Python Version and Requirements
- **Python Version**: >=3.13 (as specified in pyproject.toml)
- **Package Manager**: Uses uv with uv.lock file
- **Dependencies**: Managed through pyproject.toml

### Import Organization
- Standard library imports first (os, json, logging, pathlib, datetime, uuid, argparse)
- Third-party imports next (googleapiclient, google.oauth2, dotenv, polars, duckdb, requests)
- Local imports last (utils, custom modules)
- Use `from typing import List, Union` for type hints
- Import `load_dotenv()` early in utility modules

### Type Hints
- Use type hints for all function parameters and return values
- Preferred types: `str`, `int`, `bool`, `Path`, `List[dict]`, `Union[dict, List[dict]]`
- Use `Path` from pathlib for file paths instead of strings
- Complex objects can use `dict` when appropriate
- Example: `def create_service_account_credentials(api_config: dict) -> service_account.Credentials:`

### Naming Conventions
- **Functions**: snake_case with descriptive names (e.g., `get_channel_info`, `paginate_all_channel_uploads`)
- **Variables**: snake_case, be descriptive (e.g., `uploads_playlist_id`, `next_page_token`)
- **Classes**: PascalCase (e.g., `YouTubeClient`, `MainCliArgs`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `KEY_FILE_PATH`)
- **Private methods**: prefix with underscore if needed

### Function Structure
- Keep functions focused and single-purpose
- Use docstrings for complex functions
- Parameter ordering: required parameters first, optional with defaults last
- Return types should be explicit and consistent

### Error Handling
- Use logging for error reporting: `logger = logging.getLogger(__name__)`
- Configure logging at module level: `logging.basicConfig(level=logging.INFO)`
- Log successful operations: `logger.info(f"Object written to {file_path}")`
- Handle API errors gracefully in external service calls

### File Organization
- **Backend structure**: `backend/` contains main application code
- **Pipelines**: `backend/pipelines/youtube_api/` for data processing workflows
- **Raw data**: `backend/datasets/{channel_name}/youtube_api/raw/` for stored API responses
- **Utilities**: Keep utility functions in dedicated `utils.py` files
- **Configuration**: Use `config.py` for configuration constants

### API Integration Patterns
- Use service account credentials for Google APIs
- Build API resources with `googleapiclient.discovery.build()`
- Handle pagination with while loops checking `nextPageToken`
- Store raw API responses as compressed JSON (`.json.gz`)
- Use UTC timestamps for all datetime operations

### Data Storage Patterns
- Store data in date-partitioned files: `YYYY-MM-DD.json.gz`
- Use gzip compression for JSON files to save space
- Create directories automatically: `os.makedirs(os.path.dirname(file_path), exist_ok=True)`
- Maintain workflow logs with UUIDs for tracking

### CLI Argument Handling
- Use `argparse.ArgumentParser()` for command-line interfaces
- Create custom `argparse.Namespace` subclasses for type hints
- Provide sensible defaults for all arguments
- Include help text for all CLI arguments

### Environment Configuration
- Use `.env` files for environment variables
- Load with `load_dotenv()` at module level
- Never commit sensitive credentials or API keys
- Use service account JSON files for Google API authentication

### Code Quality
- Run `ruff check` before committing changes
- Fix auto-fixable issues with `ruff check --fix`
- Keep lines under reasonable length (ruff will enforce)
- Use meaningful variable and function names
- Avoid commented-out code in final commits

## Project-Specific Patterns

### YouTube API Pipeline
- Channel data flow: channel → uploads playlist → video metadata
- Always store raw API responses before processing
- Use workflow logs to track data collection runs
- File naming: `{channel_folder}/{data_type}/{date}.json.gz`

### Data Analysis
- Use DuckDB for SQL-based analysis (see `backend/analyses/eda.sql`)
- Use Polars for DataFrame operations when needed
- Jupyter notebooks available in `backend/analyses/` for exploratory work

## Development Workflow
1. Make changes to code
2. Run `ruff check --fix` to handle style issues
3. Test functionality manually (no formal test suite yet)
4. Commit changes with descriptive messages
5. Update documentation if needed

## Notes
- This is a data collection and analysis project focused on YouTube statistics
- The main workflow collects data from the Lirik YouTube channel
- Data is stored in a compressed JSON format for efficient storage
- No formal testing framework is currently implemented