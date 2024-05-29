import os
import sys
import time
import jpype
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
from Generate_Question.combine_prompt import PromptCombiner
from Generate_Question.generate_question import QuestionGenerator
from Get_TypeInference_Result.handle_result import ResHandler
from Get_TypeInference_Result.call_chatgpt import ModelAccesser_V2 as ModelAccesser


# rertieve posts form SO dataset by lucene index
def retrieve_posts_pipeline(fs_config, datasets, libs, not_finished):
    searched_post_folder = fs_config['SEARCHED_POST_FOLDER']
    sim_post_result_folder = fs_config['SIM_POST_RESULT_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    PostIndexer = jpype.JClass("LucenePostIndexer")
    reflag = True if len(not_finished)>0 else False

    for dataset in datasets:
        sim_res_file = f'{sim_post_result_folder}/sim_res_{dataset}.json'
        time_record_file = f'{time_record_folder}/{dataset}.json'
        result_json = utils.load_json(sim_res_file)
        dataset_folder = f'{searched_post_folder}/{dataset}'
        if os.path.exists(time_record_file): time_record = utils.load_json(time_record_file)
        else: time_record = {}

        for lib in libs:
            lib_res = result_json[lib]
            lib_folder = f'{dataset_folder}/{lib}'
            cs_names = lib_res.keys()
            if lib in time_record.keys(): time_lib = time_record[lib]
            else: time_lib = {}

            for cs_name in cs_names:
                if reflag and cs_name not in not_finished: continue
                start_time = time.time()
                cs_res = lib_res[cs_name]
                cs_folder = f'{lib_folder}/{cs_name}'
                topk_sim_postIds = cs_res['topk_sim_postIds']
                if cs_name in time_lib.keys(): time_cs = time_lib[cs_name]
                else: time_cs = {}
                for id in topk_sim_postIds:
                    PostIndexer.main(['-online',id,cs_folder])
                end_time = time.time()
                time_cs["retrieve_post"] = end_time - start_time
                time_lib[cs_name] = time_cs

            time_record[lib] = time_lib
        utils.write_json(time_record_file,time_record)
    pass


# question:
# { 
#   "<cs_name>":"<question>",
#   "<cs_name>": "xxx"
# }
def generate_question_pipeline(fs_config, datasets, libs, not_finished, original:bool, sim_top_k:int|None, rcm_top_k:int, prompt_conf:dict|None):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    api_elements_folder = fs_config['API_ELEMENTS_FOLDER']
    generated_question_folder = fs_config['GENERATED_QUESTOIN_FOLDER']
    fqn_file = fs_config['FQN_FILE']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    ques_gen = QuestionGenerator(rcm_top_k)
    reflag = True if len(not_finished)>0 else False
    prompt_list = None

    if not original:
        searched_post_folder = fs_config['SEARCHED_POST_FOLDER']
        sim_post_result_folder = fs_config['SIM_POST_RESULT_FOLDER']
        corpus_folder = fs_config['CORPUS_FOLDER']
        summarize = prompt_conf['summarize']
        ans = prompt_conf['with_ans']
        with_comments = prompt_conf['with_comments']
        level = prompt_conf['text_filter_level']
        prmp_com = PromptCombiner(level, corpus_folder, fqn_file)

    for dataset in datasets:
        api_file = f'{api_elements_folder}/API_elements_{dataset}.json'
        api_dict = utils.load_json(api_file)
        res_folder = f'{generated_question_folder}/{dataset}'
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if not os.path.exists(res_folder): os.makedirs(res_folder)
        if not original:
            sim_post_file = f'{sim_post_result_folder}/sim_res_{dataset}.json'
            sim_post_dict = utils.load_json(sim_post_file)
        if os.path.exists(time_record_file): time_record = utils.load_json(time_record_file)
        else: time_record = {}

        for lib in libs:
            res_file = f'{res_folder}/{lib}.json'
            if reflag: question_res = utils.load_json(res_file)
            else: question_res = {}
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)
            if lib in time_record.keys(): time_lib = time_record[lib]
            else: time_lib = {}

            for cs in code_snippets:
                start_time = time.time()
                cs_name = cs.replace('.java','')
                if reflag and cs_name not in not_finished: continue
                # load code snippet
                logger.info(f"generate question for: {cs_name}")
                code = utils.load_text(f'{input_folder_path}/{cs}')
                # load api elements
                cs_api_dict = api_dict[cs_name]
                api_elems = [elem["Node"] for elem in cs_api_dict]
                if cs_name in time_lib.keys(): time_cs = time_lib[cs_name]
                else: time_cs = {}
                # process posts' body & summarize
                if not original:
                    sim_post_ids = sim_post_dict[lib][cs_name]['topk_sim_postIds'][0:sim_top_k]
                    post_folder = f'{searched_post_folder}/{dataset}/{lib}/{cs_name}'
                    post_list = [f'{post_folder}/{id}.txt' for id in sim_post_ids]
                    prompt_list = prmp_com.generate_prompt_multiple_posts(post_list, summarize, ans, with_comments, api_elems)
                # generate question
                question = ques_gen.generate_question(code, api_elems, prompt_list, original)
                question_res[cs_name]= question
                end_time = time.time()
                time_cs["generate_context"] = end_time - start_time
                time_lib[cs_name] = time_cs
            
            time_record[lib] = time_lib
            logger.info(f'finish generate question for lib {lib},save to: {res_file}')
            utils.write_json(res_file,question_res)
        
        utils.write_json(time_record_file,time_record)
        logger.info(f'finish generate question for dataset {dataset}')
    pass


