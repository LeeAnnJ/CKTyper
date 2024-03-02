import sys
import time
import jpype
import logging
import argparse
import configparser

import config.task_setting as TS
import Code_Similarity_Calculate.Calculate_Code_Similarity as SimCal
import Code_Similarity_Calculate.Lucene_Index_Search as CodeSearch
import Get_TypeInference_Result.pipeline as GetResPip
from Evaluation_Result import precision_recall as CalPR
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def set_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str, help='offline, online, preparation or evaluation')
    # online mode
    parser.add_argument('--pattern', type=str, help='singal or pipeline')
    parser.add_argument('--sum', action='store_true', help='summarize the posts')
    parser.add_argument('--ans', action='store_true', help='with posts\'answer')
    parser.add_argument('--with_comments', action='store_true', help='with comments')
    parser.add_argument('--original', action='store_true', help='original or prompted')
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
# 2. search similar snippets by lucene index & similarity, get corresponding post ids
# 3. retrieve posts from SO posts dataset
# 4. process posts' body & summarize
# 5. generate question for given post
#  5.1 load code snippet
#  5.2 load api elements
# 6. call chatgpt, get results
# 7. save results in a csv file

# evaluation:
# . calculate precision for each code snippet, each lib and each dataset

def online_operation_pipline(fs_config, sum, ans, with_comments, original):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    lucene_top_k = TS.LUCENE_TOP_K
    sim_top_k = TS.SIMILARITY_TOP_K
    finished = TS.FINISHED
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    # # 1 & 2
    # # laptop processing time: 140.890625s
    # # todo: decrease the times of loading code snippets
    # logger.info('Start to search similar code snippets...')
    # CodeSearch.lucene_search_pipline(fs_config, datasets, libs, lucene_top_k)
    # sim_result_file = SimCal.cal_similarity_pipeline(fs_config, datasets, libs, lucene_top_k, sim_top_k)
    # # 3 
    # # laptop: 4481.0625s
    # logger.info('Start to retrieve posts from SO...')
    # GetResPip.retrieve_posts_pipeline(fs_config, sim_result_file)
    # # 4 ~ 5
    # # server: 1895.362702536s (StatType-SO) + 482.33577335499996s(Short-SO)
    # # original laptop: 26.609375(StatType-SO) + 12.21875(Short-SO)
    # logger.info('Start to generate questions...')
    # GetResPip.generate_question_pipeline(fs_config, datasets, libs, sum, ans, with_comments, original)
    # 6 ~ 7
    # laptop:  8.171875s(StatTypeSO) + 4.890625 s(ShortSO)
    logger.info('Start to get type infrence result...')
    GetResPip.get_result_pipline(fs_config, datasets, libs, finished, original)
    logger.info('Finish online operation pipline!')
    jpype.shutdownJVM()
    pass


def evaluation_operation(original:bool):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    logger.info('Start to calculate precision and recall...')
    CalPR.cal_precision_recall_pipline(datasets, libs, original)
    pass


# exp: python main.py --mode online --pattern singal --sum --ans --with_comments
if __name__ == '__main__':
    parser = set_arg_parser()
    args = parser.parse_args()
    fs_config = read_file_structure()
    mode = args.mode
    if mode == 'offline':
        pass
    elif mode == 'online':
        pattern = args.pattern
        if pattern == 'singal':
            pass
        elif pattern == 'pipeline':
            print("start online mode, pattern: pipeline...")
            start_time = time.process_time()
            online_operation_pipline(fs_config, args.sum, args.ans, args.with_comments, args.original)
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