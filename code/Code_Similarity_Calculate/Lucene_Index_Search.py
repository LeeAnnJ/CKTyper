import os
import time
import jpype
import logging

import utils

# rertieve posts form SO dataset by lucene index
def lucene_search_pipline(fs_config, datasets, libs, lucene_top_k, not_finished):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    lucene_folder = fs_config['LUCENE_FOLDER'].replace('topk',f'top{lucene_top_k}')
    if not os.path.exists(lucene_folder):
        os.makedirs(lucene_folder)
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    reflag = True if len(not_finished)>0 else False
    
    for dataset in datasets:
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if os.path.exists(time_record_file): time_record = utils.load_json(time_record_file)
        else: time_record = {}

        for lib in libs:
            if lib in time_record.keys(): time_lib = time_record[lib]
            else: time_lib = {}
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)

            for cs in code_snippets:
                start_time = time.time()
                cs_name = cs.replace('.java','')
                if reflag and cs_name not in not_finished: continue
                cs_folder = f'{lucene_folder}/{dataset}/{lib}/{cs_name}'
                if cs_name in time_lib.keys(): time_cs = time_lib[cs_name]
                else: time_cs = {}
                logger.info(f'search similar code snippets for {cs}...')
                cs_path = f'{input_folder_path}/{cs}'
                CodeIndexer.main(['-online',cs_path,f'{lucene_top_k}',cs_folder])
                end_time = time.time()
                time_cs["lucene_search"] = end_time - start_time
                time_lib[cs_name] = time_cs
            
            time_record[lib] = time_lib
        utils.write_json(time_record_file,time_record)
        logger.info(f'finish lucene search for {dataset}.')
    pass