import re
import utils
import logging


def extract_fqn(fs_config):
    csv_files = ["../data/from_iJTyper/sql_csv/mvn_class.csv","../data/from_iJTyper/sql_csv/mvn_interface.csv"]
    res_file = fs_config['FQN_FILE']
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
            logger.debug(f"Extracted FQN: {fqn}")
            fqn_list.add(fqn)
            simple = fqn.split('.')[-2:]
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