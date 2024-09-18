DATASETS = ["StatType-SO","Short-SO"]  # ["StatType-SO","Short-SO"]
LIBS = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"] # ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
INDEX_CONF = {
    "split_QA": False,
    "split_code": True,
}
RETRIEVAL_CONF = {
    "lucene_top_n": 50,
    "calculate_CrystalBLEU": True,
    "similarity_top_n": 10
}
RECOMMEND_TOP_K = 3
PROMPT_CONF = {
    "add_context": True,
    "data_for_context": 3,  # 0-Full, 1-CS, 2-Desc or 3-APISens
    "summarize": True,  # summarize text
}
NOT_FINISHED = []
