USING EXTERNAL FUNCTION detect_sentiment(text_col VARCHAR, lang VARCHAR) RETURNS VARCHAR LAMBDA 'textanalytics-udf'
SELECT detect_sentiment(CAST(text AS VARCHAR), 'en') AS sentiment FROM tweets
