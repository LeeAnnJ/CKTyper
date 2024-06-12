import logging

from utils import load_text
from Online_Processing.obj import TextSummarizer

class PromptCombiner(object):

    def __init__(self, level, corpus_fodler, fqn_file) -> None:
        self.logger = logging.getLogger(__name__)
        self.summarizer = TextSummarizer(level, corpus_fodler, fqn_file)
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
            post = load_text(post_file)
            self.logger.info(f"generate prompt for post: {post_file}")
            prompt = self.gen_prompt_singal_post(post, summarize, api_elems)
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
