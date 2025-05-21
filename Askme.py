import streamlit as st
import os, yaml
from dataclasses import dataclass
from datetime import datetime
from utils.util import setup_logging
from constants import (DEFAULT_LLM_MODEL, ANSWER_SUMMARY_PROMPT,
                       DEFAULT_ASKME_SCHEMA_NAME, DEFAULT_ASKME_TABLE_NAME,
                       FIND_DOC_MAX_CHUNK_TOPK, RETRIEVAL_NUM_CHUNKS_BEFORE,
                       RETRIEVAL_NUM_CHUNK_AFTER,ANSWER_SUMMARY_MIN_SIMILARITY_SCORE,
                       SEARCH_MAX_CHUNK_TOPK)
from utils.mysqllib import (mysql_connect, run_mysql_queries)
from utils.genailib import (get_llm_list, askme_query_search)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

logger = setup_logging()

@dataclass
class mysql:
    host: str
    port: int
    username: str
    password: str
    timeout: int

def st_handle_backend_exception_banner(return_value = None):
    def decorator(func):
        def wrapper_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BackendConnectionException:
                st.warning("Askme 서비스 통신 오류, 다시 접근 하세요")
            except AskMEException:
                st.warning("Askme 서비스 에러, 어플리케이션 담당자에게 연락하세요")
            except (Exception):
                st.warning("Askme 서비스 에러, 어플리케이션 담당자에게 연락하세요")
                logger.exception("Askme 서비스 에러, 어플리케이션 담당자에게 연락하세요")
            return return_value
        return wrapper_func
    return decorator

#@st.cache_resource
def get_connection(v_coninfo,schema_name = DEFAULT_ASKME_SCHEMA_NAME):
    o_conn = mysql_connect(
            database = schema_name,
            username = v_coninfo.username,
            password = v_coninfo.password,
            host = v_coninfo.host,
            port = str(v_coninfo.port),
            connection_timeout = v_coninfo.timeout,
            repeat=3
    )

    return o_conn

if __name__ == "__main__":
    logger.info(f"started askme")
    o_config = None

    with open("config.yml", "r") as file:
      o_config = yaml.load(file, Loader=yaml.FullLoader)

    o_db = mysql (
            host = o_config["mysql"]["host"],
            port = o_config["mysql"]["port"],
            username = o_config["mysql"]["username"],
            password = o_config["mysql"]["password"],
            timeout = o_config["mysql"]["timeout"] )

    o_conn = get_connection(o_db)

    with open("styles/style.css") as f:
      styles = f.read()
    st.markdown(f"<style>{styles}</style>", unsafe_allow_html=True)

    st.markdown("<div style='text-align:left'><span style='color:black; font-size:32px; font-weight:bold'>HeatWave 서비스 Q&A</span></div>", unsafe_allow_html=True)
    st.write()

    with st.sidebar:
        st.image("assets/hw.png", width=500)
        st.write()

    o_llms = get_llm_list(o_conn)

    if "askme_selected_llm_model" not in st.session_state:
        st.session_state.askme_selected_llm_model = DEFAULT_LLM_MODEL if DEFAULT_LLM_MODEL in o_llms else o_llms[2]

    with st.form(f"Heatwave 관련 궁금증 문의", clear_on_submit=False, border=False):
        prompt = st.text_area("질문 사항 입력:", key="askme_question", height=150)
        submit_button = st.form_submit_button("검색")

    o_conn = get_connection(o_db)

    if submit_button:
        if prompt.strip():
            askme_query_search(o_conn, prompt, DEFAULT_ASKME_SCHEMA_NAME, 
                    DEFAULT_ASKME_TABLE_NAME, SEARCH_MAX_CHUNK_TOPK,
                    RETRIEVAL_NUM_CHUNKS_BEFORE, RETRIEVAL_NUM_CHUNK_AFTER,
                    ANSWER_SUMMARY_MIN_SIMILARITY_SCORE)
        else:
            st.warning("질문 사항을 입력 하시기 바랍니다.")

    with st.sidebar:
        st.empty()
        st.header("기본 정보 설명")
        st.write("---")

        st.write(f"데이터베이스 : {DEFAULT_ASKME_SCHEMA_NAME}")
        st.write(f"테이블 : {DEFAULT_ASKME_TABLE_NAME}")
        st.write(f"모델 : {DEFAULT_LLM_MODEL}")



    if o_conn.is_connected(): o_conn.disconnect()
