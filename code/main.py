import sys
import time
import jpype
import logging
import argparse
import configparser

import utils
import config.task_setting as TS
import Code_Similarity_Calculate.Calculate_Code_Similarity as SimCal
import Code_Similarity_Calculate.Lucene_Index_Search as CodeSearch
import Get_TypeInference_Result.pipeline as GetResPip
import Get_TypeInference_Result.singal as GetResSin
from Evaluation_Result import precision_recall as CalPR


def set_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help='offline, online, preparation or evaluation')
    # online mode
    parser.add_argument('--pattern', type=str, help='singal or pipeline')
    parser.add_argument('--original', action='store_true', help='original or prompted')
    parser.add_argument('--source_path', type=str, help='code snippet path')
    return parser


def read_file_structure():
    fs_config = {}
    config = configparser.ConfigParser()
    config.read('./config/file_structure.ini')
    fs_config['EXP_PATH'] = config['resource']['EXP_PATH']
    fs_config['POST_DUMP_DIC'] = config['resource']['POST_DUMP_DIC']
    fs_config['SO_CODE_FOLDER'] = config['resource']['SO_CODE_FOLDER']
    fs_config['CODE_LUCENE_INDEX'] = config['resource']['CODE_LUCENE_INDEX']
    fs_config['POST_LUCENE_INDEX'] = config['resource']['POST_LUCENE_INDEX']
    fs_config['DATASET_CODE_FOLDER'] = config['resource']['DATASET_CODE_FOLDER']
    fs_config['API_ELEMENTS_FOLDER'] = config['resource']['API_ELEMENTS_FOLDER']
    fs_config['SEARCHED_POST_FOLDER'] = config['intermediate']['SEARCHED_POST_FOLDER']
    fs_config['NGRAM_FILE'] = config['intermediate']['NGRAM_FILE']
    fs_config['SIM_POST_RESULT_FOLDER'] = config['intermediate']['SIM_POST_RESULT_FOLDER']
    fs_config['GENERATED_QUESTOIN_FOLDER'] = config['intermediate']['GENERATED_QUESTOIN_FOLDER']
    fs_config['EVAL_PATH'] = config['result']['EVAL_PATH']
    fs_config['RESULT_ORIGINAL_FOLDER'] = config['result']['RESULT_ORIGINAL_FOLDER']
    fs_config['RESULT_PROMPTED_FOLDER'] = config['result']['RESULT_PROMPTED_FOLDER']
    fs_config['RESULT_SINGAL'] = config['result']['RESULT_SINGAL']
    return fs_config


# preparation:
# . dump SO posts
# . preprocess SO posts with 'java' tag
# . extract code snippets from posts

# offline mode:
# . build lucene index (post+code)
# . biud n-gram for SO code snippets

# online mode:
# 1. load given code snippet
# 2. search similar snippets, get corresponding post ids
#   2.1 by lucene index similarity
#   2.2 calculate code similarity
# 3. retrieve posts from SO posts dataset
# 4. process posts' body & summarize
# 5. generate question for given post
#  5.1 load code snippet
#  5.2 load api elements
# 6. call chatgpt, get results
# 7. save results in a csv file

# evaluation:
# . calculate precision for each code snippet, each lib and each dataset

def online_operation_pipline(fs_config, original):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    lucene_top_k = TS.LUCENE_TOP_K
    sim_top_k = TS.SIMILARITY_TOP_K
    text_level = TS.TEXT_FILTER_LEVEL
    prompt_conf = TS.PROMPT_CONF
    finished = TS.FINISHED
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    
    # 1 & 2
    logger.info('Start to search similar code snippets...')
    CodeSearch.lucene_search_pipline(fs_config, datasets, libs, lucene_top_k)
    # SimCal.cal_similarity_pipeline(fs_config, datasets, libs, lucene_top_k, sim_top_k)
    # # 3 
    # logger.info('Start to retrieve posts from SO...')
    # GetResPip.retrieve_posts_pipeline(fs_config, datasets, libs)
    # # 4 ~ 5
    # logger.info('Start to generate questions...')
    # GetResPip.generate_question_pipeline(fs_config, datasets, libs, original, sim_top_k, prompt_conf, text_level)
    # # 6 ~ 7
    # logger.info('Start to get type infrence result...')
    # GetResPip.get_result_pipline(fs_config, datasets, libs, finished, original)

    logger.info('Finish online pipline operation!')
    jpype.shutdownJVM()
    pass


