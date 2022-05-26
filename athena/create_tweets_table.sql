CREATE EXTERNAL TABLE IF NOT EXISTS tweets (
    id BIGINT,
    text STRING,
    created_at STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://machine-learning-workshop/data/tweets/'
