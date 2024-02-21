import os
import sys
import jpype
import logging
import configparser
from Get_TypeInference_Result.singal import combine_res_data
from Generate_Question.combine_prompt import PromptCombiner
from Generate_Question.generate_question import QuestionGenerator
from Get_TypeInference_Result.call_chatgpt import ModelAccesser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

# rertieve posts form SO dataset by lucene index
def retrieve_posts_pipeline(result_file):
    config = configparser.ConfigParser()
    config.read('./config/file_structure.ini')
    searched_post_folder = config['intermediate']['SEARCHED_POST_FOLDER']

    jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.class.path=./LuceneIndexer/LuceneIndexer.jar")
    PostIndexer = jpype.JClass("LucenePostIndexer")

    result_json = utils.load_json(result_file)
    for ds_res in result_json:
        dataset = ds_res['dataset']
        dataset_folder = f'{searched_post_folder}/{dataset}'
        lib_results = ds_res['libs']
        for lib_res in lib_results:
            lib = lib_res['lib']
            lib_folder = f'{dataset_folder}/{lib}'
            cs_results = lib_res['code_snippets']
            for cs_res in cs_results:
                cs_name = cs_res['cs_name']
                cs_folder = f'{lib_folder}/{cs_name}'
                topk_sim_postIds = cs_res['topk_sim_postIds']
                for id in topk_sim_postIds:
                    PostIndexer.main(['-online',id,cs_folder])
    
    jpype.shutdownJVM()
    pass


def get_result_pipline(datasets,libs,sum:bool, ans:bool, with_comments:bool,original:bool):
    logger = logging.getLogger(__name__)
    config = configparser.ConfigParser()
    config.read('./config/file_structure.ini')
    dataset_code_folder = config['resource']['DATASET_CODE_FOLDER']
    api_elements_folder = config['resource']['API_ELEMENTS_FOLDER']
    searched_post_folder = config['intermediate']['SEARCHED_POST_FOLDER']
    if original: res_folder = config['result']['RESULT_ORIGINAL_FOLDER']
    else: res_folder = config['result']['RESULT_PROMPTED_FOLDER']
    prmp_com = PromptCombiner()
    ques_gen = QuestionGenerator()
    model_acs = ModelAccesser()
    res_head = ["Node","ChatGPT Answer","Truth"]

    for dataset in datasets:
        api_file = f'{api_elements_folder}/API_elements_{dataset}.json'
        api_dict = utils.load_json(api_file)

        for lib in libs:
            res_lib_folder = f'{res_folder}/{dataset}/{lib}'
            if not os.path.exists(res_lib_folder):
                os.makedirs(res_lib_folder)
            model_acs.refresh_conversation()
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)

            for cs in code_snippets:
                cs_name = cs.replace('.java','')
                # load code snippet
                input_code_snippet_path = f'{input_folder_path}/{cs}'
                logger.info(f"==>> input code snippet: {input_code_snippet_path}")
                code = utils.load_text(input_code_snippet_path)
                # load api elements
                cs_api_dict = api_dict[cs_name]
                api_elems = [elem["Node"] for elem in cs_api_dict]
                # process posts' body & summarize
                post_folder = f'{searched_post_folder}/{dataset}/{lib}/{cs_name}'
                if original: 
                    prompt_list = None
                else:
                    prompt_list = prmp_com.generate_prompt_multiple_posts(post_folder, sum, ans, with_comments)
                    pass
                
                # generate question & get resulta
                question = ques_gen.generate_question(code, api_elems, prompt_list, original)
                logger.info("finish generate question.")
                res_json = model_acs.get_result(question)

                # handle & save result
                result_file = f'{res_lib_folder}/{cs_name}.csv'
                res_data = combine_res_data(cs_api_dict,res_json)
                logger.info(f"==>>save result to: {result_file}")
                utils.write_csv(result_file,res_data,res_head)

    pass