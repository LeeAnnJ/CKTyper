import os
import configparser

"""
Two different ways for obtaining the current directory path:
1) os.getcwd() vs. 2) os.path.dirname(os.path.realpath(__file__))
see: https://blog.csdn.net/cyjs1988/article/details/77839238/
"""
class SOProcessConfig:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/file_structure.ini')
        self.so_dir = config['resource']['SO_DATA_STORAGE']  # local dir that hosts SO data
        self.experiment_dir = f"{self.so_dir}/../SOData"
        self.so_tags_dir = os.path.join(self.experiment_dir, 'tags')
        self.posts_xml = os.path.join(self.so_dir, "Posts.xml")
        # self.comments_xml = os.path.join(self.so_dir, "Posts.xml")
        self.interested_tags = ["java"]


def read_file_structure():
    fs_config = {}
    config = configparser.ConfigParser()
    config.read('./config/path_config.ini')
    fs_config['POST_DUMP_DIC'] = config['resource']['POST_DUMP_DIC']
    fs_config['SO_CODE_FOLDER'] = config['resource']['SO_CODE_FOLDER']
    fs_config['CODE_LUCENE_INDEX'] = config['resource']['CODE_LUCENE_INDEX']
    fs_config['POST_LUCENE_INDEX'] = config['resource']['POST_LUCENE_INDEX']
    fs_config['DATASET_CODE_FOLDER'] = config['resource']['DATASET_CODE_FOLDER']
    fs_config['API_ELEMENTS_FOLDER'] = config['resource']['API_ELEMENTS_FOLDER']
    fs_config['BASELINE_RESULT'] = config['resource']['BASELINE_RESULT']
    fs_config['INTER_RECORD_FOLDER'] = config['intermediate']['INTER_RECORD_FOLDER']
    fs_config['TIME_RECORD_FOLDER'] = config['intermediate']['TIME_RECORD_FOLDER']
    fs_config['LUCENE_FOLDER'] = config['intermediate']['LUCENE_FOLDER']
    fs_config['SEARCHED_POST_FOLDER'] = config['intermediate']['SEARCHED_POST_FOLDER']
    fs_config['NGRAM_FILE'] = config['intermediate']['NGRAM_FILE']
    fs_config['SIM_CS_SCORE_FOLDER'] = config['intermediate']['SIM_CS_SCORE_FOLDER']
    fs_config['GENERATED_QUESTOIN_FOLDER'] = config['intermediate']['GENERATED_QUESTOIN_FOLDER']
    fs_config['API_DICT_FILE'] = config['intermediate']['API_DICT_FILE']
    fs_config['EVAL_PATH'] = config['result']['EVAL_PATH']
    fs_config['INFERENCE_RESULT_FOLDER'] = config['result']['INFERENCE_RESULT_FOLDER']
    # fs_config['RESULT_SINGAL'] = config['result']['RESULT_SINGAL']
    return fs_config