import os
import time
import jpype
import logging

import utils
from Online.obj import QuestionGenerator, PromptCombiner


def generate_question_signal(code_snippet, api_elems, original: bool, post_list: int | None, prompt_conf: dict | None):
    logger = logging.getLogger(__name__)
    ques_gen = QuestionGenerator()
    if original:
        logger.info("generate question...")
        question = ques_gen.generate_question(code_snippet, api_elems, None, original)
    else:
        prmp_com = PromptCombiner()
        summarize = prompt_conf['summarize']
        ans = prompt_conf['with_ans']
        with_comments = prompt_conf['with_comments']
        level = prompt_conf['text_filter_level']
        prompt_list = prmp_com.generate_prompt_multiple_posts(post_list, summarize, ans, with_comments, level)
        logger.info("generate question...")
        question = ques_gen.generate_question(code_snippet, api_elems, prompt_list, original)
    return question


# rertieve posts form SO dataset for context generation
def get_post_from_CKB_pipeline(fs_config, datasets, libs, not_finished):
    searched_post_folder = fs_config['SEARCHED_POST_FOLDER']
    sim_post_score_folder = fs_config['SIM_CS_SCORE_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    PostIndexer = jpype.JClass("LucenePostIndexer")
    reflag = True if len(not_finished) > 0 else False

    for dataset in datasets:
        sim_res_file = f'{sim_post_score_folder}/sim_res_{dataset}.json'
        time_record_file = f'{time_record_folder}/{dataset}.json'
        result_json = utils.load_json(sim_res_file)
        dataset_folder = f'{searched_post_folder}/{dataset}'
        if os.path.exists(time_record_file):
            time_record = utils.load_json(time_record_file)
        else:
            time_record = {}

        for lib in libs:
            lib_res = result_json[lib]
            lib_folder = f'{dataset_folder}/{lib}'
            cs_names = lib_res.keys()
            if lib in time_record.keys():
                time_lib = time_record[lib]
            else:
                time_lib = {}

            for cs_name in cs_names:
                if reflag and cs_name not in not_finished: continue
                start_time = time.time()
                cs_res = lib_res[cs_name]
                cs_folder = f'{lib_folder}/{cs_name}'
                topk_sim_postIds = cs_res['topk_sim_postIds']
                if cs_name in time_lib.keys():
                    time_cs = time_lib[cs_name]
                else:
                    time_cs = {}
                for id in topk_sim_postIds:
                    PostIndexer.main(['-online', id, cs_folder])
                end_time = time.time()
                time_cs["retrieve_post"] = end_time - start_time
                time_lib[cs_name] = time_cs

            time_record[lib] = time_lib
        utils.write_json(time_record_file, time_record)
    pass


# question:
# {
#   "<cs_name>":"<question>",
#   "<cs_name>": "xxx"
# }
def generate_CKcontext_pipeline(fs_config, datasets, libs, not_finished, sim_top_k: int | None, prompt_conf: dict | None):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    api_elements_folder = fs_config['API_ELEMENTS_FOLDER']
    generated_question_folder = fs_config['GENERATED_QUESTOIN_FOLDER']
    fqn_file = fs_config['FQN_FILE']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    ques_gen = QuestionGenerator()
    reflag = True if len(not_finished) > 0 else False
    prompt_list = None
    original = prompt_conf["add_context"]

    if not original:
        searched_post_folder = fs_config['SEARCHED_POST_FOLDER']
        sim_post_result_folder = fs_config['SIM_CS_SCORE_FOLDER']
        summarize = prompt_conf['summarize']
        level = prompt_conf['data_for_context']
        prmp_com = PromptCombiner(level, fqn_file)

    for dataset in datasets:
        api_file = f'{api_elements_folder}/API_elements_{dataset}.json'
        api_dict = utils.load_json(api_file)
        res_folder = f'{generated_question_folder}/{dataset}'
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if not os.path.exists(res_folder): os.makedirs(res_folder)
        if not original:
            sim_post_file = f'{sim_post_result_folder}/sim_res_{dataset}.json'
            sim_post_dict = utils.load_json(sim_post_file)
        if os.path.exists(time_record_file):
            time_record = utils.load_json(time_record_file)
        else:
            time_record = {}

        for lib in libs:
            res_file = f'{res_folder}/{lib}.json'
            if reflag:
                question_res = utils.load_json(res_file)
            else:
                question_res = {}
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)
            if lib in time_record.keys():
                time_lib = time_record[lib]
            else:
                time_lib = {}

            for cs in code_snippets:
                start_time = time.time()
                cs_name = cs.replace('.java', '')
                if reflag and cs_name not in not_finished: continue
                # load code snippet
                logger.info(f"generate question for: {cs_name}")
                code = utils.load_text(f'{input_folder_path}/{cs}')
                # load api elements
                cs_api_dict = api_dict[cs_name]
                api_elems = [elem["Node"] for elem in cs_api_dict]
                if cs_name in time_lib.keys():
                    time_cs = time_lib[cs_name]
                else:
                    time_cs = {}
                # process posts' body & summarize
                if not original:
                    sim_post_ids = sim_post_dict[lib][cs_name]['topk_sim_postIds'][0:sim_top_k]
                    post_folder = f'{searched_post_folder}/{dataset}/{lib}/{cs_name}'
                    post_list = [f'{post_folder}/{id}.txt' for id in sim_post_ids]
                    prompt_list = prmp_com.generate_prompt_multiple_posts(post_list, summarize, api_elems)
                # generate question
                question = ques_gen.generate_question(code, api_elems, prompt_list, original)
                question_res[cs_name] = question
                end_time = time.time()
                time_cs["generate_context"] = end_time - start_time
                time_lib[cs_name] = time_cs

            time_record[lib] = time_lib
            logger.info(f'finish generate question for lib {lib},save to: {res_file}')
            utils.write_json(res_file, question_res)

        utils.write_json(time_record_file, time_record)
        logger.info(f'finish generate question for dataset {dataset}')
    pass


if __name__ == '__main__':
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Xmx4g', "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    start_time = time.process_time()
    PostIndexer = jpype.JClass("LucenePostIndexer")
    PostIndexer.main(['-online', '126', '../Evaluation/intermediate/'])
    end_time = time.process_time()
    jpype.shutdownJVM()
    print(f"Running time: {end_time-start_time}")
    pass
