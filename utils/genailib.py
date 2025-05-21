from contextlib import closing
import streamlit as st
import re
from utils.mysqllib import (mysql_connect, run_mysql_queries)
from constants import DEFAULT_LLM_MODEL

def get_llm_list(conn):
    with closing(conn):
        query = f"""
                SELECT model_name FROM sys.ML_SUPPORTED_LLMS WHERE model_type = 'generation';
            """
        llms = run_mysql_queries(query, conn)

    return llms

def askme_query_search(conn, prompt, db_name, table_name, topk, 
        num_chunks_before, num_chunks_after, min_similarity_score=0.0, 
        distance_metric='COSINE', embedding_model_id=DEFAULT_LLM_MODEL):

    empty_count = 0

    query = """CALL sys.ML_MODEL_LOAD(%s, NULL);"""
    params = (embedding_model_id,)
    run_mysql_queries(query, conn, params)

    query = f"""SELECT sys.ML_EMBED_ROW(%s, JSON_OBJECT('model_id', %s)) INTO @input_embedding;"""
    params = (prompt, embedding_model_id)
    data = run_mysql_queries(query, conn, params)

    query = "SET group_concat_max_len = 4096;"
    run_mysql_queries(query, conn)

    all_results = []
    pattern = r"^[A-Za-z0-9_]{1,64}$"
    if not re.match(pattern, db_name) or not re.match(pattern, table_name):
        logger.warning(f"Possible SQL Injection Attack {schema_name}.{table_name}")
        raise AskMEException("Invalid schema or table name")

    query = f"""
                select 
                    id,
                    (1 - DISTANCE(question_vector, @input_embedding, %s)) AS similarity_score,
                    question,
                    answer
                FROM `{db_name}`.`{table_name}`
                ORDER BY similarity_score DESC, id
                LIMIT %s
    """

    params = (
            distance_metric,
            topk
    )

    response = run_mysql_queries(query, conn, params)

    st.divider()

    for row in response:
       if row[1] >= 0.6:
           exactrate = round(row[1], 2)
           st.write(f'>> 관련 질문 : {row[2]} (정확도:{int(exactrate*100)}%)')
           st.write(f'>> 관련 답변 : {row[3]}')
           st.divider()
           empty_count += 1

    if empty_count < 1: 
       st.write('>> 관련 답변이 없습니다.')
       st.divider()

