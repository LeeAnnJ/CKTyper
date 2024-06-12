DATASETS = ["StatType-SO","Short-SO"]  # ["StatType-SO","Short-SO"]
LIBS = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"] # ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
INDEX_CONF = {
    "split_QA": False,
    "split_code": False,
}
LUCENE_TOP_K = 50
SIMILARITY_TOP_K = 10
RECOMMEND_TOP_K = 5
PROMPT_CONF = {
    "summarize": True,  # summarize text
    "text_filter_level": 2  # 0-ALL, 1-TEXT or 2-API
}
NOT_FINISHED = []
