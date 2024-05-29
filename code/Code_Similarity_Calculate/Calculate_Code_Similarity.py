import os
import sys
import time
import pickle
import logging
import configparser
from pathlib import Path
from nltk import word_tokenize
from nltk.util import ngrams
from collections import Counter
from itertools import islice
from crystalbleu import corpus_bleu
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config.task_setting as TS
import utils

# extract ngrams' frequencies from SO code corpus, and save the frequency counter of each xml to a pickle file
def extract_ngrams_frequencies_per_xml(so_code_dir,frequency_counter_save_dir):
    logger = logging.getLogger(__name__)

    if not os.path.exists(frequency_counter_save_dir):
        os.makedirs(frequency_counter_save_dir)

    logger.info(f"Extracting trivially shared n-grams from SO code corpus...")
    logger.info(f"so_code_dir: {so_code_dir}")
    # <tokenized_corpus> is a list of strings
    for file in so_code_dir.iterdir():        
        logger.info(f"processing file: {file}")
        file_tokenized_corpus = []
        with open(file, 'r', encoding='utf-8') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for code in root.findall('code'):
                code_text = code.get('Code')
                code_tokenized = word_tokenize(code_text)
                file_tokenized_corpus.extend(code_tokenized)

        # Calculate frequencies of all n-grams
        file_all_ngrams = []
        for n in range(1, 5):
            file_all_ngrams.extend(list(ngrams(file_tokenized_corpus, n)))
        frequencies = Counter(file_all_ngrams)
            
        # Save frequencies of n-grams per file
        save_pickle_path = f'{frequency_counter_save_dir}/{file.stem}_ngram_frequencies_counter.pkl'
        with open(save_pickle_path, 'wb') as f:
            pickle.dump(frequencies, f)


# combine all frequency counters and calculate trivially shared ngrams
def calculate_trivially_shared_ngrams(frequency_counter_save_dir,middle_execution_progress_save_dir,save_file,topk):
    logger = logging.getLogger(__name__)
    # Load Counters and Calculate
    all_ngram_frequencies = Counter()
    # Sort the pkl_files by name
    pkl_files = sorted(Path(frequency_counter_save_dir).iterdir())

    if not os.path.exists(middle_execution_progress_save_dir):
        os.makedirs(middle_execution_progress_save_dir)

    # Check the existing _freq.pkl files and load the last existing middle execution progress _freq.pkl file
    last_freq_file = None
    start_index = 0
    for i, pkl_file in enumerate(pkl_files):
        freq_file = f'{middle_execution_progress_save_dir}/{pkl_file.stem}_freq.pkl'
        if freq_file.exists(): # the result has been calculated before
            last_freq_file = freq_file
            start_index = i + 1
        else:
            break
    if last_freq_file is not None:
        logger.info(f"Loading middle execution progress freq_file: {last_freq_file}")
        with open(last_freq_file, 'rb') as f:
            all_ngram_frequencies = pickle.load(f)

    # Continue from the last calculated pkl_file
    for pkl_file in pkl_files[start_index:]: 
        logger.info(f"Loading pkl_file: {pkl_file}")  
        with open(pkl_file, 'rb') as f:  # Load the pkl_file and update all_ngram_frequencies
            all_ngram_frequencies += pickle.load(f)

        # Save all_ngram_frequencies to the _freq.pkl file
        freq_file = f'{middle_execution_progress_save_dir}/{pkl_file.stem}_freq.pkl'
        logger.info(f"Saving middle execution progress freq_file: {freq_file}")
        with open(freq_file, 'wb') as f:
            pickle.dump(all_ngram_frequencies, f)
    
    trivially_shared_ngrams = dict(all_ngram_frequencies.most_common(topk))

    # save to pickle file
    logger.info(f"==>> Trivially shared ngrams has been saved to: {save_file}")
    with open(save_file, 'wb') as f:
        pickle.dump(trivially_shared_ngrams, f)
    return trivially_shared_ngrams


