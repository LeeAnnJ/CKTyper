import os
import heapq
import shutil
import pickle
import logging
from lxml import etree
import xml.etree.ElementTree as ET

from pathlib import Path
from nltk.util import ngrams
from nltk import word_tokenize
from collections import Counter

from utils import writeObjs2xml
from Offline_Processing.obj import Post
from Offline_Processing.obj import CodeExtracter


# extract ngrams' frequencies from SO code corpus, and save the frequency counter of each xml to a pickle file
def extract_ngrams_frequencies_per_xml(so_code_dir, frequency_counter_save_dir):
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
def calculate_trivially_shared_ngrams(frequency_counter_save_dir, middle_execution_progress_save_dir, save_file, topk):
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
        if freq_file.exists():  # the result has been calculated before
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
    logger.debug(f"trivially_shared_ngrams: {trivially_shared_ngrams}")
    with open(save_file, 'wb') as f:
        pickle.dump(trivially_shared_ngrams, f)
    return


# Offline_Processing
def similarity_preprocess(fs_config):
    # 1. Extract trivially shared n-grams from SO code corpus
    so_code_dir = fs_config['SO_CODE_FOLDER']
    exp_folder = '../data/Code_Similarity_Calculate'
    frequency_counter_save_dir = f'{exp_folder}/SO_code_ngram_frequency_counters'
    # start_time = time.process_time()
    extract_ngrams_frequencies_per_xml(so_code_dir, frequency_counter_save_dir)
    # end_time = time.process_time() # 3504.90625s (58.4min), server:4918.986504939s (81.97min)
    # logger.info('Corpus ngrams\' frequency counting time:', end_time - start_time)

    # 2. Calculate trivially shared n-grams
    middle_execution_progress_save_dir = f'{exp_folder}/ngram_freq_sum_middle_execution_progress'
    ngram_file = fs_config['NGRAM_FILE']
    k = 500  # number of trivially shared n-grams
    # start_time = time.process_time()
    calculate_trivially_shared_ngrams(frequency_counter_save_dir,middle_execution_progress_save_dir,ngram_file,k)
    # end_time = time.process_time() # 21762.626509856997s (6h)
    # logger.info('Combine counters and calculate trivially shared ngrams time:',end_time - start_time)
    shutil.rmtree(exp_folder)
    pass



def parse_xml(file):
    return ET.parse(file).getroot().findall('row')

def sort_singal_file(file_name, source_folder, res_folder):
    ans_elems = []
    ans_file = f'{source_folder}/{file_name}'
    context = etree.iterparse(ans_file, events=('end',), tag='row')
    for _, elem in context:
        ans_elems.append(Post(elem))
    ans_elems.sort()
    sorted_file = f'{res_folder}/{file_name}'
    writeObjs2xml(sorted_file, ans_elems, 'Answers')
    return


def merge_files(groups, res_folder, tmp_folder):
    logger = logging.getLogger(__name__)
    logger.info(f"merge files: {groups} from {tmp_folder} to {res_folder}")
    heap = []
    file_iters = [iter(parse_xml(f"{tmp_folder}/{group[0]}")) for group in groups]

    for i, file_iter in enumerate(file_iters):
        try:
            elem = next(file_iter)
            record = Post(elem)
            heapq.heappush(heap, (record, i))
        except StopIteration:
            continue

    merged_records = []
    res_file_list = []
    iter_count = [1, 1, 1, 1]
    file_count = 0
    for group in groups: res_file_list.extend(group)
    
    while heap:
        record, i = heapq.heappop(heap)
        merged_records.append(record)
        if len(merged_records) >= 50000:
            out_file = f"{res_folder}/{res_file_list[file_count]}"
            writeObjs2xml(out_file, merged_records, 'Answers')
            merged_records = []
            file_count += 1
        try:
            next_record = Post(next(file_iters[i]))
            heapq.heappush(heap, (next_record,i))
        except StopIteration:
            if iter_count[i] < len(groups[i]):
                file_iters[i] = iter(parse_xml(f"{tmp_folder}/{groups[i][iter_count[i]]}"))
                iter_count[i] += 1
                try:
                    next_record = Post(next(file_iters[i]))
                    heapq.heappush(heap, (next_record,i))
                except StopIteration:
                    continue
    
    if merged_records:
        out_file = f"{res_folder}/{res_file_list[file_count]}"
        # out_file = os.path.join(res_folder, f"{file_prefix}_{file_count}.xml")
        writeObjs2xml(out_file, merged_records, 'Answers')
    return


def divide_and_merge(file_list, source_folder, res_folder):
    logger = logging.getLogger(__name__)
    file_num = len(file_list)
    res = ""
    tmp = ""
    if file_num == 1: 
        logger.info(f"move file: {file_list} from {source_folder} to {res_folder}")
        sort_singal_file(file_list[0], source_folder, res_folder)
        return (res_folder, source_folder)
    else:
        group_len = (file_num+3) // 4 if file_num > 4 else 1
        grouped_files = [file_list[i:i+group_len] for i in range(0,file_num,group_len)]
        for group in grouped_files:
            if group :
                tmp, res = divide_and_merge(group, source_folder, res_folder)
        merge_files(grouped_files, res, tmp)
    return res, tmp


def extract_code_from_post(fs_config):
    post_path = fs_config['POST_DUMP_DIC']
    code_path = fs_config['SO_CODE_FOLDER']
    # sort answers
    ans_folder = f"{post_path}/answers"
    ans_files = os.listdir(ans_folder)
    tmp_folder = f"{post_path}/tmp"
    if not (os.path.exists(tmp_folder)): os.makedirs(tmp_folder)
    res, tmp = divide_and_merge(ans_files, ans_folder, tmp_folder)
    if not res==ans_folder:
        shutil.rmtree(ans_folder)
        for file in os.listdir(res):
            shutil.copyfile(f"{res}/{file}", f"{ans_folder}/{file}")
    shutil.rmtree(tmp_folder)

    # extract codes
    extracter = CodeExtracter(post_path,code_path)
    extracter.get_filtered_code_from_xml()
    pass