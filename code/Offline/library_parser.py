import re
import logging

import utils


# csv file can be downloaded from https://anonymous.4open.science/r/iJTyper-0A4D/Code/ours/sql_csv
# if you want to extract FQN from your own API library, you can use ~/code/Java/SnR-target to Parse jar files.
# instruction can be found in https://zenodo.org/records/5843327
def extract_fqn(fs_config):
    csv_files = ["../Data/from_iJTyper/sql_csv/mvn_class.csv", "../Data/from_iJTyper/sql_csv/mvn_interface.csv"]
    res_file = fs_config['API_DICT_FILE']
    logger = logging.getLogger(__name__)
    fqn_list = set()
    simple_list = set()
    # count = dict()

    for csv_file in csv_files:
        data = utils.read_csv(csv_file)
        for row in data:
            fqn = row[2].replace('/','.')
            fqn = re.sub(r'\$[1-9]+','',fqn,flags=re.DOTALL)
            fqn = fqn.replace('$','.')
            if len(row) > 4:
                super_class = row[4].replace('/','.')
                super_class = re.sub(r'\$[1-9]+','',super_class,flags=re.DOTALL)
                super_class = super_class.replace('$','.')
            else:
                super_class = ''

            logger.debug(f"Extracted FQN: {fqn}, super class: {super_class}")
            fqn_list.update([fqn, super_class])
            simple = fqn.split('.')[-2:] + super_class.split('.')[-2:]
            simple_list.update(simple)
            # for s in simple:
            #     if s not in count: count[s] = 1
            #     else: count[s] += 1

    # top_keys = sorted(count.keys(), key=lambda x:count[x], reverse=True)
    # print("top keys:", top_keys[:30])
    # freq_simple = ['com','google','internal','apache','xml','client','api','core','common','security']
    # simple_list.difference_update(freq_simple)
    api_list = simple_list.copy()
    api_list.update(fqn_list)
    fqn_dict = {
        'fqn_list':fqn_list,
        'simple_list':api_list
    }
    logger.info(f"Extracted {len(fqn_list)} FQNs, {len(simple_list)} simple name, save to: {res_file}")
    utils.write_pickle(res_file,fqn_dict)
    return 