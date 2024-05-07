import os
import re
import sys
import logging
from lxml import etree
from nltk.text import TextCollection

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils
import Preprocess.code_tokenizer as CToken


def create_corpus(so_post_folder,res_folder):
    logger = logging.getLogger(__name__)
    logger.info("start creating corpus...")
    if not os.path.exists(res_folder): os.makedirs(res_folder)
    post_docs = os.listdir(so_post_folder)
    post_texts = []
    code_texts = []

    for doc in post_docs:
        doc_path = f'{so_post_folder}/{doc}'
        logger.info(f"processing file: {doc_path}")
        content = etree.iterparse(doc_path, events=('end',), tag='row')
        for _, elem in content:
            score = int(elem.get('Score'))
            if score < 50: continue
            body = elem.get('Body')
            codes = re.findall(r'<code>(.*?)</code>', body, re.DOTALL)
            for code in codes:
                if '\n' not in code: continue
                ctokens = CToken.tokenize(code)
                code_texts.append(ctokens)
                body = body.replace(code, '')
            body = re.sub(r'<.*?>','',body,flags=re.DOTALL)
            doc_tokens = CToken.tokenize(body)
            post_texts.append(doc_tokens)
            elem.clear()
    post_corpus = TextCollection(post_texts)
    code_corpus = TextCollection(code_texts)

    logger.info(f"save corpus to: {res_folder}")
    utils.write_pickle(f'{res_folder}/post_corpus.pkl', post_corpus)
    utils.write_pickle(f'{res_folder}/code_corpus.pkl', code_corpus)
    logger.info(f"number of docs in post corpus: {len(post_texts)}")
    logger.info(f"number of docs in code corpus: {len(code_texts)}")
    logger.info("finish creating corpus!")
    pass


if __name__ == '__main__':
    so_post_folder= '../data/SOData/tags/java/questions'
    post_docs = os.listdir(so_post_folder)
    sum = 0
    count = 0
    for doc in post_docs:
        so_post_file = f'{so_post_folder}/{doc}'
        print(f"==>> Processing: {so_post_file}")
        content = etree.iterparse(so_post_file, events=('end',), tag='row')
        for _, row in content:
            num = int(row.get('Score'))
            if num>50: count += 1
    print(count)
    pass