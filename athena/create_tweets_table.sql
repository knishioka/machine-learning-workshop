CREATE EXTERNAL TABLE IF NOT EXISTS tweets (
    id BIGINT,
    test string,
    created_at string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://machine-learning-workshop/data/tweets/'
