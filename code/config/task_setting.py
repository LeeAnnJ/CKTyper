DATASETS = ["StatType-SO","Short-SO"]  # ["StatType-SO","Short-SO"]
LIBS = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"] # ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
INDEX_CONF = {
    "split_QA": False,
    "split_code": False,
}
LUCENE_TOP_K = 50
SIMILARITY_TOP_K = 10
RECOMMEND_TOP_K = 3
PROMPT_CONF = {
    "summarize": True,  # summarize text
    "text_filter_level": 3  # 0-Full, 1-CS, 2-Desc or 3-APISens
}
NOT_FINISHED = []
