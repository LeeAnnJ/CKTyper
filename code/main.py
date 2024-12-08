import os
import sys
import time
import jpype
import logging
import argparse
import datetime

from config import CKTyper_setting as TS
from Offline import SO_parser, BuildIndex, ParseLib, extract_code_from_post
from Online import RetrieveCode, GenCKC, TypeInfer
from config import fs_config, so_pro_conf
from Evaluation import CalPR, StatSign, ExecTime
from Evaluation import CheckAnswer


log_level = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL
}

def set_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--log_level', type=str, default='info', help='log level: info, debug, warning, error, critical')
    parser.add_argument('--log_file', action='store_true', help='store log file or not')
    parser.add_argument('--mode', type=str, help='offline, online, preparation or evaluation')
    # online mode
    parser.add_argument('--pattern', type=str, help='singal or pipeline')
    parser.add_argument('--source_path', type=str, help='code snippet path')
    # evaluation mode
    parser.add_argument('--operation',type=str, default='precision', help='evaluation operation: precision, check_wrong, stat_sig, process_time')
    return parser


# offline mode:
# 1. dump SO posts & preprocess SO posts with 'java' tag
# 2. extract code snippets from posts & build lucene index
# 3. extract fqn from library
# 4. extract ngrams' frequencies from SO code for code similarity calculation

# online mode:
# 1. search similar snippets, get corresponding post ids
#   1.1 by lucene index similarity
#   1.2 calculate code similarity
# 2. generate context for similar code snippets
#   2.1 retrieve posts from SO posts dataset
#   2.2 process posts' body & summarize
# 3. generate question & get results from chatgpt
#   3.1 generate question for given post
#   3.2 call chatgpt, get results
# 4. save results in a csv file

# evaluation mode:
# calculate precision for each code snippet, each lib and each dataset.
# calculate average process time for each code snippet, each lib and each dataset.

def offline_operation(fs_config):
    logger = logging.getLogger(__name__)
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./Java/LuceneIndexer/LuceneIndexer.jar")

    # 1. extract SO posts with 'java' tag from SO data
    # todo: add "language" parameter to filter SO posts with specific language
    logger.info("Start to filter SO posts ...")
    start_time = time.time()
    logger.info('get questions and their ids ======')
    SO_parser.getQuestions(so_pro_conf)
    logger.info('\n\nget answers and their ids ======')
    SO_parser.getAnswers(so_pro_conf)
    end_time = time.time()
    logger.info(f"Running time for filter SO posts: {end_time - start_time}")

    # 2. extract code snippets from posts
    logger.info('Start to extract code snippets from SO posts...')
    start_time = time.time()
    extract_code_from_post(fs_config)
    end_time = time.time()
    logger.info(f'Running time for extract codes: {end_time - start_time}')
    
    # 3. build lucene index
    logger.info('Start to build lucene index...')
    start_time = time.time()
    index_conf = TS.INDEX_CONF
    BuildIndex.build_lucene_index(index_conf)
    end_time = time.time()
    logger.info(f'Running time for build lucene index: {end_time - start_time}')

    # # 4. extract fqn from API library
    # # This step can be skipped, the parsing result has been saved in ~/Data/FQN_in_library.pickle
    # # The API libraries included in the parsing results are visible from https://anonymous.4open.science/r/iJTyper-0A4D/Code/Baseline/SnR/src/test/resources/jars/
    # logger.info('Start to extract FQN from API library...')
    # start_time = time.time()
    # ParseLib.extract_fqn(fs_config)
    # end_time = time.time()
    # logger.info(f'Running time for creat FQN set: {end_time - start_time}')

    jpype.shutdownJVM()
    logger.info('Finish offline operation!')
    return


