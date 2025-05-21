
set @query="쓰레드 풀링";
select sys.ML_EMBED_ROW(@query, JSON_OBJECT("model_id", "cohere.embed-multilingual-v3.0")) into @query_embedding;

SELECT question, answer, 
       round(1-DISTANCE(question_vector, @query_embedding, 'COSINE'),2) as score
FROM customer_qa
ORDER BY score DESC
LIMIT 3;


set @query="쓰레드 풀링";

SET @options = JSON_OBJECT('vector_store', JSON_ARRAY('askme.customer_qa'), 'vector_store_columns', JSON_OBJECT('segment', 'question','segment_embedding','question_vector', 'document_id', 'id'), 'embed_model_id', 'cohere.embed-multilingual-v3.0','model_options',JSON_OBJECT('language', 'ko'),'skip_generate', true );

CALL sys.ML_RAG(@query, @output, @options);
