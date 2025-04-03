set @query="쓰레드 풀링";
select sys.ML_EMBED_ROW(@query, JSON_OBJECT("model_id", "cohere.embed-multilingual-v3.0")) into @query_embedding;

SELECT question, answer, 
       round(1-DISTANCE(question_vector, @query_embedding, 'COSINE'),2) as score
FROM customer_qa
ORDER BY score DESC
LIMIT 3;
