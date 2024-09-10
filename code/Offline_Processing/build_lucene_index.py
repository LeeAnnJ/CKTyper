import jpype

def build_lucene_index(index_conf):
    split_QA = "True" if index_conf["split_QA"] else "False"
    split_code = "True" if index_conf["split_code"] else "False"
    # build lucene index for code snipeet in croudsourcing knowledge base
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    CodeIndexer.main(['-offline', split_QA, split_code])
    # build lucene index for SO posts to facilitate extracting post content based on the postid
    PostIndexer = jpype.JClass("LucenePostIndexer")
    PostIndexer.main(['-offline', split_QA])
    return