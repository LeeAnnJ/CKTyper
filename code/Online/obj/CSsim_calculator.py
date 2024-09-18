from nltk import word_tokenize
from crystalbleu import corpus_bleu

import utils


class CSsimCalculator(object):
    def __init__(self, ngram_file) -> None:
        self.trivially_shared_ngrams = utils.read_pickle(ngram_file)
        pass
    
    def cal_crystalBLEU_similarity(self, input_code_snippet, lucene_topk_paths):
        '''
        Calculate CrystalBLEU for input code and each lucene code.
        `input_code_snippet`: string
        `lucene_topk_paths`: list of Path
        return: dict of {lucene_topk_path: crystalBLEU_score}
        '''
        input_code_tokenized = word_tokenize(input_code_snippet)
        file_score_dict = {}

        for lucene_topk_path in lucene_topk_paths:
            lucene_code_snippet = utils.load_text(lucene_topk_path)
            lucene_code_tokenized = word_tokenize(lucene_code_snippet)
            crystalBLEU_score = corpus_bleu([[input_code_tokenized]], [lucene_code_tokenized] , ignoring=self.trivially_shared_ngrams)
            file_score_dict[lucene_topk_path] = crystalBLEU_score

        return file_score_dict