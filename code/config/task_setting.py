DATASETS = ["StatType-SO","Short-SO"] # ["StatType-SO","Short-SO"]
LIBS = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"] # ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
LUCENE_TOP_K = 15
SIMILARITY_TOP_K = 5
TEXT_FILTER_LEVEL = 2 # 0-ALL, 1-TEXT or 2-API
PROMPT_CONF = {
    "summarize": True, # summarize text
    "with_ans": False, # with post's answer
    "with_comments": False # with comments
}
NOT_FINISHED = []