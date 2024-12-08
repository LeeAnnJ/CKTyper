import os
import re
import json
import openai
import logging
from time import sleep

from config import chatgpt_conf as Conf


# todo： add model: Llama、DeepSeek、Claude
# class BaseModelAccesser(object):
#     account_num = 0
#     cur_account_num = 0
#     accounts = None
#     model_name = ""
#     model = None
#     base_message = []

#     def __init__(self) -> None:
#         if Conf.PROXY_URL: # Set the http_proxy and https_proxy environment variable
#             os.environ['http_proxy'] = Conf.PROXY_URL
#             os.environ['https_proxy'] = Conf.PROXY_URL
#         pass

# offical openai api
class ModelAccesser_V2(object):
    account_num = 0
    cur_account_num = 0
    logger = logging.getLogger(__name__)
    accounts = None
    gpt = None
    system_prompt = None
    base_message = []
    
    def __init__(self) -> None:
        if Conf.PROXY_URL: # Set the http_proxy and https_proxy environment variable
            os.environ['http_proxy'] = Conf.PROXY_URL
            os.environ['https_proxy'] = Conf.PROXY_URL
        self.model = Conf.MODEL
        self.accounts = Conf.ACCOUNTS
        self.account_num = len(Conf.ACCOUNTS)
        account = self.accounts[self.cur_account_num]
        self.gpt = openai.OpenAI(api_key=account["api_key"],base_url=account["base_url"])
        if self.system_prompt:
            self.base_message.append({"role": "system", "content": self.system_prompt})
        self.logger.info("Init ModelAccesser_V2 successfully.")
        pass

    def change_account(self):
        if self.account_num == 1:
            self.logger.error("Only one account info, can't change account.")
            return
        self.cur_account_num = (self.cur_account_num+1)%self.account_num
        account = self.accounts[self.cur_account_num]
        self.gpt = openai.OpenAI(api_key=account["api_key"],base_url=account["base_url"])
        self.logger.info(f"Change api_key successfully.")
        return

    def ask_question(self, question:str):
        messages = self.base_message.copy()
        messages.append({"role": "user", "content": question})
        time = 0
        while(True):
            try:
                complication = self.gpt.chat.completions.create(
                    model=self.model,
                    temperature = 0,
                    messages=messages,
                    response_format = { "type": "json_object" }
                )
                response = complication.choices[0].message.content
                self.logger.debug(f"recieved a response:{response}")
                return response
            except Exception as e:
                time += 1
                print(e)
                if time%3==0:
                    self.logger.error("Failed to get response, try switching account.")
                    return ""
                else:
                    self.logger.error(f"Failed to get response, try again in 30 seconds.")
                    sleep(30)

    def extract_keys_and_values(self, data):
        res = {}
        def extract(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():                   
                    if isinstance(value, dict):
                        extract(value)
                    elif not isinstance (value, list):
                        res[key] = [value]
                    else:
                        res[key] = value
            elif isinstance(obj, list):
                for item in obj:
                    extract(item)
        extract(data)
        return res
    
    # split json object from response
    def handle_response(self,response):
        result_string = re.findall(r'\{[\w\W]*\}', response)
        res_obj = {}
        for result in result_string:
            result = re.sub(r'//.*', '', result)
            json_str = result.replace("\'", '\"')
            try: 
                obj = json.loads(json_str)
                self.logger.debug(f"extracted json object: {obj}")
                extracted_obj = self.extract_keys_and_values(obj)
                self.logger.debug(f"after handle: {extracted_obj}")
                res_obj.update(extracted_obj)
            except:
                continue
        return res_obj


    def get_result(self, prompt:str):
        time = 1
        response = self.ask_question(prompt)
        result_json = self.handle_response(response)
        while result_json is None:
            if time >= self.account_num:
                raise Exception('failed to get result for prompt, please check your question and configuration.')
            self.logger.warning(f'no json object found in response: "{response}", try switching account...')
            sleep(10)
            self.change_account()
            response = self.ask_question(prompt)
            result_json = self.handle_response(response)
            time += 1
        return result_json


if __name__ == "__main__":
    mod_acs = ModelAccesser_V2()
    question = "What is the type of '1'?"
    res = mod_acs.ask_question(question)
    print(res)
    mod_acs.change_account()
    res = mod_acs.ask_question(question)
    print(res)
    pass