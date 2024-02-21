import os
import re
import sys
import json
import logging
from re_gpt import SyncChatGPT
from time import sleep
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config.chatgpt_conf as Conf

class ModelAccesser(object):
    cur_session_num = 0
    logger = logging.getLogger(__name__)
    conversation = None
    
    def __init__(self) -> None:
        if Conf.PROXY_URL:
            os.environ['http_proxy'] = Conf.PROXY_URL
            os.environ['https_proxy'] = Conf.PROXY_URL
        self.session_tokens = Conf.SESSION_TOKEN
        self.token_num = len(Conf.SESSION_TOKEN)
        session_token = self.session_tokens[self.cur_session_num]
        with SyncChatGPT(session_token=session_token) as chatgpt:
            self.gpt = chatgpt
        # Set the http_proxy and https_proxy environment variable
        self.logger.info("Init ModelAccesser successfully.")
        pass


    def refresh_conversation(self):
        self.conversation = self.gpt.create_new_conversation()
        self.logger.info("Refresh conversation successfully.")
        pass

    def change_account(self):
        flag = False
        time = 0
        while not flag:
            self.cur_session_num = (self.cur_session_num+1)%self.token_num
            session_token = self.session_tokens[self.cur_session_num]
            try:
                del self.gpt
                self.gpt = SyncChatGPT(session_token=session_token)
                self.conversation = self.gpt.create_new_conversation()
                flag = True
            except:
                self.logger.error("Failed to change account, try again in 60 seconds.")
                time += 1
                if time >= self.token_num:
                    self.logger.error("Failed to change account, all accounts are invalid.")
                    exit(1)
                else:
                    sleep(60)
        self.logger.info(f"Change account to {self.cur_session_num} successfully.")
        pass


    def ask_question(self,question:str):
        chat_stream = self.conversation.chat(question)
        response = ""
        for msg in chat_stream:
            if msg == "":
                break
            response += msg["content"]
        self.logger.info(f"model accesser recieved a response.")
        return response
    
    # split json object from response
    def handle_response(self,response):
        result_string = re.findall(r'\{([^}]*)\}', response)
        result_obj = None
        for result in result_string:
            result = re.sub(r'//.*', '', result)
            json_str = "{" + result + "}"
            try: 
                obj = json.loads(json_str)
                result_obj = obj
                break
            except:
                continue
        return result_obj


    def get_result(self,prompt:str):
        response = self.ask_question(prompt)
        result_json = self.handle_response(response)
        if result_json is None:
            self.logger.warn(f'no json object found in response: "{response}", try to change account...')
            self.change_account()
            response = self.ask_question(prompt)
            result_json = self.handle_response(response)
        if result_json is None:
            self.logger.error(f'get response: "{response}"')
            raise Exception('failed to get result for prompt, please check your question and configuration.')
        return result_json


if __name__ == "__main__":
    pass