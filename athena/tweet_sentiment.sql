USING EXTERNAL FUNCTION detect_sentiment(text_col VARCHAR, lang VARCHAR) RETURNS VARCHAR LAMBDA 'textanalytics-udf' 

WITH tweet_sentiments AS (
    SELECT
        detect_sentiment(CAST(text AS VARCHAR), 'en') AS sentiment
    FROM tweets
)

SELECT
    sentiment,
    COUNT(1)
FROM tweet_sentiments
GROUP BY sentiment
