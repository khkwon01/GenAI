create table customer_qa (
    id int not null auto_increment,
    question text,
    question_vector vector(1024) comment 'GENAI_OPTION=EMBED_MODEL_ID=cohere.embed-multilingual-v3.0',
    answer text,
    primary key(id)
) engine=innodb default charset=utf8mb4 collate=utf8mb4_bin;
