import os
import sys
import time
import jpype
import logging
import configparser
from Get_TypeInference_Result.singal import combine_res_data, handle_remain_api
from Generate_Question.combine_prompt import PromptCombiner
from Generate_Question.generate_question import QuestionGenerator
from Get_TypeInference_Result.call_chatgpt import ModelAccesser_V2 as ModelAccesser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

# rertieve posts form SO dataset by lucene index
def retrieve_posts_pipeline(fs_config, datasets, libs):
    searched_post_folder = fs_config['SEARCHED_POST_FOLDER']
    sim_post_result_folder = fs_config['SIM_POST_RESULT_FOLDER']
    PostIndexer = jpype.JClass("LucenePostIndexer")

    for dataset in datasets:
        sim_res_file = f'{sim_post_result_folder}/sim_res_{dataset}.json'
        result_json = utils.load_json(sim_res_file)
        dataset_folder = f'{searched_post_folder}/{dataset}'
        for lib in libs:
        # for lib_res in result_json:
            lib_res = result_json[lib]
            lib_folder = f'{dataset_folder}/{lib}'
            cs_results = lib_res['code_snippets']
            code_snippets = cs_results.keys()
            for cs_name in code_snippets:
                cs_res = cs_results[cs_name]
                cs_folder = f'{lib_folder}/{cs_name}'
                topk_sim_postIds = cs_res['topk_sim_postIds']
                for id in topk_sim_postIds:
                    PostIndexer.main(['-online',id,cs_folder])
    pass


def get_result_pipline(fs_config, datasets, libs, finished, original:bool):
    logger = logging.getLogger(__name__)
    api_elements_folder = fs_config['API_ELEMENTS_FOLDER']
    generated_question_folder = fs_config['GENERATED_QUESTOIN_FOLDER']
    if original: res_folder = fs_config['RESULT_ORIGINAL_FOLDER']
    else: res_folder = fs_config['RESULT_PROMPTED_FOLDER']
    model_acs = ModelAccesser()
    res_head = ["Node","ChatGPT Answer","Truth"]
    oflag = 'original' if original else 'prompted'
    not_finished = []

    for dataset in datasets:
        api_file = f'{api_elements_folder}/API_elements_{dataset}.json'
        api_dict = utils.load_json(api_file)
        
        for lib in libs:
            start_time = time.time()
            question_file = f'{generated_question_folder}/{dataset}/{oflag}_{lib}.json'
            question_data = utils.load_json(question_file)
            res_lib_folder = f'{res_folder}/{dataset}/{lib}'
            if not os.path.exists(res_lib_folder): os.makedirs(res_lib_folder)
            # model_acs.refresh_conversation()

            for cs_question in question_data:
                cs_name = cs_question['cs_name']
                if cs_name in finished: continue
                # if cs_name not in finished: continue
                question = cs_question['question']
                cs_api_dict = api_dict[cs_name]

                logger.info(f"get result for: {cs_name}")
                result_file = f'{res_lib_folder}/{cs_name}.csv'
                res_data = []
                remain_len = len(cs_api_dict)+1
                prev_num = remain_len+1
                remain_api = cs_api_dict.copy()
                get_response = True
                while remain_len>0 and remain_len<prev_num:
                    try: 
                        res_json = model_acs.get_result(question)
                    except:
                        get_response = False 
                        break
                    # handle result
                    remain_api,res_data = combine_res_data(remain_api,res_json,res_data)
                    prev_num = remain_len
                    remain_len = len(remain_api)
                    # logger.debug("res_data len: ",len(res_data),"remain_api_len: ",remain_len,"prev_num: ",prev_num)
                    time.sleep(0.5) # avoid sending qustions too frequently

                if len(res_data)==0 or not get_response:
                    not_finished.append(cs_name)
                    continue
                else:
                    logger.debug("res_data len: ",len(res_data))
                    res_data = handle_remain_api(remain_api,res_data)
                    #save result
                    finished.append(cs_name)
                    logger.info(f"save result to: {result_file}")
                    utils.write_csv(result_file,res_data,res_head)
            
            end_time = time.time()
            logger.info(f'get result time for lib {lib}: {end_time - start_time}' )

    logger.info(f'finished code snippets: {finished}, {len(finished)} altogether.')
    logger.info(f'not finished code snippets: {not_finished}')
    pass


# question:
# [
#   { "cs_name": "xxx",
#     "question": "xxx"
#   },
#   {...}
# ]
def generate_question_pipeline(fs_config, datasets, libs,  original:bool, sim_top_k:int|None, prompt_conf:dict|None, level:int|None):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    api_elements_folder = fs_config['API_ELEMENTS_FOLDER']
    generated_question_folder = fs_config['GENERATED_QUESTOIN_FOLDER']
    oflag = 'original' if original else 'prompted'
    ques_gen = QuestionGenerator()
    prompt_list = None

    if not original:
        searched_post_folder = fs_config['SEARCHED_POST_FOLDER']
        sim_post_result_folder = fs_config['SIM_POST_RESULT_FOLDER']
        prmp_com = PromptCombiner()
        summarize = prompt_conf['summarize']
        ans = prompt_conf['with_ans']
        with_comments = prompt_conf['with_comments']

    for dataset in datasets:
        api_file = f'{api_elements_folder}/API_elements_{dataset}.json'
        api_dict = utils.load_json(api_file)
        sim_post_file = f'{sim_post_result_folder}/sim_res_{dataset}.json'
        sim_post_dict = utils.load_json(sim_post_file)
        res_folder = f'{generated_question_folder}/{dataset}'
        if not os.path.exists(res_folder): os.makedirs(res_folder)

        for lib in libs:
            question_res = []
            res_file = f'{res_folder}/{oflag}_{lib}.json'
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)

            for cs in code_snippets:
                cs_name = cs.replace('.java','')
                # load code snippet
                logger.info(f"generate question for: {cs_name}")
                code = utils.load_text(f'{input_folder_path}/{cs}')
                # load api elements
                cs_api_dict = api_dict[cs_name]
                api_elems = [elem["Node"] for elem in cs_api_dict]
                # process posts' body & summarize
                if not original:
                    sim_post_ids = sim_post_dict[lib][cs_name]['topk_sim_postIds'][0:sim_top_k]
                    post_folder = f'{searched_post_folder}/{dataset}/{lib}/{cs_name}'
                    post_list = [f'{post_folder}/{id}.json' for id in sim_post_ids]
                    prompt_list = prmp_com.generate_prompt_multiple_posts(post_list, summarize, ans, with_comments, level)
                # generate question
                question = ques_gen.generate_question(code, api_elems, prompt_list, original)
                question_res.append({"cs_name": cs_name, "question": question})

            logger.info(f'finish generate question for lib {lib},save to: {res_file}')
            utils.write_json(res_file,question_res)
        logger.info(f'finish generate question for dataset {dataset}')
    pass