class SimilarityCalculator(object):
    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('./config/file_structure.ini')
        # 3. Load trivially shared n-grams
        file_path = config['intermediate']['NGRAM_FILE']
        with open(file_path, 'rb') as f:
            self.trivially_shared_ngrams = pickle.loads(f.read())
        # print(f"==>> trivially_shared_ngrams: {trivially_shared_ngrams}")
        pass

    # Calculate CrystalBLEU for input code and each lucene code
    # input_code_snippet: string
    # lucene_topk_paths: list of Path
    # return: dict of {lucene_topk_path: crystalBLEU_score}
    def cal_crystalBLEU_similarity(self, input_code_snippet, lucene_topk_paths):
        input_code_tokenized = word_tokenize(input_code_snippet)
        file_score_dict = {}

        for lucene_topk_path in lucene_topk_paths:
            lucene_code_snippet = utils.load_text(lucene_topk_path)
            lucene_code_tokenized = word_tokenize(lucene_code_snippet)
            crystalBLEU_score = corpus_bleu([[input_code_tokenized]], [lucene_code_tokenized] , ignoring=self.trivially_shared_ngrams)
            file_score_dict[lucene_topk_path] = crystalBLEU_score

        return file_score_dict


# Preprocess
def similarity_preprocess(config):
    logger = logging.getLogger(__name__)
    # config = configparser.ConfigParser()
    # config.read('./config/file_structure.ini')

    # 1. Extract trivially shared n-grams from SO code corpus
    so_code_dir = config['SO_CODE_FOLDER']
    frequency_counter_save_dir = f'../data/SO_code_ngram_frequency_counters'

    start_time = time.process_time()   
    extract_ngrams_frequencies_per_xml(so_code_dir,frequency_counter_save_dir)
    end_time = time.process_time()
    logger.info ('Corpus ngrams\' frequency counting time:', end_time - start_time) # 3504.90625s (58.4min), server:4918.986504939s (81.97min)

    # 2. Calculate trivially shared n-grams
    middle_execution_progress_save_dir = f'../data/Code_Similarity_Calculate/ngram_freq_sum_middle_execution_progress'
    k = 500 # number of trivially shared n-grams
    ngram_file = config['intermediate']['NGRAM_FILE']
    start_time = time.process_time()    
    trivially_shared_ngrams = calculate_trivially_shared_ngrams(frequency_counter_save_dir,middle_execution_progress_save_dir,ngram_file,k)
    end_time = time.process_time()
    logger.info ('Combine counters and calculate trivially shared ngrams time:',end_time - start_time) # 21762.626509856997s (6h)
    logger.debug(f"trivially_shared_ngrams: {trivially_shared_ngrams}")
    pass


# lucene_topk_dic: the folder path of lucene top-k code snippets
# output: a list of top-k similar postIds & similarity, e.g. ['122','123'],[1.0,0.9,0.9]
def cal_similarity_singal(code_snippet:str, lucene_topk_dic, calculator:SimilarityCalculator, sim_topk):
    # 6. Calculate CrystalBLEU for input code and each lucene code
    # start_time = time.process_time()
    lucene_topk_paths = Path(lucene_topk_dic).iterdir()
    file_score_dict = calculator.cal_crystalBLEU_similarity(code_snippet, lucene_topk_paths)
    # end_time = time.process_time()
    # print ('Calculate CrystalBLEU time:',end_time - start_time)

    # 7. Sort the file_score_dict by value, and print the postid of the top-k similar code snippet
    sorted_file_score_dict = sorted(file_score_dict.items(), key=lambda x: x[1], reverse=True)
    topk_sim_files = [item[0] for item in list(islice(sorted_file_score_dict, sim_topk))]
    sim_score = [item[1] for item in list(islice(sorted_file_score_dict, sim_topk))]
    topk_sim_postIds = [file.stem.split('_')[0] for file in topk_sim_files]
    
    # most_similar_code_snippet_path = sorted_file_score_dict[0][0]
    # most_similar_CrystalBLEU_score = sorted_file_score_dict[0][1]
    # most_similar_postId = sorted_file_score_dict[0][0].stem.split('_')[1]
    # print(f"==>> The most similar code snippet is: {most_similar_code_snippet_path}") # the file format of the path is {codeId}_{postId}_{normalized_Lucene_score}.java
    # print(f"==>> The most similar code snippet's CrystalBLEU score is: {most_similar_CrystalBLEU_score}")
    # print(f"==>> The most similar code snippet's postId is: {most_similar_postId}")

    return topk_sim_postIds, sim_score