def get_result_pipline(fs_config, datasets, libs, not_finished, original:bool):
    logger = logging.getLogger(__name__)
    api_elements_folder = fs_config['API_ELEMENTS_FOLDER']
    generated_question_folder = fs_config['GENERATED_QUESTOIN_FOLDER']
    fqn_file = fs_config['FQN_FILE']
    if original: res_folder = fs_config['RESULT_ORIGINAL_FOLDER']
    else: res_folder = fs_config['RESULT_PROMPTED_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    model_acs = ModelAccesser()
    res_handler = ResHandler(fqn_file)
    res_head = ["Node","ChatGPT Answer","Truth"]
    reflag = True if len(not_finished)>0 else False
    finished = []
    error_list = []

    for dataset in datasets:
        api_file = f'{api_elements_folder}/API_elements_{dataset}.json'
        api_dict = utils.load_json(api_file)
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if os.path.exists(time_record_file): time_record = utils.load_json(time_record_file)
        else: time_record = {}
        
        for lib in libs:
            question_file = f'{generated_question_folder}/{dataset}/{lib}.json'
            question_data = utils.load_json(question_file)
            res_lib_folder = f'{res_folder}/{dataset}/{lib}'
            if not os.path.exists(res_lib_folder): os.makedirs(res_lib_folder)
            if lib in time_record.keys(): time_lib = time_record[lib]
            else: time_lib = {}

            cs_names = question_data.keys()
            for cs_name in cs_names:
                start_time = time.time()
                if reflag and cs_name not in not_finished: continue
                question = question_data[cs_name]
                cs_api_dict = api_dict[cs_name]
                if cs_name in time_lib.keys(): time_cs = time_lib[cs_name]
                else: time_cs = {}

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
                    remain_api,res_data = res_handler.combine_res_data(remain_api,res_json,res_data)
                    prev_num = remain_len
                    remain_len = len(remain_api)
                    # logger.debug("res_data len: ",len(res_data),"remain_api_len: ",remain_len,"prev_num: ",prev_num)
                    time.sleep(0.5) # avoid sending qustions too frequently

                if len(res_data)==0 or not get_response:
                    error_list.append(cs_name)
                    continue
                else:
                    logger.debug("res_data len: ",len(res_data))
                    res_data = res_handler.handle_remain_api(remain_api,res_data)
                    #save result
                    finished.append(cs_name)
                    logger.info(f"save result to: {result_file}")
                    utils.write_csv(result_file,res_data,res_head)
                end_time = time.time()
                time_cs["type_inf"] = end_time - start_time
                time_lib[cs_name] = time_cs

            time_record[lib] = time_lib
            logger.info(f'finish get result for lib {lib}')
        utils.write_json(time_record_file,time_record)
    
    logger.info(f'finished code snippets: {finished}, {len(finished)} altogether.')
    logger.info(f'not finished code snippets: {error_list}')
    pass

if __name__ == '__main__':
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    start_time = time.process_time()
    PostIndexer = jpype.JClass("LucenePostIndexer")
    PostIndexer.main(['-online','126','../Evaluation/intermediate/'])
    end_time = time.process_time()
    jpype.shutdownJVM()
    print(f"Running time: {end_time-start_time}")
    pass