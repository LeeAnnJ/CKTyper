import csv
import utils
import logging


def extract_fqn(fs_config):
    csv_files = ["../data/baseline_result/sql_csv/mvn_class.csv","../data/baseline_result/sql_csv/mvn_interface.csv"]
    res_file = fs_config['FQN_FILE']
    logger = logging.getLogger(__name__)
    fqn_list = set()

    for csv_file in csv_files:
        data = utils.read_csv(csv_file)
        for row in data:
            fqn = row[2].replace('/','.').replace('$','.')
            logger.debug(f"Extracted FQN: {fqn}")
            fqn_list.add(fqn)

    logger.info(f"Extracted {len(fqn_list)} FQNs,save to: {res_file}")
    utils.write_pickle(res_file,fqn_list)
    return

# def read_csv_column(csv_file, column_name):
#     column_content = []
#     with open(csv_file, 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             column_content.append(row[column_name])
#     return column_content

# # Example usage
# csv_file = '/path/to/your/csv/file.csv'
# column_name = 'column_name'
# column_content = read_csv_column(csv_file, column_name)
# print(column_content)