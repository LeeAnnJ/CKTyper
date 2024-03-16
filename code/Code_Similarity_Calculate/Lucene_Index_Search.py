import os
import jpype
import logging

# rertieve posts form SO dataset by lucene index
def lucene_search_pipline(fs_config, datasets, libs, lucene_top_k, not_finished):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    eval_path = fs_config['EVAL_PATH']
    lucene_folder = f'{eval_path}/Lucene_top{lucene_top_k}'
    if not os.path.exists(lucene_folder):
        os.makedirs(lucene_folder)
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    reflag = False
    if len(not_finished)>0: reflag = True
    
    for dataset in datasets:
        for lib in libs:
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)
            for cs in code_snippets:
                cs_name = cs.replace('.java','')
                if reflag and cs_name not in not_finished: continue
                res_folder = f'{lucene_folder}/{dataset}/{lib}/{cs_name}'
                logger.info(f'search similar code snippets for {cs}...')
                cs_path = f'{input_folder_path}/{cs}'
                CodeIndexer.main(['-online',cs_path,f'{lucene_top_k}',res_folder])
    pass