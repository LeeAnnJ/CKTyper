import os
import time
import logging

import utils
from Online_Processing.obj import ResHandler
from Online_Processing.obj import ModelAccesser


def get_result_pipline(fs_config, datasets, libs, not_finished, original:bool, rcm_top_k):
    logger = logging.getLogger(__name__)
    api_elements_folder = fs_config['API_ELEMENTS_FOLDER']
    generated_question_folder = fs_config['GENERATED_QUESTOIN_FOLDER']
    fqn_file = fs_config['FQN_FILE']
    if original: res_folder = fs_config['RESULT_ORIGINAL_FOLDER']
    else: res_folder = fs_config['RESULT_PROMPTED_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    model_acs = ModelAccesser()
    res_handler = ResHandler(fqn_file)
    res_head = ["Node", "ChatGPT Answer", "Truth"]
    reflag = True if len(not_finished) > 0 else False
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
                question = question_data[cs_name].replace("[k]", str(rcm_top_k))
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
                while 0 < remain_len < prev_num:
                    try: 
                        res_json = model_acs.get_result(question)
                    except:
                        get_response = False 
                        break
                    # handle result
                    remain_api, res_data = res_handler.combine_res_data(remain_api, res_json, res_data)
                    prev_num = remain_len
                    remain_len = len(remain_api)
                    # logger.debug("res_data len: ",len(res_data),"remain_api_len: ",remain_len,"prev_num: ",prev_num)
                    time.sleep(0.5)  # avoid sending qustions too frequently

                if len(res_data) == 0 or not get_response:
                    error_list.append(cs_name)
                    continue
                else:
                    logger.debug("res_data len: ", len(res_data))
                    res_data = res_handler.handle_remain_api(remain_api, res_data)
                    # save result
                    finished.append(cs_name)
                    logger.info(f"save result to: {result_file}")
                    utils.write_csv(result_file, res_data, res_head)
                end_time = time.time()
                time_cs["type_inf"] = end_time - start_time
                time_lib[cs_name] = time_cs

            time_record[lib] = time_lib
            logger.info(f'finish get result for lib {lib}')
        utils.write_json(time_record_file, time_record)
    
    logger.info(f'finished code snippets: {finished}, {len(finished)} altogether.')
    logger.info(f'not finished code snippets: {error_list}')
    pass
