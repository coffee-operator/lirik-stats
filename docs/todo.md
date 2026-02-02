# Purpose

Lists opportunities to improve this codebase, organized by theme. Priority is unnecessary.

## Development

- Make unit tests run upon PR and require 100% passing for merge
- Add pre-commit hooks and PR actions for linting and formatting tools

## Features

- Add new data processing steps after raw/ to support data exploration
  - clean/ for data synthesis
  - agg/ for pre-aggregated
  - store as parquet and/or ducklake
- Add graphical user interface to explore/manipulate the repo's data

## Organization

- Refactor codebase to separate data, by channel, from logic
  - Rename this repo to "lirik_plays" and use for data
  - Create new repo "youtube_stats" and use for logic
