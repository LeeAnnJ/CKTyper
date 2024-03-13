import os
import sys
import jpype
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
from Code_Similarity_Calculate.Calculate_Code_Similarity import cal_similarity_singal,SimilarityCalculator
from Generate_Question.combine_prompt import PromptCombiner
from Generate_Question.generate_question import QuestionGenerator
from Get_TypeInference_Result.call_chatgpt import ModelAccesser_V2 as ModelAccesser


def get_sim_posts_singal(cs_path, code_snippet, lucene_top_k, sim_top_k, res_folder):
    logger = logging.getLogger(__name__)
    PostIndexer = jpype.JClass("LucenePostIndexer")
    CodeIndexer = jpype.JClass("LuceneCodeIndexer")
    calculator = SimilarityCalculator()
    lucene_posts_dic = f'{res_folder}/Lucene_top{lucene_top_k}'
    sim_post_folder = f'{res_folder}/searched_posts/'

    # 2. search similar snippets by lucene index
    logger.info(f'search similar code snippets...')
    CodeIndexer.main(['-online',cs_path,f'{lucene_top_k}',lucene_posts_dic])
    # calculate similarity, get corresponding post ids
    logger.info(f'calculate code similarity...')
    sim_posts_ids,sim_score = cal_similarity_singal(code_snippet, lucene_posts_dic, calculator, sim_top_k)
    # 3. retrieve posts from SO posts dataset
    logger.info(f'retrieve posts from SO...')
    for post_id in sim_posts_ids:
        PostIndexer.main(['-online',post_id,sim_post_folder])
    return sim_post_folder,sim_posts_ids,sim_score


def generate_question_pipeline(code_snippet, api_elems, original:bool, post_list:int|None, prompt_conf:dict|None, level:int|None):
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
        prompt_list = prmp_com.generate_prompt_multiple_posts(post_list, summarize, ans, with_comments, level)
        logger.info("generate question...")
        question = ques_gen.generate_question(code_snippet, api_elems, prompt_list, original)
    return question


def combine_res_data(api_elems, json_res, prev_data:dict):
    remain_api = []
    for node in api_elems:
        if node in json_res.keys():
            ans = json_res[node]
            prev_data[node] = ans
        else:
            remain_api.append(node)
    return remain_api,prev_data


def handle_remain_api(remain_node, prev_data):
    ans = "<FQN not provided, as it seems to be a custom interface or not present in the code snippet>"
    for node in remain_node:
        prev_data[node] = ans
    return prev_data


def get_result_singal(question, api_elems):
    logger = logging.getLogger(__name__)
    model_acs = ModelAccesser()
    res_data = []
    remain_len = len(api_elems)+1
    prev_num = remain_len+1
    remain_api = api_elems.copy()
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

    if len(res_data)==0 or not get_response:
        logger.error("Failed to get response from ChatGPT")
        exit(1)
    else:
        res_data = handle_remain_api(remain_api,res_data)
    return res_data


if __name__ == '__main__':
    api_dict = [
        {
            "Node": "Activity",
            "Truth": "android.app.Activity"
        },
        {
            "Node": "Bundle",
            "Truth": "android.os.Bundle"
        },
        {
            "Node": "TextView",
            "Truth": "android.widget.TextView"
        }
    ]
    json_res = {
        "Activity": "123",
        "Bundle": "223",
    }
    prev_data = []
    remain_api = combine_res_data(api_dict,json_res,prev_data)
    handle_remain_api(remain_api,prev_data)
    print(prev_data)
    pass