# sim_result:
# {
#   "<lib>": {
#     "<cs_name>": {
#       "topk_sim_postIds": ["xxx","xxx","xxx"],
#       "sim_scores": [0.9,0.8,0.7]
#     },
#     "<cs_name>": {...}
#   },
#   "<lib>": {...}
# }
def cal_similarity_pipeline(fs_config, datasets, libs, lucene_topk,similarity_topk, not_finished):
    logger = logging.getLogger(__name__)
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    eval_path = fs_config['EVAL_PATH']
    sim_post_result_folder = fs_config['SIM_POST_RESULT_FOLDER']
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    lucene_folder = fs_config['LUCENE_FOLDER'].replace('topk',f'top{lucene_topk}')
    if not os.path.exists(sim_post_result_folder): os.makedirs(sim_post_result_folder)
    similarity_calculator = SimilarityCalculator()
    reflag = True if len(not_finished)>0 else False

    # 4. Load input code snippet
    for dataset in datasets:
        result_file_str = f'{sim_post_result_folder}/sim_res_{dataset}.json'
        time_record_file = f'{time_record_folder}/{dataset}.json'
        if reflag: sim_result = utils.load_json(result_file_str)
        else: sim_result = {}
        if os.path.exists(time_record_file): time_record = utils.load_json(time_record_file)
        else: time_record = {}

        for lib in libs:
            if reflag: code_snippets_result = sim_result[lib]
            else: code_snippets_result = {}
            input_folder_path = f'{dataset_code_folder}/{dataset}/{lib}'
            code_snippets = os.listdir(input_folder_path)
            if lib in time_record.keys(): time_lib = time_record[lib]
            else: time_lib = {}

            for cs in code_snippets:
                start_time = time.time()
                cs_name = cs.replace('.java','')
                if reflag and cs_name not in not_finished: continue
                if cs_name in time_lib.keys(): time_cs = time_lib[cs_name]
                else: time_cs = {}
                input_code_snippet_path = f'{input_folder_path}/{cs}'
                logger.info(f"calculate similarity for: {input_code_snippet_path}")
                # 5. Get Lucene top-k code snippets
                lucene_topk_dic = f'{lucene_folder}/{dataset}/{lib}/{cs_name}'
                # logger.debug(f" lucene_topk_dir: {lucene_topk_dic}")
                # 6. Calculate CrystalBLEU for input code and each lucene code
                input_code_snippet = utils.load_text(input_code_snippet_path)
                topk_sim_postIds,sim_score = cal_similarity_singal(input_code_snippet,lucene_topk_dic,similarity_calculator,similarity_topk)
                code_snippets_result[cs_name] = {"topk_sim_postIds": topk_sim_postIds, "sim_scores": sim_score}
                end_time = time.time()
                time_cs["sim_cal"] = end_time - start_time
                time_lib[cs_name] = time_cs

            sim_result[lib] = code_snippets_result
            time_record[lib] = time_lib
        # 8. Save the result to file
        utils.write_json(result_file_str,sim_result)
        utils.write_json(time_record_file,time_record)
        logger.info(f'Finish code similarity calculation for dataset {dataset}, save result to file:{result_file_str}')
    return


if __name__ == '__main__':
    script_path = Path(__file__).parent.absolute()
    print(script_path)
    # similarity_preprocess()
    # 4. Load input code snippet
    datasets = TS.DATASETS
    libs = TS.LIBS
    # dataset = Datasets[0]
    # lib = libs[2]
    # code_snippet_file = "hibernate_class_1.java"
    lucene_topk = 10
    similarity_topk = 3
    # cal_similarity_pipeline(datasets,libs,lucene_topk,similarity_topk)
    pass

