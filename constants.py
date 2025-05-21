DEFAULT_ASKME_SCHEMA_NAME = "askme"
DEFAULT_ASKME_TABLE_NAME = "customer_qa"
DEFAULT_LLM_MODEL = "cohere.embed-multilingual-v3.0"

FIND_DOC_MAX_CHUNK_TOPK = 200
ANSWER_SUMMARY_MAX_CHUNK_TOPK = 5
SEARCH_MAX_CHUNK_TOPK = 3
RETRIEVAL_NUM_CHUNKS_BEFORE = 0
RETRIEVAL_NUM_CHUNK_AFTER = 1
ANSWER_SUMMARY_MIN_SIMILARITY_SCORE = 0.0

ANSWER_SUMMARY_PROMPT = """
    You are a data summarizer. I will provide you with a question and relevant context data. Your task is to summarize the parts of the context that are most relevant to answering the question.

    Context:
    {context}

    Question:
    {question}

    Please provide a concise summary based on the question.
"""


CLIENT_TIMEOUT = (10,240)
