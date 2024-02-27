import os
import sys
import logging
import configparser

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

miss_info = "\"<FQN not provided, as it seems to be a custom interface or not present in the code snippet>\""


# return: [total,correct,wrong,precision,recall]
def cal_precision_recall_singal(result_file):
    data = utils.read_csv(result_file)
    head = ["Node","ChatGPT Answer","Truth","Correct"]
    total = 0
    correct = 0
    wrong = 0
    res_data = []
    for line in data:
        if line[0].startswith('Total'):
            break
        res_line = line[:3]
        ans = line[1]
        truth = line[2]
        total += 1
        if ans == truth:
            res_line.append("1")
            correct += 1
        elif ans == miss_info:
            res_line.append("0")
        else:
            res_line.append("0")
            wrong += 1
        res_data.append(res_line)
    if (correct+wrong)==0: precision = 0
    else: precision = correct / (correct + wrong)
    recall = correct / total
    res_data.append([f'Total: {total}', f'Correct: {correct}', f'Wrong:  {wrong}', f'Precision: {precision}', f'Recall: {recall}'])
    utils.write_csv(result_file, res_data, head)
    return [total,correct,wrong,precision,recall]


# save total data for every lib & dataset
def cal_precision_recall_pipline(datasets,libs,original:bool):
    config = configparser.ConfigParser()
    config.read('./config/file_structure.ini')
    if original: res_folder = config['result']['RESULT_ORIGINAL_FOLDER']
    else: res_folder = config['result']['RESULT_PROMPTED_FOLDER']
    logger = logging.getLogger(__name__)
    header = ["name","total", "correct", "wrong", "precision", "recall"]
    infos = []
    for dataset in datasets:
        dataset_folder = f'{res_folder}/{dataset}'
        dataset_statistic = []
        dataset_total = 0
        dataset_correct = 0
        dataset_wrong = 0

        for lib in libs:
            lib_folder = f'{dataset_folder}/{lib}'
            cs_results = os.listdir(lib_folder)
            lib_statistic = []
            lib_total = 0
            lib_correct = 0
            lib_wrong = 0

            for cs_res in cs_results:
                if cs_res == f'{lib}_sum.csv':
                    continue
                cs_name = cs_res.split('.')[0]
                logger.info(f"Calculate precision & recall for: {cs_name}")
                res_file = f'{lib_folder}/{cs_res}'
                cs_statistic = cal_precision_recall_singal(res_file)
                lib_total += int(cs_statistic[0])
                lib_correct += int(cs_statistic[1])
                lib_wrong += int(cs_statistic[2])
                lib_statistic.append([cs_name]+cs_statistic)
            
            lib_precision = lib_correct / (lib_correct + lib_wrong)
            lib_recall = lib_correct / lib_total
            lib_info = [lib_total, lib_correct,lib_wrong, lib_precision, lib_recall]
            lib_statistic.append(["Sum"]+lib_info)
            lib_res_file = f'{lib_folder}/{lib}_sum.csv'
            logger.info(f"Save precision & recall for lib: {lib}")
            utils.write_csv(lib_res_file, lib_statistic, header)

            dataset_total += lib_total
            dataset_correct += lib_correct
            dataset_wrong += lib_wrong
            dataset_statistic.append([lib]+lib_info)

        dataset_precision = dataset_correct / (dataset_correct + dataset_wrong)
        dataset_recall = dataset_correct / dataset_total
        dataset_statistic.append(["Sum",dataset_total, dataset_correct, dataset_wrong, dataset_precision, dataset_recall])
        dataset_res_file = f'{dataset_folder}/{dataset}_sum.csv'
        logger.info(f"Save precision & recall for dataset: {dataset}")
        utils.write_csv(dataset_res_file, dataset_statistic, header)
        infos.append(f'dataset: {dataset}, total: {dataset_total}, correct: {dataset_correct}, wrong:{dataset_wrong}, precision: {dataset_precision}, recall: {dataset_recall}')

    for info in infos: logger.info(info)
    pass