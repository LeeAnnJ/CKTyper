import re
import os
import sys
import torch
import logging
from nltk import sent_tokenize
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
import config.text_summarizer_env as ENV
import Preprocess.code_tokenizer as Tokenizer

class TextSummarizer(object):
    logger = logging.getLogger(__name__)
    model_name = ENV.SUM_MODEL_NAME
    size = ENV.MAX_BATCH_SIZE
    max_text_len = ENV.AVERAGE_WORD_LENGTH*size
    code_token_number = ENV.CODE_TOKEN_NUMBER
    sentence_number = ENV.SENTENCE_NUMBER

    def __init__(self, level, corpus_folder, fqn_file) -> None:
        # load model and tokenizer
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        device = torch.device(f'cuda:{ENV.CUDADEVICE}' if torch.cuda.is_available() else "cpu")
        # device = torch.device(f'cuda' if torch.cuda.is_available() else "cpu")
        print(device)
        self.model.to(device)
        # load corpus
        self.code_corpus = utils.read_pickle(f'{corpus_folder}/code_corpus.pkl')
        self.post_corpus = utils.read_pickle(f'{corpus_folder}/post_corpus.pkl')
        self.fqn_set = utils.read_pickle(fqn_file)['simple_list']
        self.text_level = level
        pass
    

    # split text into small pieces
    def split_text(self,text): # ensure text's length is less than model's max length
        splited_body = []
        sentences = sent_tokenize(text)
        part = ""
        part_len = 0
        for sentence in sentences:
            part += sentence+" "
            part_len += len(sentence)
            if part_len > self.size:
                splited_body.append(part)
                part = ""
                part_len = 0
        if len(part)>0:
            if len(part)<self.size/2 and len(splited_body)>0:
                splited_body[-1] += part
            else: splited_body.append(part)
        return splited_body

    def cal_import_tokens(self, codes, api_elems)->list[str]:
        imp_tokens = api_elems.copy()
        # code_tokens = []
        # # calculate tf-idf for each token in code
        # for code in codes:
        #     tokens = Tokenizer.tokenize(code)
        #     code_tokens.extend([[token, self.code_corpus.tf_idf(token,code)] for token in tokens])
        # code_tokens = sorted(code_tokens, key=lambda x:x[1], reverse=True)
        # # add most important tokens to imp_tokens
        # count = 0
        # for token in code_tokens:
        #     if token[0] not in imp_tokens:
        #         imp_tokens.append(token[0])
        #         count += 1
        #     if count >= self.code_token_number: break
        return imp_tokens

    def judge_api(self, token)->bool:
        if "()" in token: return True
        elif "." in token and len(token.replace('.',''))>3: return True
        else: return False

    def select_sentences(self, body, imp_tokens)->str:
        selected = ""
        sentences = sent_tokenize(body)
        body_tokens = []
        # print(len(sentences))
        for sentence in sentences:
            sen_tokens = Tokenizer.tokenize(sentence)
            # if any(word in sentence for word in imp_tokens) or any(self.judge_api(token) for token in sen_tokens) or len(re.findall(r'<code>(.*?)</code>', sentence))>0:
            if any(word in sentence for word in imp_tokens) or any (token in self.fqn_set for token in sen_tokens):
                selected += sentence + " "
            body_tokens.append(sen_tokens)

        # if len(selected)==0:
        #     token_tf_idf = []
        #     for i in range(len(body_tokens)):
        #         sen_token = body_tokens[i]
        #         token_tf_idf.extend( [[token,i,self.post_corpus.tf_idf(token,body)] for token in sen_token])
        #     token_tf_idf = sorted(token_tf_idf, key=lambda x:x[2], reverse=True)
        #     count = 0
        #     selected_idx = []
        #     for token in token_tf_idf:
        #         if token[1] not in selected_idx:
        #             # print(token)
        #             selected_idx.append(token[1])
        #             count += 1
        #         if count >= self.sentence_number: break
        #     for idx in sorted(selected_idx):
        #         selected += sentences[idx]
        # self.logger.debug(f"selected sentences: {selected}")
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
        selected = body
        if self.text_level >=2:
            imp_tokens = self.cal_import_tokens(codes, api_elems)
            self.logger.debug(f'imp_tokens:{imp_tokens}')
            selected = self.select_sentences(body, imp_tokens)
        selected = re.sub(r'<.*?>','',selected,flags=re.DOTALL) # remove tags from body, e.g <p>, <strong>
        self.logger.debug(f"selected text: {selected}")
        splited_body = self.split_text(selected)
        return splited_body

    
    # input: unprocessed body; output: summary of text
    def generate_summary_pegasus(self, splited_text:list[str]): 
        summary = ""
        # splited_text = self.split_text(text)
        for input in splited_text:
            if len(input) > 200:
                input_ids = self.tokenizer.encode(input, return_tensors="pt", max_length=512, truncation=True)
                input_ids = input_ids.to(self.model.device)
                summary_ids = self.model.generate(input_ids, max_length=512, length_penalty=1.0, num_beams=4, early_stopping=True)
                summary += self.tokenizer.decode(summary_ids[0], skip_special_tokens=True) + " "
            else:
                summary += input + " "
        return summary
    pass

if __name__ == '__main__':
    text = '''
    '''
    api_elems = ["DApp","summer","API"]
    summarizer = TextSummarizer("../data/corpus/")
    res = summarizer.preprocess_body(text,2,api_elems)
    print(res)
    pass