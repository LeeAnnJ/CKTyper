DATASETS = ["StatType-SO","Short-SO"]  # ["StatType-SO","Short-SO"]
LIBS = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"] # ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
INDEX_CONF = {
    "split_QA": False,
    "split_code": False,
}
RETRIEVAL_CONF = {
    "lucene_top_n": 50,
    "calculate_CrystalBLEU": False,
    "similarity_top_n": 10
}
RECOMMEND_TOP_K = 3
PROMPT_CONF = {
    "summarize": True,  # summarize text
    "text_filter_level": 3  # 0-Full, 1-CS, 2-Desc or 3-APISens
}
NOT_FINISHED = []
