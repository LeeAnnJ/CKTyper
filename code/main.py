import os
import sys
import time
import jpype
import logging
import argparse
import datetime

import utils
from Offline_Processing import ParseSO, ParseLib, extract_code_from_post
from Online_Processing import SearchCode, GenQues, GetResPipe, GetResSig
from config import task_setting as TS, fs_config, so_pro_conf
from Evaluation_Result import CalPR, CheckAnswer, StatSig, ProTime


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
    parser.add_argument('--original', action='store_true', help='original or prompted')
    parser.add_argument('--source_path', type=str, help='code snippet path')
    # evaluation mode
    parser.add_argument('--operation',type=str, default='precision', help='evaluation operation:precision,check_wrong,stat_sig,process_time')
    return parser


# offline mode:
# 1. dump SO posts & preprocess SO posts with 'java' tag
# 2. extract code snippets from posts
# 3. build lucene index (post+code)
# 4. extract fqn from library
# 5. extract ngrams' frequencies from SO code

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

# evaluation:
# . calculate precision for each code snippet, each lib and each dataset

def offline_operation(fs_config):
    logger = logging.getLogger(__name__)
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")

    # # 1. extract SO posts with 'java' tag from SO data
    # logger.info("Start to filter SO posts with \"java\" tag ...")
    # start_time = time.time()
    # logger.info('get questions and their ids ======')
    # ParseSO.getQuestions(so_pro_conf)
    # logger.info('\n\nget answers and their ids ======')
    # ParseSO.getAnswers(so_pro_conf)
    # end_time = time.time()
    # logger.info(f"Running time for filter SO posts with \"java\" tag: {end_time - start_time}")

    # # 2 extract code snippets from posts
    # logger.info('Start to extract code snippets from SO posts...')
    # start_time = time.time()
    # extract_code_from_post(fs_config)
    # end_time = time.time()
    # logger.info(f'Running time for extract codes: {end_time - start_time}')
    
    # 3. biuld lucene index
    logger.info('Start to build lucene index...')
    start_time = time.time()
    index_conf = TS.INDEX_CONF
    split_QA = "True" if index_conf["split_QA"] else "False"
    split_code = "True" if index_conf["split_code"] else "False"
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    CodeIndexer.main(['-offline', split_QA, split_code])
    # PostIndexer = jpype.JClass("LucenePostIndexer")
    # PostIndexer.main(['-offline', split_QA])
    end_time = time.time()
    logger.info(f'Running time for build lucene index: {end_time - start_time}')

    # # 4. extract fqn from library
    # logger.info('Start to extract FQN from API library...')
    # start_time = time.time()
    # ParseLib.extract_fqn(fs_config)
    # # PreNgram.similarity_preprocess(fs_config)
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
def online_operation_pipline(fs_config, original):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    lcn_k = TS.LUCENE_TOP_K
    sim_k = TS.SIMILARITY_TOP_K
    rcm_k = TS.RECOMMEND_TOP_K
    prompt_conf = TS.PROMPT_CONF
    not_finished = TS.NOT_FINISHED

    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    if not os.path.exists(time_record_folder):
        os.makedirs(time_record_folder)

    # 1
    start_time = time.process_time()
    logger.info('Start to search similar code snippets...')
    SearchCode.lucene_search_pipline(fs_config, datasets, libs, lcn_k, not_finished)
    SearchCode.cal_similarity_pipeline(fs_config, datasets, libs, lcn_k, sim_k, not_finished)
    end_time = time.process_time()
    logger.info(f'time spent for searching similar code snippets: {end_time-start_time}')

    # 2
    logger.info('Start to retrieve posts from SO...')
    start_time = time.process_time()
    GenQues.retrieve_posts_pipeline(fs_config, datasets, libs, not_finished)
    end_time = time.process_time()
    logger.info(f'time spent for retireve code snippets: {end_time-start_time}')
    logger.info('Start to generate questions...')
    start_time = time.process_time()
    GenQues.generate_question_pipeline(fs_config, datasets, libs, not_finished, original, sim_k, prompt_conf)
    end_time = time.process_time()
    logger.info(f'time spent for generating questions: {end_time-start_time}')

    # 3
    logger.info('Start to get type infrence result...')
    start_time = time.time()
    GetResPipe.get_result_pipline(fs_config, datasets, libs, not_finished, original, rcm_k)
    end_time = time.time()
    logger.info(f'time spent for getting type infrence result: {end_time-start_time}')

    jpype.shutdownJVM()
    logger.info('Finish online pipline operation!')
    return


# online mode for a single code snippet
# source_path: the json file contains the code snippet and api elments
def online_operation_singal(fs_config, source_path, original:bool=False):
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
        question = GenQues.generate_question_signal(code_snippet, api_elements, original)
    else:
        prompt_conf = TS.PROMPT_CONF
        res_data['prompt_conf'] = prompt_conf
        sim_post_folder, sim_posts_ids, sim_score = SearchCode.get_sim_posts_singal(source_path, code_snippet, lucene_top_k, sim_top_k, res_folder)
        # 4. process posts' body & summarize
        logger.info(f'process posts and summarize...')
        post_list = [f'{sim_post_folder}/{id}.json' for id in sim_posts_ids]
        res_data['sim_code_info'] = {
            'post_id': sim_posts_ids,
            'sim_score': sim_score,
        }
        # 5. generate question for given post
        question = GenQues.generate_question_signal(code_snippet, api_elements, original, post_list, prompt_conf)

    res_data['question'] = question
    logger.info('Start to get type infrence result...')
    infere_result = GetResSig.get_result_singal(question, api_elements)
    res_data['inference_result'] = infere_result
    res_file = f'{res_folder}/result.json'
    logger.info(f'save result to:{res_file}')
    utils.write_json(res_file,res_data)
    jpype.shutdownJVM()
    logger.info('Finish online operation for singal code snippet!')
    return


# operation: precision, check_wrong, stat_sig, process_time
def evaluation_operation(fs_config, operation, original: bool):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    not_finished = []
    ops = operation.split('+')
    
    # calculate precision and recall
    if 'precision' in ops:
        logger.info('Start to calculate precision and recall...')
        CalPR.cal_precision_recall_pipline(fs_config, datasets, libs, original)

    # list wrong answer & not perfect file
    if 'check_wrong' in ops:
        CheckAnswer.list_wrong_answer_pipline(fs_config, datasets, libs, original)
        not_finished = CheckAnswer.list_not_perfect_file(fs_config, datasets)

    # calculate statistical significance
    if 'stat_sig' in ops:
        logger.info('Start to calculate statistical significance...')
        StatSig.cal_statistical_significance(fs_config)

    # calculate average process time
    if 'process_time' in ops:
        logger.info('Start to calculate average process time...')
        ProTime.cal_average_process_time(fs_config)

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
            online_operation_singal(fs_config, args.source_path, args.original)
            end_time = time.process_time()
            print ('Online singal processing time:', end_time - start_time)
        elif pattern == 'pipeline':
            print("start online mode, pattern: pipeline...")
            online_operation_pipline(fs_config, args.original)
        else:
            print('Invalid online_pattern: {}'.format(pattern))
            sys.exit(1)
    elif mode == 'evaluation':
        # print("start evaluation mode...")
        start_time = time.time()
        evaluation_operation(fs_config, args.operation, args.original)
        end_time = time.time()
        print ('Evaluation processing time:', end_time - start_time)
    else:
        print('Invalid mode: {}'.format(mode))
        sys.exit(1)
