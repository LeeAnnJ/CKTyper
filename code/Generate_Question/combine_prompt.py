import os
import sys
import logging
import configparser
from Generate_Question.summarize import TextSummarizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

class PromptCombiner(object):

    def __init__(self) -> None:
        self.summarizer = TextSummarizer()
        config = configparser.ConfigParser()
        config.read('./config/file_structure.ini')
        self.json_folder = config['intermediate']['SEARCHED_POST_FOLDER']
        self.logger = logging.getLogger(__name__)
        pass

    # attach comments after question and answers
    def add_comments(self,text,comments,sum:bool):
        for com in comments:
            com_text = self.summarizer.preprocess_body(com["Body"])
            if(sum):
                com_text = self.summarizer.generate_summary_pegasus(com_text)
            text += com_text
        return text


    # combine code snippet,text in question, answer and comments
    def generate_prompt_singal_post(self, post, sum:bool,ans:bool, with_comments:bool):
        # get question text
        question = post["Question"]
        ques_text = self.summarizer.preprocess_body(question["Body"])
        if(sum):
            ques_text = self.summarizer.generate_summary_pegasus(ques_text)
        if(with_comments): # add comments text
            ques_comments = question["Comments"]
            ques_text = self.add_comments(ques_text,ques_comments,sum)

        if (ans):# get answer texts
            answers = post["Answers"]
            # ans_texts = []
            ans_texts = ""
            for ans in answers:
                ans_body = ans["Body"]
                ans_text = self.summarizer.preprocess_body(ans_body)
                if(sum):
                    ans_text = self.summarizer.generate_summary_pegasus(ans_text)
                
                if(with_comments): # add comments text
                    ans_comments = ans["Comments"]
                    ans_text = self.add_comments(ans_text,ans_comments,sum)
                # ans_texts.append(ans_text)
                ans_texts += ans_text
            prompt = ques_text + ans_texts
        else:
            prompt = ques_text
        return prompt
    
    # generate context from related posts
    # base_folder: related posts' folder
    # post_ids: list of post ids, e.g. ['122','123']
    def generate_prompt_multiple_posts(self, base_folder:str, sum:bool, ans:bool, with_comments:bool):
        prompt_list = []
        post_list = os.listdir(base_folder)
        for post_name in post_list:
            post_file = f'{base_folder}/{post_name}' # todo: reconsider file path
            post = utils.load_json(post_file)
            self.logger.info(f"generate prompt for post: {post_name}")
            prompt = self.generate_prompt_singal_post(post,sum,ans,with_comments)
            prompt_list.append(prompt)
        return prompt_list


if __name__ == '__main__':
    # with open(file_name, 'r') as tf:
    #     data = json.load(tf)
    # print(type(data["Answers"][0]["Body"])
    # with open(code_file, 'r') as cf:
    #     code = cf.read()
    # print(type(code))
    # combinber = PromptCombiner()
    # prompt = combinber.generate_singal_prompt(code,data,True,True)
    # print(prompt)
    # with open('./test.json', 'w') as jf:
    #     json.dump(prompt, jf)
    pass