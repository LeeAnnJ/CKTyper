import re
import torch
import logging
from nltk import sent_tokenize
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

import utils
from config import text_summarizer_env as ENV
from Online_Processing.obj import tokenize

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


if __name__ == '__main__':
    text = '''
    '''
    api_elems = ["DApp", "summer", "API"]
    summarizer = TextSummarizer(3, "")
    res = summarizer.preprocess_body(text, 2, api_elems)
    abs = summarizer.generate_summary_pegasus(res)
    print(res)
    pass