# time record:
# {
#     <lib>: {
#         <cs_name>: {
#             "lucene_search": 123,
#             "sim_cal": 123,
#             "retrieve_post": 123,
#             "generate_context": 123,
#             "type_inf": 123,
#         },
#         <cs_name>: {...},
#     }
#     <lib>: {...},
# }
def online_operation_pipline(fs_config):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    retrieval_conf = TS.RETRIEVAL_CONF
    rcm_k = TS.RECOMMEND_TOP_K
    prompt_conf = TS.PROMPT_CONF
    not_finished = TS.NOT_FINISHED

    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./Java/LuceneIndexer/LuceneIndexer.jar")
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    if not os.path.exists(time_record_folder):
        os.makedirs(time_record_folder)

    # 1. Two-Phase Similar CS Retrieval
    start_time = time.process_time()
    logger.info('Start to search similar code snippets...')
    RetrieveCode.lucene_search_pipline(fs_config, datasets, libs, retrieval_conf["lucene_top_n"], not_finished)
    RetrieveCode.cal_similarity_pipeline(fs_config, datasets, libs, retrieval_conf, not_finished)
    end_time = time.process_time()
    logger.info(f'time spent for searching similar code snippets: {end_time-start_time}')

    # 2. Croudsourcing Knowledge Context (CKC) Generation
    logger.info('Start to retrieve posts from SO...')
    start_time = time.process_time()
    GenCKC.get_post_from_CKB_pipeline(fs_config, datasets, libs, not_finished)
    end_time = time.process_time()
    logger.info(f'time spent for retireve posts: {end_time-start_time}')
    logger.info('Start to generate questions...')
    start_time = time.process_time()
    GenCKC.generate_CKcontext_pipeline(fs_config, datasets, libs, not_finished, retrieval_conf["similarity_top_n"], prompt_conf)
    end_time = time.process_time()
    logger.info(f'time spent for generating questions: {end_time-start_time}')

    # 3. Type Inference Using A LLM
    logger.info('Start to get type infrence result...')
    start_time = time.time()
    TypeInfer.LLM_type_inference_pipline(fs_config, datasets, libs, not_finished, rcm_k)
    end_time = time.time()
    logger.info(f'time spent for getting type infrence result: {end_time-start_time}')

    jpype.shutdownJVM()
    logger.info('Finish online pipline operation!')
    return


# # online mode for a single code snippet
# # source_path: the json file contains the code snippet and api elments
def online_operation_singal(fs_config, source_path):
    return


# operation: precision, check_wrong, stat_sig, process_time
def evaluation_operation(fs_config, operation):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    not_finished = []
    ops = operation.split('+')
    
    # calculate precision and recall
    if 'precision' in ops:
        logger.info('Start to calculate precision and recall...')
        CalPR.cal_precision_recall_pipline(fs_config, datasets, libs)

    # list wrong answer & not perfect file
    if 'check_wrong' in ops:
        CheckAnswer.list_wrong_answer_pipline(fs_config, datasets, libs)
        not_finished = CheckAnswer.list_not_perfect_file(fs_config, datasets)

    # calculate statistical significance
    if 'stat_sig' in ops:
        logger.info('Start to calculate statistical significance...')
        StatSign.cal_statistical_significance(fs_config)

    # calculate average process time
    if 'process_time' in ops:
        logger.info('Start to calculate average process time...')
        ExecTime.cal_average_process_time(fs_config)

    return not_finished


# e.p. python main.py --mode online --pattern singal --original
if __name__ == '__main__':
    parser = set_arg_parser()
    args = parser.parse_args()

    if args.log_file:
        now = datetime.datetime.now().strftime('%y%m%d%H%M')
        log_path = f"{fs_config['INTER_RECORD_FOLDER']}/logs/{now}.log"
        logging.basicConfig(filename=log_path, level=log_level[args.log_level], format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        logging.basicConfig(level=log_level[args.log_level], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    mode = args.mode
    if mode == 'offline':
        print("start offline mode...")
        offline_operation(fs_config)
        pass
    elif mode == 'online':
        pattern = args.pattern
        if pattern == 'singal':
            print("start online mode, pattern: singal...")
            start_time = time.process_time()
            online_operation_singal(fs_config, args.source_path)
            end_time = time.process_time()
            print ('Online singal processing time:', end_time - start_time)
        elif pattern == 'pipeline':
            print("start online mode, pattern: pipeline...")
            online_operation_pipline(fs_config)
        else:
            print('Invalid online_pattern: {}'.format(pattern))
            sys.exit(1)
    elif mode == 'evaluation':
        # print("start evaluation mode...")
        start_time = time.time()
        evaluation_operation(fs_config, args.operation)
        end_time = time.time()
        print ('Evaluation processing time:', end_time - start_time)
    else:
        print('Invalid mode: {}'.format(mode))
        sys.exit(1)
