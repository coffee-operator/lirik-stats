-- 


CREATE OR REPLACE TABLE channel_history (
    id VARCHAR PRIMARY KEY,
    channel_id VARCHAR,
    file_name VARCHAR,
    date_api_pull DATE,
    rank_api_pull INTEGER,
    is_current BOOLEAN,
    kind VARCHAR,
    etag VARCHAR,
    name VARCHAR,
    description VARCHAR,
    custom_url VARCHAR,
    thumbnail_url VARCHAR,
    playlist_uploads_id VARCHAR,
    view_count INTEGER,
    subscriber_count INTEGER,
    topic_ids VARCHAR[],
    topic_categories VARCHAR[]
    
);

CREATE OR REPLACE TABLE channel (
    id VARCHAR PRIMARY KEY,
    history_id VARCHAR,
    file_name VARCHAR,
    date_api_pull DATE,
    rank_api_pull INTEGER,
    is_current BOOLEAN,
    kind VARCHAR,
    etag VARCHAR,
    name VARCHAR,
    description VARCHAR,
    custom_url VARCHAR,
    thumbnail_url VARCHAR,
    playlist_uploads_id VARCHAR,
    view_count INTEGER,
    subscriber_count INTEGER,
    topic_ids VARCHAR[],
    topic_categories VARCHAR[]
);

INSERT INTO
    channel_history
SELECT
    md5(id || filename) AS id,
    id AS channel_id,
    filename AS file_name,
    CAST(regexp_replace(split_part(filename, '/', -1), '.json.gz', '') AS date) AS date_api_pull,
    row_number() OVER (ORDER BY date_api_pull DESC) AS rank_api_pull,
    CASE
        WHEN rank_api_pull = 1 THEN True
        ELSE False
    END AS is_current,
    kind,
    etag,
    snippet['title'] AS name,
    snippet['description'] AS description,
    snippet['customUrl'] AS custom_url,
    snippet['thumbnails']['default']['url'] AS thumbnail_url,
    contentDetails['relatedPlaylists']['uploads'] AS playlist_uploads_id,
    statistics['viewCount'] AS view_count,
    statistics['subscriberCount'] AS subscriber_count,
    topicDetails['topicIds'] as topic_ids,
    topicDetails['topicCategories'] as topic_categories
FROM (
    SELECT
        unnest(items[1]),
        filename,
    FROM
        read_json('./backend/datasets/lirik_plays/youtube_api/raw/channel/*.json.gz', filename=True)
);

INSERT INTO
    channel
SELECT
    channel_id AS id,
    id as history_id,
    file_name,
    date_api_pull,
    rank_api_pull,
    is_current,
    kind,
    etag,
    name,
    description,
    custom_url,
    thumbnail_url,
    playlist_uploads_id,
    view_count,
    subscriber_count,
    topic_ids,
    topic_categories
FROM 
    channel_history
WHERE
    is_current = True;

-- .mode line
-- SELECT * FROM channel;

-- .mode box
-- DESCRIBE channel;

EXPORT DATABASE 'backend/datasets/lirik_plays/youtube_api/clean/' (
    FORMAT parquet
);
