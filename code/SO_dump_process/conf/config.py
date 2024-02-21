import simplejson
import os


"""
Two different ways for obtaining the current directory path:
1) os.getcwd() vs. 2) os.path.dirname(os.path.realpath(__file__))
see: https://blog.csdn.net/cyjs1988/article/details/77839238/
"""
config_json = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

class Config:

    def __init__(self):
        with open(config_json, 'r') as f:
            content = f.read()
        config = simplejson.loads(content)
        self.so_url = config['so_url']
        self.so_dir = config['so_dir']  # local dir that hosts SO data
        self.experiment_dir = config['experiment_dir']
        self.posts_xml = os.path.join(self.so_dir, config['posts_xml'])
        self.comments_xml = os.path.join(self.so_dir, config['comments_xml'])
        self.posthistory_xml = os.path.join(self.so_dir, config['posthistory_xml'])
        self.tags_xml = os.path.join(self.so_dir, config['tags_xml'])
        self.interested_tags = config['interested_tags']

        self.tagcate_dir = os.path.join(self.experiment_dir, 'tag_categorization_new')
        self.lang_models_dir = os.path.join(self.experiment_dir, 'lang_models')
        self.eval_dir = os.path.join(self.experiment_dir, 'evaluation')
        self.baselines_dir = os.path.join(self.eval_dir, 'baselines')

        if not os.path.exists(self.tagcate_dir):
            os.makedirs(self.tagcate_dir)
        if not os.path.exists(self.lang_models_dir):
            os.makedirs(self.lang_models_dir)
        if not os.path.exists(self.baselines_dir):
            os.makedirs(self.baselines_dir)
