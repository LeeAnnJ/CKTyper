import os
import time
import jpype
import logging

from pathlib import Path
from itertools import islice

import utils
from Online.obj import SimilarityCalculator


# rertieve posts form SO dataset by lucene index
def lucene_search_pipline(fs_config, datasets, libs, lucene_top_n, not_finished):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    lucene_folder = fs_config['LUCENE_FOLDER'].replace('topk', f'top{lucene_top_n}')
    if not os.path.exists(lucene_folder):
        os.makedirs(lucene_folder)
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    reflag = True if len(not_finished) > 0 else False

    for dataset in datasets:
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if os.path.exists(time_record_file):
            time_record = utils.load_json(time_record_file)
        else:
            time_record = {}

        for lib in libs:
            if lib in time_record.keys():
                time_lib = time_record[lib]
            else:
                time_lib = {}
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)

            for cs in code_snippets:
                start_time = time.time()
                cs_name = cs.replace('.java', '')
                if reflag and cs_name not in not_finished: continue
                cs_folder = f'{lucene_folder}/{dataset}/{lib}/{cs_name}'
                if cs_name in time_lib.keys():
                    time_cs = time_lib[cs_name]
                else:
                    time_cs = {}
                logger.info(f'search similar code snippets for {cs}...')
                cs_path = f'{input_folder_path}/{cs}'
                CodeIndexer.main(['-online', cs_path, f'{lucene_top_n}', cs_folder])
                end_time = time.time()
                time_cs["lucene_search"] = end_time - start_time
                time_lib[cs_name] = time_cs

            time_record[lib] = time_lib
        utils.write_json(time_record_file, time_record)
        logger.info(f'finish lucene search for {dataset}.')
    pass


# lucene_topk_dic: the folder path of lucene top-k code snippets
# output: a list of top-k similar postIds & similarity, e.g. ['122','123'],[1.0,0.9,0.9]
def cal_similarity_singal(code_snippet:str, lucene_topk_dic, calculator:SimilarityCalculator, sim_topk):
    # 6. Calculate CrystalBLEU for input code and each lucene code
    # start_time = time.process_time()
    lucene_topk_paths = Path(lucene_topk_dic).iterdir()
    file_score_dict = calculator.cal_crystalBLEU_similarity(code_snippet, lucene_topk_paths)
    # end_time = time.process_time()
    # print ('Calculate CrystalBLEU time:',end_time - start_time)

    # 7. Sort the file_score_dict by value, and print the postid of the top-k similar code snippet
    sorted_file_score_dict = sorted(file_score_dict.items(), key=lambda x: x[1], reverse=True)
    topk_sim_files = [item[0] for item in list(islice(sorted_file_score_dict, sim_topk))]
    sim_score = [item[1] for item in list(islice(sorted_file_score_dict, sim_topk))]
    topk_sim_postIds = [file.stem.split('_')[0] for file in topk_sim_files]
    
    # most_similar_code_snippet_path = sorted_file_score_dict[0][0]
    # most_similar_CrystalBLEU_score = sorted_file_score_dict[0][1]
    # most_similar_postId = sorted_file_score_dict[0][0].stem.split('_')[1]
    # print(f"==>> The most similar code snippet is: {most_similar_code_snippet_path}") # the file format of the path is {codeId}_{postId}_{normalized_Lucene_score}.java
    # print(f"==>> The most similar code snippet's CrystalBLEU score is: {most_similar_CrystalBLEU_score}")
    # print(f"==>> The most similar code snippet's postId is: {most_similar_postId}")

    return topk_sim_postIds, sim_score


# output: a list of top-k similar postIds & similarity, e.g. ['122','123'],[1.0,0.9,0.9]
def select_topn_cs(lucene_topk_dic, sim_topk):
    lucene_list = os.listdir(lucene_topk_dic)
    lucene_score_list = [item.split('_') for item in lucene_list]
    lucene_score_list = [[item[0], float(item[1].replace(".java",""))] for item in lucene_score_list]
    sorted_list = sorted(lucene_score_list, key=lambda x:x[1], reverse=True)
    topk_sim_postIds = [item[0] for item in sorted_list[0:sim_topk]]
    sim_score = [item[1] for item in sorted_list[0:sim_topk]]
    return topk_sim_postIds, sim_score


