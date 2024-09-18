import re
import os
import time
import torch
import jpype
import logging
from nltk import sent_tokenize
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

import utils
from Online.obj import PromptGenerator
from Online.obj import tokenize
from config import PEGUSUS_env as ENV


class TextSummarizer(object):
    logger = logging.getLogger(__name__)
    model_name = ENV.SUM_MODEL_NAME
    size = ENV.MAX_BATCH_SIZE
    code_token_number = ENV.CODE_TOKEN_NUMBER
    sentence_number = ENV.SENTENCE_NUMBER

    def __init__(self, level, fqn_file) -> None:
        average_word_len = 6
        self.max_text_len = self.size*average_word_len
        self.max_output = round(self.max_text_len*(ENV.SUMMARIZATION_RATIO+0.05)/average_word_len)
        self.min_output = round(self.max_text_len*(ENV.SUMMARIZATION_RATIO-0.05)/average_word_len)
        # load model and tokenizer
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        device = torch.device(f'cuda:{ENV.CUDADEVICE}' if torch.cuda.is_available() else "cpu")
        # device = torch.device(f'cuda' if torch.cuda.is_available() else "cpu")
        print(device)
        self.model.to(device)
        self.fqn_set = utils.read_pickle(fqn_file)['simple_list']
        self.text_level = level
        pass

    # split text into small pieces
    def split_text(self, text):  # ensure text's length is less than model's max length
        splited_body = []
        sentences = sent_tokenize(text)
        part = ""
        part_len = 0
        for sentence in sentences:
            part += sentence+" "
            part_len += len(sentence)
            if part_len > self.max_text_len:
                splited_body.append(part)
                part = ""
                part_len = 0
        if len(part)>0:
            if len(part)<self.max_text_len/2 and len(splited_body)>0:
                splited_body[-1] += part
            else: splited_body.append(part)
        return splited_body


    def judge_api(self, token) -> bool:
        if "()" in token: return True
        elif "." in token and len(token.replace('.', '')) > 3: return True
        else: return False

    def select_sentences(self, body, imp_tokens) -> str:
        selected = ""
        sentences = sent_tokenize(body)
        body_tokens = []
        # print(len(sentences))
        for sentence in sentences:
            sen_tokens = tokenize(sentence)
            if any(word in sentence for word in imp_tokens) or any (token in self.fqn_set for token in sen_tokens):
                selected += sentence + " "
            body_tokens.append(sen_tokens)

        return selected

    # remove code and tags from body, and split text into small pieces
    def preprocess_body(self, body, api_elems)->list[str]:
        selected = ""
        codes = []
        if self.text_level >=1:
            pre_codes = re.findall(r'<pre><code>(.*?)</code></pre>',body,re.DOTALL)
            for pre_code in pre_codes: 
                if '\n' not in pre_code: continue
                if self.text_level >=2: codes.append(pre_code) # save codes for calculating important api
                body = body.replace(pre_code, '') # remove codes from body
        if self.text_level==1: selected = '\n'.join(codes)
        else: selected = body

        if self.text_level >=3:
            self.logger.debug(f'imp_tokens:{api_elems}')
            selected = self.select_sentences(body, api_elems)
        selected = re.sub(r'<.*?>','',selected,flags=re.DOTALL) # remove tags from body, e.g <p>, <strong>
        self.logger.debug(f"selected text: {selected}")
        splited_body = self.split_text(selected)
        return splited_body

    # input: unprocessed body; output: summary of text
    def generate_summary_pegasus(self, splited_text: list[str]):
        summary = ""
        # splited_text = self.split_text(text)
        for input in splited_text:
            if len(input) > 200:
                input_ids = self.tokenizer.encode(input, return_tensors="pt", max_length=512, truncation=True)
                input_ids = input_ids.to(self.model.device)
                summary_ids = self.model.generate(input_ids, 
                    max_length=self.max_output,
                    min_length=self.min_output,
                    length_penalty=1.0,
                    num_beams=4,
                    early_stopping=True,
                    repetition_penalty=1.5,
                    no_repeat_ngram_size=3)
                summary += self.tokenizer.decode(summary_ids[0], skip_special_tokens=True) + " "
            else:
                summary += input + " "
        return summary
    pass


class PromptCombiner(object):

    def __init__(self, level, fqn_file) -> None:
        self.logger = logging.getLogger(__name__)
        self.summarizer = TextSummarizer(level, fqn_file)
        pass

    # # attach comments after question and answers
    # def add_comments(self, text, comments, sum, api_elems):
    #     for com in comments:
    #         com_text = self.summarizer.preprocess_body(com["Body"], api_elems)
    #         if sum:
    #             com_text = self.summarizer.generate_summary_pegasus(com_text)
    #         else:
    #             com_text = "".join(com_text)
    #         if len(com_text)>0: text += com_text
    #     return text

    # combine code snippet,text in question, answer and comments
    def gen_prompt_singal_post(self, body, sum, api_elems):
        text = self.summarizer.preprocess_body(body, api_elems)
        if sum:
            prompt = self.summarizer.generate_summary_pegasus(text)
        else:
            prompt = "".join(text)
        self.logger.debug(f'\nsummarize:\n {prompt}\n')
        return prompt

    # generate context from related posts
    # post_list: list of post file paths
    def generate_prompt_multiple_posts(self, post_list:list, summarize:bool, api_elems=None):
        prompt_list = []
        for post_file in post_list:
            post = utils.load_text(post_file)
            self.logger.info(f"generate prompt for post: {post_file}")
            prompt = self.gen_prompt_singal_post(post, summarize, api_elems)
            prompt_list.append(prompt)
        return prompt_list


def generate_question_signal(code_snippet, api_elems, original: bool, post_list: int | None, prompt_conf: dict | None):
    logger = logging.getLogger(__name__)
    ques_gen = PromptGenerator()
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
    fqn_file = fs_config['API_DICT_FILE']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    ques_gen = PromptGenerator()
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
