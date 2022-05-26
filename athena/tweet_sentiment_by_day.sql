USING EXTERNAL FUNCTION detect_sentiment(text_col VARCHAR, lang VARCHAR) RETURNS VARCHAR LAMBDA 'textanalytics-udf'

WITH tweet_sentiments AS (
    SELECT
        detect_sentiment(CAST(text AS VARCHAR), 'en') AS sentiment,
        format_datetime(date_parse(created_at, '%a %b %d %H:%i:%s +0000 %Y'), 'YYYY-MM-dd') AS post_date
    FROM tweets
)

SELECT
    post_date,
    sentiment,
    COUNT(1) AS sentiment_cnt,
    100.0 * COUNT(1) / SUM(COUNT(1)) OVER (PARTITION BY post_date) AS sentiment_ratio
FROM tweet_sentiments
GROUP BY post_date, sentiment
ORDER BY post_date, sentiment