# sim_result:
# {
#   "<lib>": {
#     "<cs_name>": {
#       "topk_sim_postIds": ["xxx","xxx","xxx"],
#       "sim_scores": [0.9,0.8,0.7]
#     },
#     "<cs_name>": {...}
#   },
#   "<lib>": {...}
# }
def cal_similarity_pipeline(fs_config, datasets, libs, retrieval_conf, not_finished):
    logger = logging.getLogger(__name__)
    lucene_topn = retrieval_conf["lucene_top_n"]
    calculate_CrystalBLEU = retrieval_conf["calculate_CrystalBLEU"]
    similarity_topn = retrieval_conf["similarity_top_n"]

    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    sim_cs_score_folder = fs_config['SIM_CS_SCORE_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    lucene_folder = fs_config['LUCENE_FOLDER'].replace('topk',f'top{lucene_topn}')
    ngram_file = fs_config['NGRAM_FILE']
    if not os.path.exists(sim_cs_score_folder): os.makedirs(sim_cs_score_folder)
    similarity_calculator = SimilarityCalculator(ngram_file)
    reflag = True if len(not_finished)>0 else False

    # Load input code snippet
    for dataset in datasets:
        result_file_str = f'{sim_cs_score_folder}/sim_res_{dataset}.json'
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if reflag: sim_result = utils.load_json(result_file_str)
        else: sim_result = {}
        if os.path.exists(time_record_file): time_record = utils.load_json(time_record_file)
        else: time_record = {}

        for lib in libs:
            if reflag: code_snippets_result = sim_result[lib]
            else: code_snippets_result = {}
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)
            if lib in time_record.keys(): time_lib = time_record[lib]
            else: time_lib = {}

            for cs in code_snippets:
                start_time = time.time()
                cs_name = cs.replace('.java','')
                if reflag and cs_name not in not_finished: continue
                if cs_name in time_lib.keys(): time_cs = time_lib[cs_name]
                else: time_cs = {}
                input_code_snippet_path = f'{input_folder_path}/{cs}'
                logger.info(f"calculate similarity for: {input_code_snippet_path}")
                # Get Lucene top-k code snippets
                lucene_topk_dic = f'{lucene_folder}/{dataset}/{lib}/{cs_name}'
                # logger.debug(f" lucene_topk_dir: {lucene_topk_dic}")
                
                #  Calculate CrystalBLEU for input code and each lucene code
                if calculate_CrystalBLEU:
                    input_code_snippet = utils.load_text(input_code_snippet_path)
                    topk_sim_postIds, sim_score = cal_similarity_singal(input_code_snippet,lucene_topk_dic,similarity_calculator,similarity_topn)
                else:
                    topk_sim_postIds, sim_score = select_topn_cs(lucene_topk_dic, similarity_topn)
                code_snippets_result[cs_name] = {"topk_sim_postIds": topk_sim_postIds, "sim_scores": sim_score}
                end_time = time.time()
                time_cs["sim_cal"] = end_time - start_time
                time_lib[cs_name] = time_cs

            sim_result[lib] = code_snippets_result
            time_record[lib] = time_lib
        # Save the result to file
        utils.write_json(result_file_str,sim_result)
        utils.write_json(time_record_file,time_record)
        logger.info(f'Finish code similarity calculation for dataset {dataset}, save result to file:{result_file_str}')
    return


def get_sim_posts_singal(cs_path, code_snippet, lucene_top_k, sim_top_k, res_folder):
    logger = logging.getLogger(__name__)
    PostIndexer = jpype.JClass("LucenePostIndexer")
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    calculator = SimilarityCalculator()
    lucene_posts_dic = f'{res_folder}/Lucene_top{lucene_top_k}'
    sim_post_folder = f'{res_folder}/searched_posts/'

    # search similar snippets by lucene index
    logger.info(f'search similar code snippets...')
    CodeIndexer.main(['-online', cs_path, f'{lucene_top_k}', lucene_posts_dic])
    # calculate similarity, get corresponding post ids
    logger.info(f'calculate code similarity...')
    sim_posts_ids, sim_score = cal_similarity_singal(code_snippet, lucene_posts_dic, calculator, sim_top_k)
    # retrieve posts from SO posts dataset
    logger.info(f'retrieve posts from SO...')
    for post_id in sim_posts_ids:
        PostIndexer.main(['-online', post_id, sim_post_folder])
    return sim_post_folder, sim_posts_ids, sim_score


if __name__ == '__main__':
    # 4. Load input code snippet
    datasets = []
    libs = []
    lucene_topk = 10
    similarity_topk = 3
    # cal_similarity_pipeline(datasets,libs,lucene_topk,similarity_topk)
    pass

