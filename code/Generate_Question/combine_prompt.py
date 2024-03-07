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
    def add_comments(self, text, comments, sum, level):
        for com in comments:
            com_text = self.summarizer.preprocess_body(com["Body"], level)
            if sum and len(com_text)>200:
                com_text = self.summarizer.generate_summary_pegasus(com_text)
            if len(com_text)>0: text += com_text
        return text


    # combine code snippet,text in question, answer and comments
    def generate_prompt_singal_post(self, post, sum:bool, with_ans:bool, with_comments:bool, level:int):
        # get question text
        question = post["Question"]
        ques_title = question["Title"]
        ques_body = question["Body"]
        ques_text = self.summarizer.preprocess_body(ques_body,level)
        if sum and len(ques_text)>200:
            ques_text = self.summarizer.generate_summary_pegasus(ques_text)
        if with_comments: # add comments text
            ques_comments = question["Comments"]
            ques_text = self.add_comments(ques_text,ques_comments,sum)

        if with_ans: # get answer texts
            answers = post["Answers"]
            ans_texts = ""
            for answer in answers:
                ans_body = answer["Body"]
                ans_text = self.summarizer.preprocess_body(ans_body,level)
                if sum and len(ans_text)>200:
                    ans_text = self.summarizer.generate_summary_pegasus(ans_text)
                if with_comments: # add comments text
                    ans_comments = answer["Comments"]
                    ans_text = self.add_comments(ans_text,ans_comments,sum)
                ans_texts += ans_text
            prompt = ques_title + ques_text + ans_texts
        else:
            prompt = ques_title + ques_text
        return prompt
    
    # generate context from related posts
    # post_list: list of post file paths
    def generate_prompt_multiple_posts(self, post_list:list, summarize, ans, with_comments, level):
        prompt_list = []
        for post_file in post_list:
            post = utils.load_json(post_file)
            self.logger.info(f"generate prompt for post: {post_file}")
            prompt = self.generate_prompt_singal_post(post, summarize, ans, with_comments, level)
            prompt_list.append(prompt)
        return prompt_list


if __name__ == '__main__':
    # combinber = PromptCombiner()
    # base_folder = "..\Evaluation\SearchContentByPostId\StatType-SO\gwt\gwt_class_2"
    # prompt = combinber.generate_prompt_multiple_posts(base_folder,True,False,False)
    # print(prompt)
    # with open('./test.json', 'w') as jf:
    #     json.dump(prompt, jf)
    pass