# todo: add lucene index searching
import os
import jpype
import logging
import configparser

# todo: modify configuration reading
# rertieve posts form SO dataset by lucene index
def lucene_search_pipline(datasets,libs,lucene_top_k):
    config = configparser.ConfigParser()
    config.read('./config/file_structure.ini')
    dataset_code_folder = config['resource']['DATASET_CODE_FOLDER']
    eval_path = config['result']['EVAL_PATH']
    lucene_folder = f'{eval_path}/Lucene_top{lucene_top_k}'
    if not os.path.exists(lucene_folder):
        os.makedirs(lucene_folder)

    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    logger = logging.getLogger(__name__)

    for dataset in datasets:
        for lib in libs:
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)
            res_folder = f'{lucene_folder}/{dataset}/{lib}'
            if not os.path.exists(res_folder): os.makedirs(res_folder)
            for cs in code_snippets:
                logger.info(f'search similar code snippets for {cs}...')
                cs_path = f'{input_folder_path}/{cs}'
                res_path = f'{res_folder}/{cs.replace(".java","")}'
                CodeIndexer.main(['-online',cs_path,f'{lucene_top_k}',res_path])

    jpype.shutdownJVM()
    pass