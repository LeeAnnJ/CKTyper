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
    eval_path = fs_config['EVAL_PATH']
    baseline_folder = fs_config['BASELINE_RESULT']
    RQ3_folder = f"{eval_path}/RQ3/"
    origin_folder = fs_config["RESULT_ORIGINAL_FOLDER"]
    eval_path = fs_config['EVAL_PATH']
    p_values = {
        "CKTyper v.s.":{},
    }

    for dataset in datasets:
        CKTyper_res_folder = f"{RQ3_folder}CKTyper/{dataset}"
        iJTyper_folder = f"{baseline_folder}/iJTyper/{dataset}"
        SnR_and_MLM_folder = f"{baseline_folder}/SnR+MLMTyper/{dataset}"
        ChatGPT_folder = f"{origin_folder}/{dataset}"
        CKTyper_TypeFilter_folder = f"{RQ3_folder}CKTyper-TypeFilter/{dataset}"
        CKTyper_CKGG_folder = f"{RQ3_folder}CKTyper-CKGG/{dataset}"
        CKTyper_S_NER_folder = f"{RQ3_folder}CKTyper-S-NER/{dataset}"
        CKTyper_Full_folder = f"{RQ3_folder}CKTyper-Full/{dataset}"
        CKTyper_CS_folder = f"{RQ3_folder}CKTyper-CS/{dataset}"
        CKTyper_Desc_folder = f"{RQ3_folder}CKTyper-Desc/{dataset}"
        
        CKTyper_stat = get_CKTyper_stat(CKTyper_res_folder, libs)
        iJTyper_stat = get_iJTyper_stat(iJTyper_folder)
        SnR_acc_stat, SnR_rcl_stat, MLM_stat = get_SnR_and_MLM_stat(SnR_and_MLM_folder, libs)
        ChatGPT_stat = get_CKTyper_stat(ChatGPT_folder, libs)
        CKTyper_CKGG_stat = get_CKTyper_stat(CKTyper_CKGG_folder, libs)
        CKTyper_TypeFilter_stat = get_CKTyper_stat(CKTyper_TypeFilter_folder, libs)
        CKTyper_S_NER_stat = get_CKTyper_stat(CKTyper_S_NER_folder, libs)
        CKTyper_Full_stat = get_CKTyper_stat(CKTyper_Full_folder,libs)
        CKTyper_CS_stat = get_CKTyper_stat(CKTyper_CS_folder,libs)
        CKTyper_Desc_stat = get_CKTyper_stat(CKTyper_Desc_folder,libs)
        
        _, iJTyper_p = mannwhitneyu(CKTyper_stat, iJTyper_stat)
        _, SnR_acc_p = mannwhitneyu(CKTyper_stat, SnR_acc_stat)
        _, SnR_rcl_p = mannwhitneyu(CKTyper_stat, SnR_rcl_stat)
        _, MLMTyper_p = mannwhitneyu(CKTyper_stat, MLM_stat)
        _, ChatGPT_p = mannwhitneyu(CKTyper_stat, ChatGPT_stat)
        _, CKTyper_CKGG_p = mannwhitneyu(CKTyper_stat, CKTyper_CKGG_stat)
        _, CKTyper_TypeFilter_p = mannwhitneyu(CKTyper_stat, CKTyper_TypeFilter_stat)
        _, CKTyper_S_NER_p = mannwhitneyu(CKTyper_stat, CKTyper_S_NER_stat)
        _, CKTyper_FUll_p = mannwhitneyu(CKTyper_stat, CKTyper_Full_stat)
        _, CKTyper_CS_p = mannwhitneyu(CKTyper_stat, CKTyper_CS_stat)
        _, CKTyper_Desc_p = mannwhitneyu(CKTyper_stat, CKTyper_Desc_stat)

        CKTyper_dataset_dict = {
            "iJTyper": iJTyper_p,
            "SnR_acc": SnR_acc_p,
            "SnR_rcl": SnR_rcl_p,
            "MLMTyper": MLMTyper_p,
            "ChatGPT": ChatGPT_p,
            "CKTyper-CKGG": CKTyper_CKGG_p,
            "CKTyper_TypeFilter": CKTyper_TypeFilter_p,
            "CKTyper_S_NER": CKTyper_S_NER_p,
            "CKTyper_Full": CKTyper_FUll_p,
            "CKTyper_CS": CKTyper_CS_p,
            "CKTyper_Desc": CKTyper_Desc_p,
        }
        p_values["CKTyper v.s."][dataset] = CKTyper_dataset_dict
    
    res_file = f"{eval_path}/statistical_significance.json"
    utils.write_json(res_file, p_values)
    pass