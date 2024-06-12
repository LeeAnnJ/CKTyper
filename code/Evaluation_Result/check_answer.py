import os
import logging

import utils

def list_not_perfect_file(fs_config, datasets):
    record_folder = f"{fs_config['INTER_RECORD_FOLDER']}/wrong_answer"
    not_finished = set()
    for dataset in datasets:
        res_file = f'{record_folder}/{dataset}_wrong.csv'
        data = utils.read_csv(res_file)
        for line in data:
            not_finished.add(line[0])
    print("Not perfect file: ", not_finished)
    return list(not_finished)

def list_wrong_answer_pipline(fs_config, datasets, libs, original:bool):
    logger = logging.getLogger(__name__)
    if original: res_folder = fs_config['RESULT_ORIGINAL_FOLDER']
    else: res_folder = fs_config['RESULT_PROMPTED_FOLDER']
    record_folder = f"{fs_config['INTER_RECORD_FOLDER']}/wrong_answer"
    if not os.path.exists(record_folder): os.makedirs(record_folder)
    head = ["CS_name","Node","ans","truth"]

    for dataset in datasets:
        wrong = []
        dataset_folder = f'{res_folder}/{dataset}'
        for lib in libs:
            lib_folder = f'{dataset_folder}/{lib}'
            cs_results = os.listdir(lib_folder)
            for cs_res in cs_results:
                if cs_res == f'{lib}_sum.csv':
                    continue
                cs_name = cs_res.split('.')[0]
                # logger.info(f"Check wrong answer for: {cs_name}")
                res_file = f'{lib_folder}/{cs_res}'
                # wrong_answer = list_wrong_answer_singal(res_file,cs_name)
                data = utils.read_csv(res_file)
                for line in data:
                    if line[0].startswith('Total:'): break
                    ans = line[1]
                    truth = line[2]
                    node = line[0]
                    if ans != truth: 
                        record = [cs_name, node, ans, truth]
                        logger.info(f"Wrong answer: {record}")
                        wrong.append(record)
            dst_res_file = f'{record_folder}/{dataset}_wrong.csv'
            utils.write_csv(dst_res_file, wrong, head)
            logger.info(f"Save wrong answer to: {dst_res_file}") 
    return