import sys
import time
import jpype
import logging
import argparse

import config.task_setting as TS
import Code_Similarity_Calculate.Calculate_Code_Similarity as SimCal
import Code_Similarity_Calculate.Lucene_Index_Search as CodeSearch
import Get_TypeInference_Result.pipeline as GetResPip
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

def online_operation_pipline(sum, ans, with_comments, original):
    logger = logging.getLogger(__name__)
    datasets = TS.DATASETS
    libs = TS.LIBS
    lucene_top_k = TS.LUCENE_TOP_K
    sim_top_k = TS.SIMILARITY_TOP_K
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    # # 1 & 2
    # # laptop processing time: 140.890625s
    # # todo: decrease the times of loading code snippets
    # logger.info('Start to search similar code snippets...')
    # CodeSearch.lucene_search_pipline(datasets, libs, lucene_top_k)
    # sim_result_file = SimCal.cal_similarity_pipeline(datasets, libs, lucene_top_k, sim_top_k)
    # 3
    sim_result_file = '../Evaluation/Sim_post_results//sim_result_top_3.json'
    logger.info('Start to retrieve posts from SO...')
    GetResPip.retrieve_posts_pipeline(sim_result_file)
    # # 4 ~ 5
    # logger.info('Start to generate questions...')
    # GetResPip.generate_question_pipeline(datasets, libs, sum, ans, with_comments, original)
    # # 6 ~ 7
    # logger.info('Start to get type infrence result...')
    # GetResPip.get_result_pipline(datasets, original)
    # logger.info('Finish online operation pipline!')
    jpype.shutdownJVM()
    pass


# exp: python main.py --mode online --pattern singal --sum --ans --with_comments
if __name__ == '__main__':
    parser = set_arg_parser()
    args = parser.parse_args()
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
            online_operation_pipline(args.sum, args.ans, args.with_comments, args.original)
            end_time = time.process_time()
            print ('Online pipeline processing time:', end_time - start_time) # ?
            pass
        else:
            print('Invalid online_pattern: {}'.format(pattern))
            sys.exit(1)
        pass
    else:
        print('Invalid mode: {}'.format(mode))
        sys.exit(1)