# online mode for a single code snippet
# source_path: the json file contains the code snippet and api elments
def online_mode_singal(fs_config, source_path, original:bool=False):
    logger = logging.getLogger(__name__)
    lucene_top_k = TS.LUCENE_TOP_K
    sim_top_k = TS.SIMILARITY_TOP_K
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")

    logger.info(f'Processing code snippet: {source_path}')
    # 1. load given code snippet
    cs_name = source_path.split('/')[-1].replace('.java','')
    source_data = utils.load_json(source_path)
    code_snippet = source_data['code']
    api_elements = source_data['api_elements']
    result_singal = fs_config['RESULT_SINGAL']
    res_folder = f'{result_singal}/{cs_name}'
    res_data = {
        'code_path': source_path,
        'api_elements': api_elements,
        'original': original
    }

    if original:
        # 5. generate question for given post
        question = GetResSin.generate_question_pipeline(code_snippet, api_elements, original)
    else:
        text_level = TS.TEXT_FILTER_LEVEL
        prompt_conf = TS.PROMPT_CONF
        res_data['prompt_conf'] = prompt_conf
        res_data['prompt_conf']['text_level'] = text_level
        sim_post_folder,sim_posts_ids,sim_score = GetResSin.get_sim_posts_singal(source_path, code_snippet, lucene_top_k, sim_top_k, res_folder)
        # 4. process posts' body & summarize
        logger.info(f'process posts and summarize...')
        post_list = [f'{sim_post_folder}/{id}.json' for id in sim_posts_ids]
        res_data['sim_code_info'] = {
            'post_id': sim_posts_ids,
            'sim_score': sim_score,
        }
        # 5. generate question for given post
        question = GetResSin.generate_question_pipeline(code_snippet, api_elements, original, post_list, prompt_conf, text_level)

    res_data['question'] = question
    logger.info('Start to get type infrence result...')
    infere_result = GetResSin.get_result_singal(question,api_elements)
    res_data['inference_result'] = infere_result
    res_file = f'{res_folder}/result.json'
    logger.info(f'save result to:{res_file}')
    utils.write_json(res_file,res_data)
    jpype.shutdownJVM()
    logger.info('Finish online operation for singal code snippet!')
    pass


def evaluation_operation(original:bool):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    logger.info('Start to calculate precision and recall...')
    CalPR.cal_precision_recall_pipline(datasets, libs, original)
    pass


# e.p. python main.py --mode online --pattern singal --original
if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    parser = set_arg_parser()
    args = parser.parse_args()
    fs_config = read_file_structure()

    mode = args.mode
    if mode == 'offline':
        pass
    elif mode == 'online':
        pattern = args.pattern
        if pattern == 'singal':
            print("start online mode, pattern: singal...")
            start_time = time.process_time()
            online_mode_singal(fs_config, args.source_path, args.original)
            end_time = time.process_time()
            print ('Online singal processing time:', end_time - start_time)
            pass
        elif pattern == 'pipeline':
            print("start online mode, pattern: pipeline...")
            start_time = time.process_time()
            online_operation_pipline(fs_config, args.original)
            end_time = time.process_time()
            print ('Online pipeline processing time:', end_time - start_time)
            pass
        else:
            print('Invalid online_pattern: {}'.format(pattern))
            sys.exit(1)
        pass
    elif mode == 'evaluation':
        print("start evaluation mode...")
        start_time = time.process_time()
        evaluation_operation(args.original)
        end_time = time.process_time()
        print ('Evaluation pipeline processing time:', end_time - start_time)
        pass
    else:
        print('Invalid mode: {}'.format(mode))
        sys.exit(1)