import os
import utils
import logging
import matplotlib.pyplot as plt

def count_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return len(lines)


def draw_time_graph(x_data, y_data, color, title, res_file):
    plt.scatter(x_data, y_data, marker='x',c=color)
    plt.xlabel('Lines of code snippet')
    plt.ylabel('Time (s)')
    plt.title(title)
    plt.savefig(res_file)
    plt.clf()


# result:
# {
#     <lib>: {
#         <cs_name>: {
#             "lucene_search": 123,
#             "sim_cal": 123,
#             "retrieve_post": 123,
#             "generate_context": 123,
#             "type_inf": 123,
#             "lines":123,
#             "average_sum":123
#         },
#         <cs_name>: {...},
#         "lib_average": 123
#     }
#     <lib>: {...},
#     "dataset_average": 123
# }
def cal_average_process_time(fs_config):
    logger = logging.getLogger(__name__)
    record_list = {
        "StatType-SO":[],
        "Short-SO":[]
    }
    def list_dir(folder):
        if os.path.isdir(folder):
            if folder.endswith("average"): return
            files = os.listdir(folder)
            for file in files:
                list_dir(f"{folder}/{file}")
        else:
            if folder.endswith("StatType-SO.json"):
                record_list["StatType-SO"].append(f"{folder}")
            elif folder.endswith("Short-SO.json"):
                record_list["Short-SO"].append(f"{folder}")

    datasets = ["StatType-SO","Short-SO"]
    libs = ["android", "gwt", "hibernate", "joda_time", "jdk", "xstream"]
    color = {"StatType-SO":"r", "Short-SO":"b"}
    time_record_folder = fs_config['TIME_RECORD_FOLDER']
    dataset_code_folder = fs_config['DATASET_CODE_FOLDER']
    list_dir(time_record_folder)

    for dataset in datasets:
        avg_time = {}
        count = {}
        # counting lines of cs
        for lib in libs:
            lib_data = {}
            code_snippets = os.listdir(f"{dataset_code_folder}/{dataset}/{lib}")
            for cs in code_snippets:
                cs_name = cs.split('.')[0]
                lines = count_lines(f"{dataset_code_folder}/{dataset}/{lib}/{cs}")
                lib_data[cs_name] = {
                    "lucene_search": 0,
                    "sim_cal": 0,
                    "retrieve_post": 0,
                    "generate_context": 0,
                    "type_inf": 0,
                    "lines":lines
                }
                count[cs_name] = {
                    "lucene_search": 0,
                    "sim_cal": 0,
                    "retrieve_post": 0,
                    "generate_context": 0,
                    "type_inf": 0
                }
            avg_time[lib] = lib_data
            count[lib] = count
        # accumulating processing time
        for record in record_list[dataset]:
            logger.info(f"Processing {record}")
            dataset_record = utils.load_json(record)
            for lib in libs:
                lib_record = dataset_record[lib]
                for cs_name in lib_record:
                    cs_record = lib_record[cs_name]
                    for key in cs_record:
                        avg_time[lib][cs_name][key] += cs_record[key]
                        count[lib][cs_name][key] += 1
        # calculating average processing time
        dataset_sum = 0
        dataset_count = 0
        x_data = []
        y_data = []
        for lib in avg_time:
            lib_sum = 0
            lib_count = 0
            for cs in avg_time[lib]:
                cs_sum = 0
                for key in avg_time[lib][cs]:
                    if key == "lines": continue
                    avg_time[lib][cs][key] /= count[lib][cs][key]
                    cs_sum += avg_time[lib][cs][key]
                avg_time[lib][cs]["average_sum"] = cs_sum
                y_data.append(cs_sum)
                lines = (int(avg_time[lib][cs]["lines"]/10)+1)*10 if dataset=="StatType-SO" else avg_time[lib][cs]["lines"]
                x_data.append(lines)
                lib_sum += cs_sum
                lib_count += 1
                
            avg_time[lib]["lib_average"] = lib_sum/lib_count
            dataset_sum += lib_sum
            dataset_count += lib_count

        # drawing graph
        fig_path = f"{time_record_folder}/average/average_time_{dataset}.png"
        fig_title = f'Average processing time of {dataset}'
        draw_time_graph(x_data, y_data, color[dataset], fig_title, fig_path)

        avg_time["dataset_average"] = dataset_sum/dataset_count
        y_data = sorted(y_data)
        avg_time["dataset_median"] = y_data[len(y_data)//2]
        avg_time["dataset_min"] = y_data[0]
        avg_time["dataset_max"] = y_data[-1]

        res_file = f"{time_record_folder}/average/average_time_{dataset}.json"
        utils.write_json(res_file, avg_time)
        logger.info(f"Average processing time of {dataset} has saved to {res_file}")

    