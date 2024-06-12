import os
from scipy.stats import mannwhitneyu

import utils

def get_CKTyper_stat(res_folder, libs):
    res_stat = []
    for lib in libs:
        lib_sum_file = f"{res_folder}/{lib}/{lib}_sum.csv"
        lib_data = utils.read_csv(lib_sum_file)[0:-1]
        for line in lib_data:
            res_stat.append(float(line[-1]))
    return res_stat


def get_iJTyper_stat(res_folder):
    res_stat = []
    res_files = os.listdir(res_folder)
    for res_file in res_files:
        data = utils.read_csv(f"{res_folder}/{res_file}")[-1]
        res_stat.append(float(data[-1].split(':')[-1]))
    return res_stat


def get_SnR_and_MLM_stat(res_folder,libs):
    snr_acc_stat = []
    snr_rcl_stat = []
    mlm_stat = []
    for lib in libs:
        res_files = os.listdir(f"{res_folder}/{lib}")
        for res_file in res_files:
            if res_file == f"{lib}.csv": continue
            res_data = utils.read_csv(f"{res_folder}/{lib}/{res_file}")[-2]
            snr_acc_stat.append(float(res_data[-2].split(':')[-1]))
            snr_rcl_stat.append(float(res_data[-1].split(':')[-1]))
            mlm_stat.append(float(res_data[1].split(':')[-1]))
    return (snr_acc_stat, snr_rcl_stat, mlm_stat)


# {
#     "<dataset>":{
#         "<method>": <p-value>,
#         ...
#     },
#     "<dataset>":{...}
# }
def cal_statistical_significance(fs_config):
    datasets = ["StatType-SO","Short-SO"]
    libs = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
    baseline_folder = fs_config['BASELINE_RESULT']
    CKTyper_folder = fs_config["RESULT_PROMPTED_FOLDER"]
    origin_folder = fs_config["RESULT_ORIGINAL_FOLDER"]
    eval_path = fs_config['EVAL_PATH']
    p_values = {
        "CKTyper v.s.":{},
        "ChatGPT_RAG v.s.":{},
        "CKTyper_noRAG v.s.":{},
    }

    for dataset in datasets:
        CKTyper_res_folder = f"{CKTyper_folder}/{dataset}"
        iJTyper_folder = f"{baseline_folder}/iJTyper/{dataset}"
        SnR_and_MLM_folder = f"{baseline_folder}/SnR+MLMTyper/{dataset}"
        ChatGPT_folder = f"{origin_folder}/no_RAG/{dataset}"
        ChatGPT_RAG_folder = f"{origin_folder}/RAG/{dataset}"
        CKTyper_noRAG_folder = CKTyper_res_folder.replace("RAG","no_RAG")

        CKTyper_stat = get_CKTyper_stat(CKTyper_res_folder, libs)
        iJTyper_stat = get_iJTyper_stat(iJTyper_folder)
        SnR_acc_stat, SnR_rcl_stat, MLM_stat = get_SnR_and_MLM_stat(SnR_and_MLM_folder, libs)
        ChatGPT_stat = get_CKTyper_stat(ChatGPT_folder, libs)
        ChatGPT_RAG_stat = get_CKTyper_stat(ChatGPT_RAG_folder, libs)
        CKTyper_noRAG_stat = get_CKTyper_stat(CKTyper_noRAG_folder, libs)
        
        _, iJTyper_p = mannwhitneyu(CKTyper_stat, iJTyper_stat)
        _, SnR_acc_p = mannwhitneyu(CKTyper_stat, SnR_acc_stat)
        _, SnR_rcl_p = mannwhitneyu(CKTyper_stat, SnR_rcl_stat)
        _, MLMTyper_p = mannwhitneyu(CKTyper_stat, MLM_stat)
        _, ChatGPT_p = mannwhitneyu(CKTyper_stat, ChatGPT_stat)
        _, ChatGPT_RAG_p = mannwhitneyu(CKTyper_stat, ChatGPT_RAG_stat)
        _, CKTyper_noRAG_p = mannwhitneyu(CKTyper_stat, CKTyper_noRAG_stat)
        CKTyper_dataset_dict = {
            "iJTyper": iJTyper_p,
            "SnR_acc": SnR_acc_p,
            "SnR_rcl": SnR_rcl_p,
            "MLMTyper": MLMTyper_p,
            "ChatGPT": ChatGPT_p,
            "ChatGPT_RAG": ChatGPT_RAG_p,
            "CKTyper_noRAG": CKTyper_noRAG_p
        }
        p_values["CKTyper v.s."][dataset] = CKTyper_dataset_dict
        _, p_values["ChatGPT_RAG v.s."][dataset] = mannwhitneyu(ChatGPT_RAG_stat, ChatGPT_stat)
        _, p_values["CKTyper_noRAG v.s."][dataset] = mannwhitneyu(CKTyper_noRAG_stat, ChatGPT_stat)
    
    res_file = f"{eval_path}/statistical_significance.json"
    utils.write_json(res_file, p_values)
    pass