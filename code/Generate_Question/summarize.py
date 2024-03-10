import re
import os
import sys
import torch
from nltk import sent_tokenize
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config.text_summarizer_env as ENV

class TextSummarizer(object):
    model_name = ENV.SUM_MODEL_NAME
    size = ENV.MAX_BATCH_SIZE
    max_text_len = ENV.AVERAGE_WORD_LENGTH*size

    def __init__(self) -> None:
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        device = torch.device("cuda:{ENV.CUDADEVICE}" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        pass
    
    # remove code and tags from body, and split text into small pieces
    def preprocess_body(self,body,level:int=0)->list[str]:
        if level > 0: # remove code from body
            codes = re.findall(r'<code>(.*?)</code>',body,re.DOTALL)
            for code in codes: # remove codes from body
                if '\n' not in code: continue
                # deleted = "<pre><code>"+code+"</code></pre>"
                body = body.replace(code, '')
        body = re.sub(r'<.*?>','',body,flags=re.DOTALL) # remove tags from body, e.g <p>, <strong>
        # split text into small pieces
        splited_body = []
        sentences = sent_tokenize(text)
        part = ""
        part_len = 0
        for sentence in sentences:
            if level > 1: # keep sentences containing API elements
            # 什么样的单词是api元素?
                pass
            part += sentence
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
    
    def split_text(self,text): # ensure text's length is less than model's max length
        return [text[i:i+self.size] for i in range(0, len(text), self.size)]
    
    # input: unprocessed body; output: summary of text
    def generate_summary_pegasus(self, splited_text:list[str]): 
        summary = ""
        # splited_text = self.split_text(text)
        for input in splited_text:
            input_ids = self.tokenizer.encode(input, return_tensors="pt", max_length=512, truncation=True)
            input_ids = input_ids.to(self.model.device)
            summary_ids = self.model.generate(input_ids, max_length=512, length_penalty=1.0, num_beams=4, early_stopping=True)
            summary += self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    pass

if __name__ == '__main__':
    text = ''''''
    summarizer = TextSummarizer()
    summary = summarizer.generate_summary_pegasus(text)
    print(summary)
    pass